class BaseDomainException(Exception):
    message: str | None = None
    status: int = 400

    def __init__(self, message: str | None = None) -> None:
        self.message = message if message else self.message


class DialogAlreadyExistException(BaseDomainException):
    message = "Dialog already exist"
