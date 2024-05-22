import difflib

def print_diff(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        text1 = f1.readlines()
        text2 = f2.readlines()
        
    diff = difflib.unified_diff(text1, text2, lineterm='')
    print('\n'.join(diff))
file1 = "max.hack"
file2 = "06/pong/Pong.hack"
print_diff(file1, file2)
