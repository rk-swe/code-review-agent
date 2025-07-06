class AppBaseError(Exception):
    message: str

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class AppInternalError(AppBaseError):
    pass


class AppUserError(AppBaseError):
    pass
