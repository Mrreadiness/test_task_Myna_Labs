import dataclasses


@dataclasses.dataclass
class Pagination:
    limit: int = 10
    offset: int = 0
