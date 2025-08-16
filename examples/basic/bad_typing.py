def x(a: str) -> int:
    return ord(a)


def y():
    c: int = x('a')
    d: float = x('a')
    e: int = x(0)

