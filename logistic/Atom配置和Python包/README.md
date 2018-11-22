# Real time Python codes collaboration using Atom

This tutorial sets up the Atom Real time Python codes and configures Python Packages we'll be using in the project.

There are two documents you can use to install all the stuffs.

- atomsetup.bat
- pythonconfiguration.bat

## Guild line

1. Sign up for a GitHub Account
2. Download Atom IDE
3. Install relevant packages
   1. **teletype** https://teletype.atom.io/
   2. Script https://atom.io/packages/script
   3. autocomplete-python
   4. python-tools
   5. atom-python-run
4. Python Configurations

## Step by step

### Step 1. Sign up for GitHub

Go to https://github.com/, and opt-in with your email.

### Step 2. Download Atom

Atom could be downloaded here https://atom.io/ for Mac and for Windows.

### Step 3. Install Relevant Packages

Three simple ways you can do this. 

**One** is just click the document **atomsetup.bat** which is in the same folder as this tutorial. 



**Another way** is to open you Terminal (MacOS) or Command Prompt and type.

```shell
apm install teletype
apm install script
apm install autocomplete-python
apm install python-tools
apm install atom-python-run
```

This is exactly what is in the batch file.



Or, you can open atom package management, and install these packages.

Make sure you are able to run python in Atom. Open a Python Script in Atom and use **Ctrl+Shift+b** to run the script.

Teletype is the package that we'll use as real-time code viewer.

You are all set in Atom!

## Python Configurations

### Environment Set-up

Notice that this project will use Python 3.5+, so make sure you download the right version of Python, or just use the anaconda version. Virtual environments are not required but make sure you update all the packages to its latest version, especially for TensorFlow.

Also make sure you have put the right python into your system path and in Atom.

### Packages Management

To install packages I also prepared a shell document, you can click on that and it'll automatically do the stuff. The file is **pythonconfiguration.bat**

!! Notice if you use the script it'll automatically install CPU versions of TensorFlow.

Or you can do it manually, with the following packages required. You can use 

```shell
pip install pkg-name
```

to install all of the following packages. 

**Required Packages**

- Numpy, pandas
- Machine Learning
  - Sklearn
- Deep Learning
  - Keras
  - TensorFlow (GPU/CPU)
- Natural Language Process
  - Jieba