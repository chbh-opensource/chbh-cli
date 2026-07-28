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
      Show the version of the installed CHBH environment template.

  chbh bear-modules
      Load the basic BlueBEAR modules recommended for Python by CHBH.

  chbh summarise-logs <log-directory>
      Summarise SLURM logs in the specified directory.
      This may install a python instance the first time it runs after install.

  chbh venv <group> [group ...]
      Create or update a UV environment in the current directory.

Available venv groups:
  meeg     EEG, MEG and electrophysiology tools
  mri      MRI and neuroimaging tools
  sleep    Sleep analysis tools
  dev      Development and code-quality tools

Examples:
  chbh install

  chbh version

  chbh bear-modules

  chbh summarise-logs ./logs

  chbh venv meeg

  chbh venv mri

  chbh venv meeg mri

  chbh venv meeg sleep

  chbh venv meeg mri sleep dev

Notes:
  - A .venv is created in the current working directory.
  - If no pyproject.toml exists, the CHBH template is copied into
    the current directory.
  - Existing pyproject.toml files are preserved and used as-is.
  - Activate the environment with:

        source .venv/bin/activate

```
