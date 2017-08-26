import os

#path = os.path.expanduser('~')
path = os.path.expandvars('$HOME')

for root, folders, files in os.walk(path):
    if '.git' in folders:
        print(root)
