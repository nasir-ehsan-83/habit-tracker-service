from enum import Enum

class UserRole(int, Enum):
    user = 1789
    admin = 2020

class UserStatus(str, Enum):
    active = "active"
    deleted = "deleted"

class HabitStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    skipped = "skipped"
    deleted = "deleted"

