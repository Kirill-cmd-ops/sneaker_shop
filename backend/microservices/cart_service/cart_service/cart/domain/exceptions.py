class DomainException(Exception):
    ...


class CartNotFound(DomainException):
    ...


class SneakerNotFound(DomainException):
    ...


class SneakerSizeNotAvailable(DomainException):
    ...


class SneakerNotFoundInCart(DomainException):
    ...
