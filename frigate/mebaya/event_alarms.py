import os
import json
import datetime
from typing import Union

from frigate.models import Event, EventCloud
from frigate.const import (
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


class EventToCloudEvent:
    # /home/mvision/apps/frigate/frigate/events/maintainer.py
    # /home/mvision/apps/frigate/frigate/record/export.py
    def __init__(self, devicename: str, model_type: str):
        self.model_type = model_type
        self.devicename = devicename

    def send(self, event_data: dict, event_config):

        start_time = event_data["start_time"] - event_config.pre_capture
        # get recording name it may not be present yet
        recording = find_record_name(start_time, event_data['camera'])
        cloud_filename = recording.replace(RECORD_DIR, CLOUD_DIR)
        # score if snapshot is available
        score = None if event_data["snapshot"] is None else event_data["snapshot"]["score"]
        # numeric time stamp to datetime
        start_time_dt = datetime.datetime.fromtimestamp(start_time)

        eventdict = dict(
                    id=event_data['id'],
                    device=self.devicename,
                    camera=event_data['camera'],
                    label=event_data["label"],
                    start_time=start_time_dt,
                    path=cloud_filename,
                    model_type=event_data['model_type'],
                    top_score=event_data['top_score'],
                    score=score
                )
        self.execute(eventdict)

    def execute(self, eventdict: dict) -> None:
        (
            EventCloud.insert(eventdict)
            .on_conflict(
                conflict_target=[EventCloud.id],
                update=eventdict,
            )
            .execute()
        )
    def update(self, eventdict: dict) -> None:

        start_time_dt = datetime.datetime.fromtimestamp(eventdict['start_time'])
        if 'end_time' in eventdict:
            end_time_dt = datetime.datetime.fromtimestamp((eventdict['end_time']))
        else:
            end_time_dt = None
        eventdict = dict(
                    id=eventdict['id'],
                    device=self.devicename,
                    camera=eventdict['camera'],
                    label=eventdict["label"],
                    start_time=start_time_dt,
                    end_time=end_time_dt,
                    model_type=self.model_type,
                    top_score=eventdict['top_score'],
                    score=eventdict['score'],
                    updated=True
                )
        EventCloud.update(eventdict).where(EventCloud.id == eventdict["id"]).execute()


class RecordExtractor:

