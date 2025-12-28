from enum import Enum


class SubscriptionStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE_BY_USER = "INACTIVE_BY_USER"
    INACTIVE_BY_SYSTEM = "INACTIVE_BY_SYSTEM"
