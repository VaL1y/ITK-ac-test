from enum import Enum

class TaskStatus(str, Enum):
    new = "new"
    in_progress = "in_progress"
    done = "done"