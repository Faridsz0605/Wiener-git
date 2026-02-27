# what is this?

<!--toc:start-->

- [what is this?](#what-is-this)
  - [but for real ?](#but-for-real)
  - [Ill build it from scratch](#ill-build-it-from-scratch)
  - [Getting started](#getting-started)
  <!--toc:end-->

> [!NOTE]
> this sort of article/ readme its literally me narrating the journey of coding this. im not a software dev. yet. if you want the artile to follow along im begging you go to ->[here](https://wyag.thb.lt/)

If you ask me. ill genuately tell you i have no fucking clue. Check the one who knoks at -> [here](https://wyag.thb.lt/)

## but for real ?

Yes. I ask to myself i need to understand github. So my unemployed ass decided. herm why should i see a 4 hours youtube course to keep knowing shit?

## Ill build it from scratch

So this is my version as a computer rat. on python. lowkenuetly i wanted to write it on C and then on rust.
But actually i dont know shit. Im from Colombia and i just want to contribute and document my trip so this is me getting started.

## Getting started

As i waid earlier you whould go to the one who write this (and literally knows) [here](https://wyag.thb.lt/)
But if i repeated that 2 times and you still here maybe i can help with something or you just a lazy head dont want to go to a strange link. which i get it.

\*\*> [!IMPORTANT]

> Im hosting this on an unix system which is required by using the `wyag` thing. as executable, i have no idea how to set this up on window. probably will work normally on WSL hich is a default shell on windows but you know how papa gates love to peek our buts when trying to check out some software.

## import libraries

Now we are talking. the header of the `libwyag.py` file would be long... at least for a junior (me) so we must import necesary libraries as follows ->

```python
import argparse
import configparser
from datetime import datetime
from fnmatch import fnmatch
import hashlib
from math import ceil
import os
import re
import sys
import zlib


try:
  import grp , pwd
except ModuleNotFoundError:
  pass
```

the header of yout `main.py` or whatever you called the file must have them ill explain a little further.

### the CLI libraries

as you (and every one) should know git is a CLI (command line interface) so we need python to parce argument straight from comand-line so [argparse](https://docs.python.org/3/library/argparse.html) would be our best friend as itll do 99% of the work as our friend [Thibault Polge](thibault@thb.lt) tells us on the document (this project is based of). thats why we import ->

```python
import argparse
import configparser # <- to read and write files with Microsoft INI format
```

Also we will need some time manipulation

```python
from datetime import datetime
```

The following comand is for unix like system ->

```python
try:
  import grp, pwd
except ModuleNotFoundError:
  pass
```

what happen there is we try to import groups and pwd (print working directory) if not possible return `ModuleNotFoundError` then pass.

### some git implementation necessary modules

to create and support file matching on patterns like `.gitignore` we inport `fnmatch`

```python
from fnmatch import fnmatch
#hashing support (as git uses SHA-1)
import hashlib
```

and here some extra libraries to use ->

```python
from math import ceil
import possible
import re
import sys
import zlib
```

I know this is a nightmare for non-juniors reading this. But you literally saw the way i write this `article` from the begining and keep on reading so you genuately either interested or hate me in which cases im totally fine.

## junior survived importing packages :D

yes i'm 100 lines and still haven't code nothing... that says more about me that anything about the blog im reading this of. but i like to be as user friendly as possible, now internet information has no personality due to AI slop, thaths why im doing this so fucking chatgpt dont do some strange shit to my programs.

# Now the real code

first of we need to init a repository we cant build a castle from the rooftop. Now it needs some abstraction our `git` command would certaintly almost always target a repo to `init,config,checkout,delete` files.
as the author tells us a git is made of a `work tree` which is what is meant to be on version control and the `git directory` where git 'does its things' in my words. So those are the 'program files' and then its the 'work tree' which help us on version control. Now keeping that idea clear the regular worktree is a regular directory and the git directory is the child of the worktree `.git`.

> [!NOTE]
> git supports more operations than a worktree but we need to stick to basics, i mean you're programming on python. not a real men for now.

Now a repo is an object as on OOP (object oriented programming) if you are like me and dont know shit about that the way i could getting it its thinking as properties like videogame skills explained on [this](https://youtu.be/SI7O81GMG2A?si=8DCuJ1PLkWZP8EI6) video. so we must accomplish the following goals:

- we must check if the `.git` directory its created.
- Then the program must read some config file such as `.git/config` and check for a config variable author calls `core.repositoryformatversion` to be 0.

the contstuctor func would include the optional command `force` whcich disable checks.because the function `create_repo()` will use a `repo` object to create a repo (this part just blow me up) but we need to still be able to create a repo even within an invalid location.

```python

class GitRepo (object):
"""defines what is a repo"""
worktree = None
gitdir = None
conf = None #<- variables that define what a repo contains

def __init__(self, path, force=False): #args for the func
  self.worktree =path
  self.gitdir = os.path.join(path, ".git")

  if not(force or os.path.isdir(self.gitdir)):
    raise Exception(f"Not a git repo con {path}")#<- checks if on current path the `.git` exist if not and not force parameter. then error.

  self.conf =configparser.Configparser()
  cf = repo_file(self, "config")

    if cf and os.path.exist(cf):
      self.conf.read([cf])
    elif not force:
      raise Exception("No config file.")

    if not force:
      vers = int(self.conf.get("core", "repositoryformatversion"))
      if vers != 0:
      raise Exception(f"Unsupported repo format version on {vers}")

```

that class is just defining the logic of what is a repo on our git interpretation.

## I discovered something

i know i know all the above would be lost. but if you are as lost as i am you are goint to thank me as i learn more by literally imploding everything jajaj.
now everything is properly setted. but i didnt really wasnt understanding the written guide so the REAL men came in clutch check him out [here](https://youtu.be/g2cfjDENSyw?si=Bm-cpjJJ9pBITMLa)
now at this moment (27/feb/2026) i had to sort of start over because i was not really understanding the parsing but ill explain

we first check arguments to parse from the shell as users input defining global variables that will be used by our main program as follows ->

```python
parser =argparse.ArgumentParser(description="Describe your poroject here")
```

and then telling the program our command will support sub commands. I know i know. basic programming but you know im colombian and i have what is normally called (divine intellect) so yes. im basically a monkey but finded out whats important.
Then we defined what will happen when not arguments entered (basic logic)

```python
  if not args.command:
    parser.print_help()
    return
```

it might sound like i am very very stupid. But i didnt knew `args.command` uses `command` which we defined on the snippet `subparsers = parser.add_subparser(dest="command") #<- yes that command`
