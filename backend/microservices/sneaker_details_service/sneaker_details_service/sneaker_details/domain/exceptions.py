class DomainException(Exception):
    ...


class RecordAlreadyExists(DomainException):
    ...


class SneakerNotFound(DomainException):
    ...


class SneakerAlreadyExists(DomainException):
    ...


class SneakerAssociationAlreadyExists(DomainException):
    ...


class SneakerSizeAlreadyExists(DomainException):
    ...


class SneakerSizeNotFound(DomainException):
    ...