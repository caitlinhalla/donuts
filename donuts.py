import argparse

def parse_args():
   parser = argparse.ArgumentParser()
   parser.add_argument('-p', '--filepath', help='Specify a file path', dest='filepath', required=True)
   #parser.add_argument('-v', '--version', help='Specify the target upgrade version of .NET Core.', dest='version', required=True, choices=['2.0', '2.1'])

   return parser.parse_args()

def main():
   args = parse_args()
   write_file(args.filepath)

def write_file(filepath):
    with open(filepath) as file1:
      with open('file2.txt', 'w') as file2:
         contents = file1.read()
         file2.write(contents)

if __name__ == "__main__":
    main()