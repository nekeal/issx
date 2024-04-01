import attr


@attr.s()
class Issue:
    id: int = attr.ib()
    title: str = attr.ib()
    description: str = attr.ib()
    web_url: str = attr.ib(default=None)
    reference: str = attr.ib(default=None)
