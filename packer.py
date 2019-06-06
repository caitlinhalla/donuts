import os
import argparse
from config.packer_config import PackerConfig
import glob
import importlib
import inspect
from obfuscators.obfuscator import Obfuscator


def parse_args(menu):
    parser = argparse.ArgumentParser()
    parser.add_argument('-if', '--inputFilepath',
                        help='Specify an input file path name', dest='input_filepath', required=True)
    parser.add_argument('-of', '--outputFilepath',
                        help='Specify an output file path name', dest='output_filepath', required=True)
    parser.add_argument('-var', '--variable_name',
                        help='Name of the variable into which the packed script will be stored', dest='variable_name', default="x")

    parser.add_argument('-obs', '--obfuscators', choices=menu.keys(),
                        help='Obfuscators used to pack script', dest='obfuscator_list', nargs="+", required=True)

    return parser.parse_args()


def main():
    obfuscator_filenames = get_obfuscator_file_names()
    instantiated_obfuscator_classes = import_modules(obfuscator_filenames)

    menu = generate_obfuscator_menu(instantiated_obfuscator_classes)

    args = parse_args(menu)

    configuration = PackerConfig(args)
    write_file(configuration, menu)


def generate_obfuscator_menu(instantiated_obfuscator_classes):
    return dict((item.name, item)
                for item in instantiated_obfuscator_classes)


def import_modules(obfuscator_filenames):
    instantiated_class_list = []
    for obfuscator in obfuscator_filenames:
        module = importlib.import_module(f'obfuscators.{obfuscator}')
        class_members = inspect.getmembers(module, inspect.isclass)
        for member in class_members:
            abstract = inspect.isabstract(member[1])
            if abstract:
                continue
            instance = isinstance(member[1](), Obfuscator)
            if instance:
                instantiated_class_list.append(member[1]())
    return instantiated_class_list


def get_obfuscator_file_names():
    obfuscators = []
    for obfuscator in glob.glob("./obfuscators/*_obfuscator.py"):
        base_name = os.path.basename(obfuscator)
        file_name = os.path.splitext(base_name)[0]
        obfuscators.append(file_name)
    return obfuscators


def write_file(configuration, menu):
    with open(configuration.input_filepath, "rb") as file1:
        with open(configuration.output_filepath, 'w') as file2:
            contents = file1.read()

            for x in set(configuration.obfuscator_list):
                file2.write(menu[x].generate_imports())

            for x in configuration.obfuscator_list:
                contents = menu[x].obfuscate(contents)

            file2.write(
                f"{configuration.variable_name}= '''{contents.decode('ascii')}'''\n")

            for x in configuration.obfuscator_list:
                file2.write(menu[x].generate_deobfuscator(
                    f"{configuration.variable_name}"))

            file2.write(f"exec({configuration.variable_name})")


if __name__ == "__main__":
    main()
