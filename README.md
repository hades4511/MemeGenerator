Meme Generator
===============

This is a project for 'Python Intermediate Nano Degree' that generates memes by using a collection of images and quotes.

## How to build project
This project was built using python 3.9, so after cloning this project, make sure to create and activate a virtual environment for python 3.9. After this, run command:

* install requirements
```shell
pip install -r requirements.txt
```

* Check test cases
```shell
python -m unittest
```

* Run using command line
```shell
python meme.py --body="To bork or not to bork" --author="Some dog" --path="{{image_path}}"
```

* Run Flask server using
```shell
python app.py
```

## Roles and responsibilities

1. Quote Engine: This module is responsible for parsing quotes from files with the following four formats:
   * .txt
   * .pdf
   * .docx
   * .csv
2. Meme Engine: This module is responsible for generating a meme by using quote data and image path. It writes quote on the image and saves it in provided path.
3. meme.py: This file parses commands from command line and generate a meme accordingly.
4. app.py: This file contains code for flask app that either generates a random meme or generate a meme by taking user's parameters from a HTML form.
