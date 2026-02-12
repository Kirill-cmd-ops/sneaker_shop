class DomainException(Exception):
    ...


class SneakerNotFound(DomainException):
    ...


class SneakerAlreadyExists(DomainException):
    ...


class SneakerIsInactive(DomainException):
    ...


class OneTimeSubscriptionIsActive(DomainException):
    ...


class OneTimeSubscriptionAlreadyExists(DomainException):
    ...


class OneTimeSubscriptionNotFound(DomainException):
    ...


class PermanentSubscriptionIsActive(DomainException):
    ...


class PermanentSubscriptionAlreadyExists(DomainException):
    ...

class PermanentSubscriptionNotFound(DomainException):
    ...
