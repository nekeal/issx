from attrs import field, frozen


@frozen
class Issue:
    id: int = field()
    title: str = field()
    description: str = field()
    web_url: str = field(default=None)
    reference: str = field(default=None)
