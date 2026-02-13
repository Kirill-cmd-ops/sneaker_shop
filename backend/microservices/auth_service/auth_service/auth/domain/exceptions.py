class DomainException(Exception):
    ...


class RoleNotFound(DomainException):
    ...


class UserNotFound(DomainException):
    ...

class UserRoleAssociationAlreadyExists(DomainException):
    ...


class BlacklistAlreadyExists(DomainException):
    ...
