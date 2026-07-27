# CHBH CLI Tool for neuroimagers.

To use the tool download the repo and place the files in the directory you wish to start your project.

## Installing tool
(Making it executable)

```bash
bash ./chbh install
```


## Setting up an MEG environment

```bash
chbh meeg
```

This will create a uv environment with the core packages used in MEG analysis, to get you up and running fast. 


## Full Usage

```bash
Usage:
  chbh <group> [group ...]

Available groups:
  meeg
  mri
  sleep
  dev

Examples:

  chbh meeg
  chbh mri
  chbh meeg mri
  chbh meeg sleep
  chbh meeg mri sleep
  chbh meeg mri dev
```
