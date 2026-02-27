```text
                                                                                             ___
                ,--,                                                                ,--,   ,--.'|_
         .---.,--.'|                  ,---,             __  ,-.                   ,--.'|   |  | :,'
        /. ./||  |,               ,-+-. /  |          ,' ,'/ /|          ,----._,.|  |,    :  : ' :
     .-'-. ' |`--'_       ,---.  ,--.'|'   |   ,---.  '  | |' |         /   /  ' /`--'_  .;__,'  /
    /___/ \: |,' ,'|     /     \|   |  ,"' |  /     \ |  |   ,'        |   :     |,' ,'| |  |   |
 .-'.. '   ' .'  | |    /    /  |   | /  | | /    /  |'  :  /          |   | .\  .'  | | :__,'| :
/___/ \:     '|  | :   .    ' / |   | |  | |.    ' / ||  | '           .   ; ';  ||  | :   '  : |__
.   \  ' .\   '  : |__ '   ;   /|   | |  |/ '   ;   /|;  : |           '   .   . |'  : |__ |  | '.'|
 \   \   ' \ ||  | '.'|'   |  / |   | |--'  '   |  / ||  , ;            `---`-'| ||  | '.'|;  :    ;
  \   \  |--" ;  :    ;|   :    |   |/      |   :    | ---'             .'__/\_: |;  :    ;|  ,   /
   \   \ |    |  ,   /  \   \  /'---'        \   \  /                   |   :    :|  ,   /  ---`-'
    '---"      ---`-'    `----'               `----'                     \   \  /  ---`-'
                                                                          `--`-'
```

# wiener-git

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/python-3.12-blue.svg" alt="Python Version">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  </a>
  <img src="https://img.shields.io/badge/build-passing-brightgreen.svg" alt="Build Status">
</p>

# WHat is this?

this is a tiny side project from me to show educate myself a little of python programming. It is nothing fancy and its not designed to be used as an alternative to git. its just one of the probably millions of existing clones of those big tools written in python.
the last thing i want to this project its a bunch of ai slop taking part of it so that is what it is for.
Also although this is kind of a proffessional focused project. I like to be something like myself. so if you dont want to read the source and you happen to like my personality. you can also read along the [yap.md](/src/yap.md) to see what im struggling on bit by bit.

---

## what does this have?

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [License](#license)

---

## Overview

This project is a personal exploration of Git's architecture. Instead of just using `git add` and `git commit`, we're building the mechanisms that make them possible:

- **Content Addressable Storage:** Understanding how Git uses SHA-1 hashes to store objects.
- **The Object System:** Implementing Blobs, Trees, and Commits.
- **The Repository:** Managing the `.git` directory structure and configuration.

> "I ask to myself i need to understand github. So my unemployed ass decided. herm why should i see a 4 hours youtube course to keep knowing shit?" — _From the project notes._

_Inspired by [Write Yourself a Git](https://wyag.thb.lt/)._
_also used_ [Py-git](https://youtu.be/g2cfjDENSyw?si=q7kx6qKwxQ-MZEFk)

---

## Features

- **Built from Scratch:** No high-level Git libraries, just pure Python and standard modules.
- **Educational First:** Highly documented code (and journals) explaining every step of the way.
- **Unix Optimized:** Designed for Unix environments (Linux/macOS), following the philosophy of the original Git.

---

## Installation

### Prerequisites

- **Python 3.12+**
- **Unix-based system** (Linux/macOS). WSL2 is recommended for Windows users.

### Setup

1. **Clone the repository:**

```bash
   git clone https://github.com/your-username/wiener-git.git
   cd wiener-git
```

1. **Environment Setup:**
   If you use [mise](https://mise.jdx.dev/), the environment will be set up automatically:

   ```bash
   mise install
   ```

   Otherwise, create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

---

## Usage

The project is currently in the development phase. The core library lives in `src/libwyag.py`.

### Initializing a Repository

To create a new `wiener-git` repository:

```bash
python src/libwyag.py init
```

_Note: Commands are being actively implemented. Check [src/libwyag.py](src/libwyag.py) for the current status of command support._

---

## Project Structure

- `src/libwyag.py`: The core logic of the Git implementation.
- `src/yap.md`: **"Yet Another Post"** - A personal journal and documentation of the coding journey.
- `mise.toml`: Tool version management and environment configuration.

---

## Roadmap

- [x] Repository initialization logic (`init`)
- [ ] Object hashing and storage
- [ ] Reading and writing Trees
- [ ] Commit history and Logging
- [ ] Status and Diffing

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">Everything is under the image of Wiener-hund studios which is not an official enterprise but is made from humans. should check out the repo</p>
