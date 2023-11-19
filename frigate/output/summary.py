"""Handle outputting low res / fps summary segments from decoded frames."""

import logging
import multiprocessing as mp
import queue
import subprocess as sp
import threading

from frigate.config import CameraConfig
from frigate.log import LogPipe

logger = logging.getLogger(__name__)


class FFMpegConverter(threading.Thread):
    def __init__(
        self,
        config: CameraConfig,
        input_queue: queue.Queue,
        logpipe: LogPipe,
        stop_event: mp.Event,
    ):
        threading.Thread.__init__(self)
        self.name = f"{config.name}_output_converter"
        self.camera = config.name
        self.input_queue = input_queue
        self.logpipe = logpipe
        self.stop_event = stop_event

        ffmpeg_cmd = [
            "ffmpeg",
            "-hide_banner",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "yuv420p",
            "-video_size",
            f"{config.detect.width}x{config.detect.height}",
            "-i",
            "pipe:",
            "-f",
            "mpegts",
            "-c:v",
            "libx264",
            "-bf",
            "0",
            "-fps_mode",
            "vfr",
            "-r",
            "5",
            "/media/frigate/summary.ts",
        ]

        self.process = sp.Popen(
            ffmpeg_cmd,
            stdout=sp.DEVNULL,
            stderr=logpipe,
            stdin=sp.PIPE,
            start_new_session=True,
        )

    def __write(self, b) -> None:
        try:
            self.process.stdin.write(b)
        except BrokenPipeError:
            self.logpipe.dump()

    def exit(self):
        self.process.terminate()

        try:
            self.process.communicate(timeout=30)
        except sp.TimeoutExpired:
            self.process.kill()
            self.process.communicate()

    def run(self) -> None:
        while not self.stop_event.is_set():
            try:
                frame = self.input_queue.get(True, timeout=1)
                self.__write(frame)
            except queue.Empty:
                pass

        self.exit()


class SummaryRecorder:
    def __init__(self, config: CameraConfig, stop_event: mp.Event) -> None:
        self.config = config
        self.input = queue.Queue(maxsize=config.detect.fps)
        self.logpipe = LogPipe(f"ffmpeg.{config.name}.summary")
        self.converter = FFMpegConverter(
            config,
            self.input,
            self.logpipe,
            stop_event,
        )
        self.converter.start()

    def should_write_frame(
        self,
        current_tracked_objects: list[dict[str, any]],
        motion_boxes: list[list[int]],
    ) -> bool:
        """Decide if this frame should be added to summary."""

        # send frame if a non-stationary object is in a zone
        if any((len(o["current_zones"]) > 0 and not o["stationary"]) for o in current_tracked_objects):
            return True

        # TODO think of real motion box logic to use
        if len(motion_boxes) % 2 == 1:
            return True

        return False

    def write_data(
        self,
        current_tracked_objects: list[dict[str, any]],
        motion_boxes: list[list[int]],
        frame,
    ) -> None:
        if self.should_write_frame(current_tracked_objects, motion_boxes):
            try:
                self.input.put_nowait(frame.tobytes())
            except queue.Full:
                # drop frames if queue is full
                pass

    def exit(self) -> None:
        self.converter.join()
