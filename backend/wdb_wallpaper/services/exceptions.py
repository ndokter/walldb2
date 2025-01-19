class ServiceError(Exception):
    pass


class UnsupportedFileExtensionError(ServiceError):
    pass