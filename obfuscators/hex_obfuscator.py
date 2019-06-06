from obfuscators.obfuscator import Obfuscator


class HexObfuscator(Obfuscator):
    OBFUSCATOR_NAME = "hex"

    def obfuscate(self, contents):

        for i in range(len(contents)):
            contents[i] ^= 0x55

        return contents

    def generate_deobfuscator(self, variable_name):
        return f"{variable_name} = for i in range(len({variable_name})): {variable_name}[x] ^= 0x55\n"

    def generate_imports(self):
        return ""
