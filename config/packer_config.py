class PackerConfig:
    def __init__(self, args):
        self.input_filepath = args.input_filepath
        self.output_filepath = args.output_filepath
        self.variable_name = args.variable_name
        self.obfuscator_list = args.obfuscator_list
