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


class ObfuscatorConfiguration:
    def __init__(self, args):
        self.input_filepath = args.input_filepath
        self.output_filepath = args.output_filepath
        self.variable_name = args.variable_name
        self.obfuscator_list = args.obfuscator_list


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-if', '--inputFilepath',
                        help='Specify an input file path name', dest='input_filepath', required=True)
    parser.add_argument('-of', '--outputFilepath',
                        help='Specify an output file path name', dest='output_filepath', required=True)
    parser.add_argument('-var', '--variable_name',
                        help='Name of the variable into which the packed script will be stored', dest='variable_name', default="x")

    parser.add_argument('-obs', '--obfuscators',
                        help='Obfuscators used to pack script', dest='obfuscator_list', nargs="+", required=True)

    return parser.parse_args()


def main():
    args = parse_args()
    configuration = ObfuscatorConfiguration(args)
    write_file(configuration)


def write_file(configuration):
    with open(configuration.input_filepath, "rb") as file1:
        with open(configuration.output_filepath, 'w') as file2:
            contents = file1.read()

            for x in set(configuration.obfuscator_list):
                file2.write(obfuscators[x].generate_imports())

            for x in configuration.obfuscator_list:
                contents = obfuscators[x].obfuscate(contents)

            file2.write(
                f"{configuration.variable_name}= '''{contents.decode('ascii')}'''\n")

            for x in configuration.obfuscator_list:
                file2.write(obfuscators[x].generate_deobfuscator(
                    f"{configuration.variable_name}"))

            file2.write(f"exec({configuration.variable_name})")


if __name__ == "__main__":
    main()
