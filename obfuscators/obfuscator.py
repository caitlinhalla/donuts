from abc import ABC, ABCMeta, abstractmethod


class Obfuscator(ABC):

    def __init__(self):
        super().__init__()

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def obfuscate(self, contents):
        pass

    @abstractmethod
    def generate_deobfuscator(self, contents):
        pass

    @abstractmethod
    def generate_imports(self):
        pass
