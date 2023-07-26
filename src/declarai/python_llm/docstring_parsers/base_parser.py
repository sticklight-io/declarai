from abc import ABC


class BaseDocStringParser(ABC):
    def docstring(self):
        raise NotImplementedError()

    def description(self):
        raise NotImplementedError()

    def params(self):
        raise NotImplementedError()

    def returns(self):
        raise NotImplementedError()



