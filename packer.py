import argparse
import zlib
import base64
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


class ZlibObfuscator(Obfuscator):
    def obfuscate(self, contents):
        return zlib.compress(contents)

    def generate_deobfuscator(self, variable_name):
        return f"{variable_name} = zlib.decompress({variable_name})\n"

    def generate_imports(self):
        return "import zlib\n"


class Base64Obfuscator(Obfuscator):
    def obfuscate(self, contents):
        return base64.b64encode(contents)

    def generate_deobfuscator(self, variable_name):
        return f"{variable_name} = base64.b64decode({variable_name})\n"

    def generate_imports(self):
        return "import base64\n"


class XorObfuscator(Obfuscator):
    def obfuscate(self, contents):

        for i in range(len(contents)):
            contents[i] ^= 0x55

        return contents

    def generate_deobfuscator(self, variable_name):
        return f"{variable_name} = for i in range(len({variable_name})): {variable_name}[x] ^= 0x55\n"

    def generate_imports(self):
        return ""


obfuscators = {
    "base64": Base64Obfuscator(),
    "zlib": ZlibObfuscator(),
    "xor": XorObfuscator()
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-if', '--inputFilepath',
                        help='Specify an input file path name', dest='inputFilepath', required=True)
    parser.add_argument('-of', '--outputFilepath',
                        help='Specify an output file path name', dest='outputFilepath', required=True)

    return parser.parse_args()


def main():
    args = parse_args()
    write_file(args.inputFilepath, args.outputFilepath)


obfuscator_list = ["base64", "zlib", "base64"]


def write_file(inputFilepath, outputFilepath):
    with open(inputFilepath, "rb") as file1:
        with open(outputFilepath, 'w') as file2:
            contents = file1.read()

            for x in obfuscator_list:
                contents = obfuscators[x].obfuscate(contents)
                file2.write(obfuscators[x].generate_imports())

            file2.write("var_1 = '''")
            file2.write(contents.decode('ascii'))
            file2.write("'''\n")

            for x in obfuscator_list:
                file2.write(obfuscators[x].generate_deobfuscator("var_1"))

            file2.write("exec(var_1)")


if __name__ == "__main__":
    main()
