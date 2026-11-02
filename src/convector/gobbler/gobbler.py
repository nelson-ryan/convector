from pathlib import Path

class Gobbler:
    """ Parent class for iterators
        path (Path): path to source, file or dir
    """
    def __init__(self, source):
        self.source = source

    def __iter__(self):
        if isinstance(self.source, Path):
            if self.source.is_file():
                yield from self._gobble_file(self.source)
            if self.source.is_dir():
                yield from self._gobble_dir(self.source)
        elif isinstance(self.source, list):
            yield from self._process(self.source)

    def _gobble_file(self, source):
        raise NotImplementedError

    def _gobble_dir(self, source):
        raise NotImplementedError

    def _process(self, source):
        raise NotImplementedError


