class DomainException(Exception):
    ...


class FavoriteNotFound(DomainException):
    ...


class SneakerNotFound(DomainException):
    ...


class SneakerSizeNotAvailable(DomainException):
    ...


class SneakerNotFoundInFavorite(DomainException):
    ...
