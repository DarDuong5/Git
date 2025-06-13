class GitIgnore:
    def __init__(self, absolute: list[tuple[str , bool]] = None, scoped: dict[str, list[tuple[str, bool]]] = None):
        self.absolute = absolute
        self.scoped = scoped