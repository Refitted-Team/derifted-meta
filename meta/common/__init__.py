import os
import datetime

DATETIME_FORMAT_HTTP = "%a, %d %b %Y %H:%M:%S %Z"


def serialize_datetime(dt: datetime.datetime):
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat()


def polymc_path():
    if "PMC_DIR" in os.environ:
        return os.environ["PMC_DIR"]
    return "polymc"


def upstream_path():
    if "UPSTREAM_DIR" in os.environ:
        return os.environ["UPSTREAM_DIR"]
    return "upstream"


def ensure_upstream_dir(path):
    path = os.path.join(upstream_path(), path)
    if not os.path.exists(path):
        os.makedirs(path)


def ensure_component_dir(component_id):
    path = os.path.join(polymc_path(), component_id)
    if not os.path.exists(path):
        os.makedirs(path)


def transform_maven_key(maven_key: str):
    return maven_key.replace(":", ".")
