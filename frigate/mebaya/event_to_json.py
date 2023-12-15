import json
import datetime

from frigate.models import Event
from frigate.const import EXPORT_DIR, MAX_PLAYLIST_SECONDS


def get_datetime_from_timestamp(timestamp: int) -> str:
    """Convenience fun to get a simple date time from timestamp."""
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y_%m_%d_%H_%M")


class EventToJson:
    # /home/mvision/apps/frigate/frigate/events/maintainer.py
    # /home/mvision/apps/frigate/frigate/record/export.py
    def __init__(self):
        pass

    def process(self, event_data: Event, event_config):

        start_time = event_data["start_time"] - event_config.pre_capture
        end_time = (
                None
                if event_data["end_time"] is None
                else event_data["end_time"] + event_config.post_capture
            )
        event_json = dict(
                    id=event_data['id'],
                    camera=event_data['camera'],
                    label=event_data["label"],
                    start_time=start_time,
                    end_time=end_time
                )
        filename = self.name(camera=event_data['camera'], start_time=start_time, end_time=end_time)
        self.save(event_json, filename)
        return event_json
        
    def save(self, event_json, filename):
        
        with open(filename, "wt") as fp:
            json.dump(event_json, fp)

    def name(self, camera, start_time, end_time):
        final_file_name = f"{EXPORT_DIR}/{camera}_{get_datetime_from_timestamp(start_time)}__{get_datetime_from_timestamp(end_time)}.json"
        return final_file_name