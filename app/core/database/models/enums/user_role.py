from enum import Enum

class UserRole(str, Enum):
    MEMBER = "member"
    TEAM_ADMIN = "team_admin"
    SUPERUSER = "superuser"