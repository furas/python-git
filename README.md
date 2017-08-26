### gits-find.py

Use `walk()` to find all folders with subfolder `.git`.

### gits-status.py

Use `walk()` to find all folders with subfolder `.git` and execute `git status --short` and count modified files.

### mr.py

Based on [mu_repo](http://fabioz.github.io/mu-repo/) (python) and [gr](http://mixu.net/gr/) (npm).

(`gr` uses colors but checks only 5 level deep subfolders.)

Required: colorama (`pip install colorama`)
    
It can use `~/.mu_repo` if you have `mu_repo` already installed (`pip install mu_repo`)


Normal command

    mr.py find  # find all repos in ~ ($HOME) folder and save in ~/.config/.mr.cfg
    mr.py ls    # list all repos from ~/.config/.mr.cfg
    
    # count modified files in every repos (similar to `git status --short | wc -l` or `gr st`)    
    
    mr.py st    
    mr.py st -a  # show only with midified files
    mr.py st -b  # show only without midified files
    
    
Shell command (with parenthesis if piping or space)    

    mr.py sh CMD
    mr.py sh "CMD ARGS"
    mr.py sh "CMD1|CMD2"
    
    ex. 
    
    mr.py sh ls
    mr.py sh "ls -al"
    mr.py sh "git status --short | wc -l"

Git command (no need parenthesis, but can't use piping)

    mr.py git ARGS
    
    ex.
    
    mr.py git status --short
    
Using regex or filename match (have to be before command)

    mr.py --regex PATTERN ls
    mr.py --regex PATTERN sh CMD
    
    mr.py --fnmatch PATTERN ls
    mr.py --fnmatch PATTERN sh CMD

    ex. 
    
    mr.py --regex python ls
    mr.py --regex python$ st
    mr.py --regex ^python sh "ls -al"
    mr.py --regex ^python sh "cat .git/config"
    
    mr.py --fnmatch python* ls
    mr.py --fnmatch *python ls
    
    mr.py --fnmatch python* sh "ls -al"
    mr.py --fnmatch *python sh "ls -al"
    
    mr.py --fnmatch python* sh "git status --short"
    mr.py --fnmatch *python sh "git status --short"

