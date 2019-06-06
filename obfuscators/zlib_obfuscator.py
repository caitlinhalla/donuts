from obfuscators.obfuscator import Obfuscator
import zlib


class ZlibObfuscator(Obfuscator):
    @property
    def name(self):
        return "zlib"

    def obfuscate(self, contents):
        return zlib.compress(contents)

    def generate_deobfuscator(self, variable_name):
        return f"{variable_name} = zlib.decompress({variable_name})\n"

    def generate_imports(self):
        return "import zlib\n"
