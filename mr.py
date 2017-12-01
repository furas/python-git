#!/usr/bin/env python3

import sys
import os
import colorama as C
import json
import fnmatch
import re
import subprocess
import argparse

def find_repos(path, sort=True, regex=None, fnmatch=None):
    '''
    find all folders with .git subfolder 
    and filter using regex or fnmatch
    '''

    path = os.path.realpath(path)
    repos = []
    
    for root, folders, files in os.walk(path):
        if '.git' in folders:
            repos.append(root)

    if sort:
        repos.sort()
        
    if regex:
        repos = filter_regex(repos, regex)
    elif fnmatch:
        repos = filter_fnmatch(repos, fnmatch)
    
    return repos

def filter_regex(repos, pattern):
    '''
    filter list of repos using regex
    '''
    return filter(lambda x:re.search(pattern, x), repos)

def filter_fnmatch(repos, pattern):
    '''
    filter list of repos using filename match
    '''
    return fnmatch.filter(repos, pattern)

def display(repos):
    '''
    display list of repos using colors 
    '''
    for repo in repos:
        pos = repo.rfind('/')+1    
        print(C.Fore.LIGHTBLACK_EX, repo[:pos], C.Fore.WHITE, repo[pos:], sep='')

def save(cfg, filename='~/.config/mr.cfg'):
    '''
    save list of repos in '~/.config/mr.cfg' as JSON
    '''
    
    filename = os.path.expanduser(filename)
    with open(filename, 'w') as f:
        json.dump(list(cfg), f)

def load(filename='~/.config/mr.cfg'):
    '''
    load list of repos from '~/.config/mr.cfg' as JSON
    '''
    filename = os.path.expanduser(filename)
    with open(filename, 'r') as f:
        return json.load(f)

# ---------------------------------------------------------------------

parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(dest='command')
parser.add_argument('-d', '--debug', action='store_true', help='display extra information')

parser.add_argument('-r', '--regex', help='filter repos using regex (no need //) (ie. ".*python.*")')
parser.add_argument('-m', '--fnmatch', help='filter repos using fnmatch (?,*) (ie. "*python*")')

parser.add_argument('-l', '--load', default='~/.config/mr.cfg', help='load from file (default ~/.config/mr.cfg)')
parser.add_argument('--mu', action='store_true', help='load repos from mu_repo config') , 
parser.add_argument('--mu-cfg', default='~/.mu_repo', help='load repos from mu_repo (default: ~/.mu_repo)')

subparser_find = subparsers.add_parser('find', help='find repos on disk')
subparser_find.add_argument('folder', nargs='?', default='~/', help='starting folder (default ~ [user home folder])')
subparser_find.add_argument('-s', '--save', default='~/.config/mr.cfg', help='save in file (default ~/.config/mr.cfg)')

subparser_ls = subparsers.add_parser('ls', help='list repos')

subparser_st = subparsers.add_parser('st', help='list status - count modified files')
subparser_st.add_argument('-m', '--modified', action='store_true', help='show only with modified files')
subparser_st.add_argument('-o', '--other', action='store_true', help='show only not modified files')
subparser_st.add_argument('-c', '--count', action='store_true', help='show only count')

subparser_sh = subparsers.add_parser('sh', help='shell command')
subparser_sh.add_argument('CMD', help='use mu_repo', default='')

subparser_git = subparsers.add_parser('git', help='list status - count modified files')
subparser_git.add_argument('ARGS', nargs=argparse.REMAINDER, help='execute git')

argument = parser.parse_args(sys.argv[1:])


if argument.debug:
    print(argument, '\n')


if argument.command == 'mu':
    import mu_repo as mr
    repos = mr.CreateConfig(os.path.expanduser('~/.mu_repo'))
else:   
    repos = load(argument.load)


if argument.regex:
    repos = filter_regex(repos, argument.regex)
elif argument.fnmatch:
    repos = filter_fnmatch(repos, argument.fnmatch)


if argument.command == 'find':
    repos = find_repos(os.path.expanduser(argument.folder), argument.regex, argument.fnmatch)
    
    if argument.save:
        save(repos, argument.save)
        
    display(repos)

elif argument.command == 'ls':
    display(repos)

elif argument.command == 'st':
    argument.CMD = 'git status --short'
    command = argument.CMD.split()
        
    for repo in repos:

        try:
            os.chdir(repo)
        except FileNotFoundError:
            pos = repo.rfind('/')+1    
            print(C.Fore.RED, "Folder doesn't exist: ", C.Fore.LIGHTBLACK_EX, repo[:pos], C.Fore.WHITE, repo[pos:], sep='')
            continue
            
        process = subprocess.run(command, check=True, stdout=subprocess.PIPE)
        result = process.stdout.decode('utf-8')
        
        if result:
            value = len(result.strip().split('\n'))
        else:
            value = 0
        
        if argument.modified and value == 0:
            continue
            
        if argument.other and value != 0:
            continue

        pos = repo.rfind('/')+1    
        print(C.Fore.LIGHTBLACK_EX, repo[:pos], C.Fore.WHITE, repo[pos:], sep='', end=' ')

        if value == 0:
            color = C.Fore.GREEN
        else: 
            color = C.Fore.RED

        if argument.count:
            print(color, value, sep='')
        else:
            print()
            print(color, result, sep='')
    
elif argument.command == 'git': 
    
    command = ['git']
    
    if argument.ARGS:
        command += argument.ARGS

    for repo in repos:
        
        try:
            os.chdir(repo)
        except FileNotFoundError:
            pos = repo.rfind('/')+1    
            print(C.Fore.RED, "Folder doesn't exist: ", C.Fore.LIGHTBLACK_EX, repo[:pos], C.Fore.WHITE, repo[pos:], sep='')
            continue
                    
        pos = repo.rfind('/')+1    
        print(C.Fore.LIGHTBLACK_EX, repo[:pos], C.Fore.WHITE, repo[pos:], sep='')

        process = subprocess.run(command, check=True, stdout=subprocess.PIPE)
        result = process.stdout.decode('utf-8')#.strip()

        print(result)
    
elif argument.command == 'sh': 
    for repo in repos:

        try:
            os.chdir(repo)
        except FileNotFoundError:
            pos = repo.rfind('/')+1    
            print(C.Fore.RED, "Folder doesn't exist: ", C.Fore.LIGHTBLACK_EX, repo[:pos], C.Fore.WHITE, repo[pos:], sep='')
            continue
                    
        pos = repo.rfind('/')+1    
        print(C.Fore.LIGHTBLACK_EX, repo[:pos], C.Fore.WHITE, repo[pos:], sep='')
        
        data = None
        process = None
        for command in argument.CMD.split('|'):
            command = command.split()
            previous = process
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=data)
            data = process.stdout
            #previous.close()
        result = process.communicate()[0].decode('utf-8').strip()
        print(result)
else:
    parser.print_help()
