import os
import json
import datetime
from typing import Union

from frigate.models import Event
from frigate.const import (
                            EXPORT_DIR,
                            RECORD_DIR,
                            CLOUD_DIR)


def get_datetime_from_timestamp(timestamp: int) -> str:
    """Convenience fun to get a simple date time from timestamp."""
    try:
        dt = datetime.datetime.fromtimestamp(timestamp).strftime("%Y_%m_%d_%H_%M")
    except:
        dt = "na"
    return dt


def find_record_name(start_time: Union[datetime.datetime, float], camera) -> str:
    """
    Args:
        start_time (datetime.datetime of float) if float it should be timestamp
    Returns:
        str: path
    """
    if isinstance(start_time, float):
        start_time = datetime.datetime.fromtimestamp(start_time)
    directory = os.path.join(
        start_time.strftime("%Y-%m-%d/%H"),
        camera,
    )
    # file will be in utc due to start_time being in utc
    file_name = f"{start_time.strftime('%M.%S.mp4')}"
    file_path = os.path.join(directory, file_name)
    return file_path


class EventToJson:
    # /home/mvision/apps/frigate/frigate/events/maintainer.py
    # /home/mvision/apps/frigate/frigate/record/export.py
    def __init__(self, event_config):
        self.event_config = event_config
        pass

    def process(self, event_data: Event):

        start_time = event_data["start_time"] - self.event_config.pre_capture
        end_time = (
                None
                if event_data["end_time"] is None
                else event_data["end_time"] + self.event_config.post_capture
            )
        # get recording name it may not be present yet
        recording = find_record_name(start_time, event_data['camera'])
        event_json = dict(
                    id=event_data['id'],
                    camera=event_data['camera'],
                    label=event_data["label"],
                    start_time=start_time,
                    end_time=end_time,
                    path=recording
                )
        cloud_filename = recording.replace(RECORD_DIR, CLOUD_DIR)
        self.save(event_json, cloud_filename)

        
    def save(self, event_json, filename):
        
        with open(filename, "wt") as fp:
            json.dump(event_json, fp)
