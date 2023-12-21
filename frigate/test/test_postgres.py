import datetime

import pytest

from playhouse.postgres_ext import PostgresqlExtDatabase
from frigate.models import EventCloud
from frigate.mebaya.settings import PGSettings



def test_pg_connection():
    dbcloud = PostgresqlExtDatabase(
        PGSettings.POSTGRES_DB,
        user=PGSettings.POSTGRES_USER,
        password=PGSettings.POSTGRES_PASSWD,
        host=PGSettings.POSTGRES_ADDRESS,
        port=PGSettings.POSTGRES_PORT)
    models = [EventCloud]
    dbcloud.bind(models)
    dbcloud.connect()
    dbcloud.create_tables(models)

    event_cloud = {
        EventCloud.id: 0,
        EventCloud.label: "test",
        EventCloud.camera: "test",
        EventCloud.start_time: datetime.datetime.now(),
        EventCloud.path: "test"
    }
    (
        # MEBAYA
        EventCloud.insert(event_cloud)
        .on_conflict(
            conflict_target=[EventCloud.id],
            update=event_cloud,
        )
        .execute()
    )