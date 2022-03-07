<h1 align="center">
    Gittle
</h1>

<h4 align="center">
    A simple reimplementation of basic `git` commands
</h4>

This repo is to illustrate the following commands

 - `git add`
 - `git commit`
 - `git switch`
 - `git log`

## Usage

Move into a project repo and run `gittle init`.

```{bash}
> gittle init
Creating gittle repo at '/home/akhil/repos/gittle-project'
```

This will make a minimal `gittle` repo

```{bash}
> tree -a .gittle
.gittle
├── HEAD
└── store
```

Add some basic project files

```{bash}
mkdir src .hidden
echo "print('hi')" > src/__init__.py
echo "# I'm a hidden file" > .hidden/hidden.txt
echo "akhil:akhil@domain.com" > .names
```

Use `gittle add` to stage files

```{bash}
> gittle add
? Which files do you want to stage? (Use arrow keys to move, <space> to select, <a> to toggle, <i> to invert)
 » ○ .names
   ○ .hidden/hidden.txt
   ○ src/__init__.py
```

```{bash}
> gittle add
? Which files do you want to stage? done (2 selections)
Updated staging area
```

Run `gittle add` again to amend the staging area.

Use `gittle commit` to snapshot the repo state to the store

```{bash}
> gittle commit
Wrote the snapshot (commit) called '58bfd9f6' to the gittle store
```

Use `gittle cat-object` to explore the store

```{bash}
> gittle cat-object 6a008743
File:
src/__init__.py

Content:
print('hi')
```

```{bash}
> gittle cat-object 58bfd9f6
Parents:
Root commit

Hashes:
 - 6a008743
 - 9be66eb4
```