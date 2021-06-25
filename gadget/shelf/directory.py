import uuid
from pathlib import Path, PurePath
from datetime import datetime

home = Path.home()
shelf = home / ".gadget"
shelf.mkdir(exist_ok=True)

job = None
data = None
timestamp = None


def mk_job(name: str):
    """
    :name of the experiment
    """
    global timestamp, job, data
    assert isinstance(name, str)
    timestamp = datetime.now().isoformat()
    job = shelf / name
    job.mkdir(exist_ok=True)
    data = job / PurePath("data")
    data.mkdir(exist_ok=True)


def get_index():
    """
    TODO: Connect to a SQL DB
    """
    return job / PurePath(timestamp).with_suffix(".json") if job is not None else None


def get_latest():
    return job / PurePath("latest").with_suffix(".json") if job is not None else None


def get_pkl_ref() -> PurePath:
    while True:
        candidate = data / PurePath(uuid.uuid4().hex).with_suffix(".pkl")
        if not candidate.exists():
            return candidate
