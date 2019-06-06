from obfuscators.obfuscator import Obfuscator
import base64


class Base64Obfuscator(Obfuscator):
    @property
    def name(self):
        return "base64"

    def obfuscate(self, contents):
        return base64.b64encode(contents)

    def generate_deobfuscator(self, variable_name):
        return f"{variable_name} = base64.b64decode({variable_name})\n"

    def generate_imports(self):
        return "import base64\n"
