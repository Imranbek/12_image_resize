# Image Resizer

This script can resize your picture in the way you want it. Enjoy)

# How to Install

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
pip install -r requirements.txt # alternatively try pip3
```

Remember, it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) for better isolation.

# Quickstart

For start script you need to run the script in console/terminal.

```bash
$ python image_resuze.py 1.JPG -s 1
```

Also you can find full list of parameters by running:
```bash
$ python image_resuze.py -h
```

# Rules of logic
This script can't resize your image with entered combination of scale and size parameters. 
It can work only with just the scale parameter or with one or both of the width and height parameters.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
