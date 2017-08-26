### gits-find.py

Use `walk()` to find all folders with subfolder `.git`.

### gits-status.py

Use `walk()` to find all folders with subfolder `.git` and execute `git status --short` and count modified files.

### mr.py

Based on [mu_repo](http://fabioz.github.io/mu-repo/) (python) and [gr](http://mixu.net/gr/) (npm).

(`gr` uses colors but checks only 5 level deep subfolders.)

Required: colorama (`pip install colorama`)
    
It can use `~/.mu_repo` if you have `mu_repo` already installed (`pip install mu_repo`)


    mr.py find 
    mr.py ls
    mr.py sh CMD
    mr.py sh "CMD1|CMD2"
    
    mr.py --regex PATTERN ls
    mr.py --regex PATTERN sh CMD
    
    ex. mr.py --regex python ls
    
    mr.py --fnmatch PATTERN ls
    mr.py --fnmatch PATTERN sh CMD
    
    ex. mr.py --regex python* ls
    ex. mr.py --regex *python ls
    
