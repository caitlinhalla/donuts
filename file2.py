var_1 = '''def write_file(filepath):
    with open(filepath) as file1:
      with open('file2.txt', 'w') as file2:
         contents = file1.read()
         file2.write(contents)'''
print(var_1)