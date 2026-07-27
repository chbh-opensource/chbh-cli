# CHBH CLI Tool for neuroimagers.

To use the tool download the repo and place the files in the directory you wish to start your project.

## Installing tool
This will download the script and making it executable from anywhere in your terminal.

```bash
git clone https://github.com/chbh-opensource/chbh-cli.git
cd chbh-cli
bash ./chbh install
```


## Setting up an MEG environment

You can create new python environments using the `chbh` command. This will copy a template `pyproject.toml` file into your working directory and initialise a new virtual environment with a range of common tools installed in it.


```bash
cd /path/to/my/working/directory
chbh meeg
source .venv/bin/activate
```

This works using UV, and can be further customised after install using `uv add` [full docs here](https://docs.astral.sh/uv/reference/cli/#uv-add).

For example, if we want to include `seaborn`.

```bash
uv add seaborn
```

The package will be added to the virtual environment and the dependencies syncronised.



## Full Usage

```bash
CHBH environment manager

Usage:
  chbh install
      Install the chbh command and environment template.

  chbh version
      Show the version of the installed CHBH environment templates.

  chbh base_module
      Load the standard BlueBEAR modules required for CHBH
      Python environments.

  chbh <group> [group ...]
      Create/update a UV environment in the current directory
      using one or more dependency groups.

Available groups:
  meeg     EEG, MEG and electrophysiology tools
  mri      MRI and neuroimaging tools
  sleep    Sleep analysis tools
  dev      Development and code-quality tools

Examples:
  chbh meeg
      Create a MEEG environment.

  chbh mri
      Create an MRI environment.

  chbh meeg mri
      Create an environment with both MEEG and MRI tools.

  chbh meeg sleep
      Create an electrophysiology and sleep-analysis environment.

  chbh meeg mri sleep dev
      Install all currently available CHBH groups.

Notes:
  - A .venv is created in the current working directory.
  - If no pyproject.toml exists, the CHBH template will be copied
    into the current directory.
  - Existing pyproject.toml files are preserved and will be used
    instead of the CHBH template.
  - After installation, activate the environment with:

        source .venv/bin/activate
```
