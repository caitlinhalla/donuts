from abc import ABC, abstractmethod


class Obfuscator(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def obfuscate(self, contents):
        pass

    @abstractmethod
    def generate_deobfuscator(self, contents):
        pass

    @abstractmethod
    def generate_imports(self):
        pass
