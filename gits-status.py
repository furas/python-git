import os
import subprocess

#path = os.path.expanduser('~')
path = os.path.expandvars('$HOME')

cmd = 'git status --short'
#cmd = 'git status --porcelain'

cmd = cmd.split()

for root, folders, files in os.walk(path):
    if '.git' in folders:
        print(root)
        os.chdir(root)
        s = subprocess.run(cmd, check=True, stdout=subprocess.PIPE)
        print('modified:', len(s.stdout), '\n')   
