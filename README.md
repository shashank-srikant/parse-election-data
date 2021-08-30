# parse-election-data

Thanks to [Pushpendre](https://github.com/se4u) for setting this up.

## Instructions
 **pyenv**: First install `pyenv`. See their webpage for clear instructions on how to do so. [Pyenv webpage](https://github.com/pyenv/pyenv/#installation)

 Make sure the environment variables are correctly set up.

 - Once installed, run to install and select `Python 3.9.0`
 ```
 $ pyenv install 3.9.0
 $ pyenv global 3.9.0
 ```

 *Note* - The above installation should have also installed `pyenv virtualenv` package.

 This helps create virtual environments to load different packages into.

 - Create a virtual environment called `code-quality` which runs Python 3.9.0.
 ```
 $ pyenv virtualenv election-data
 $ pyenv activate election-data
 ```

 - Install the requirements via pip within `election-data`.
```
$ pip install -r ./scripts/requirements.txt
```

 - To run the script to parse the PDF into image cards
 ```
 $ python parse.py /path/to/folder/containing/pdfs /path/to/folder/in/which/to/dump/card/jpegs
```

- To convert the image cards into text
```
 $ cd /path/to/folder/in/which/to/dump/card/jpegs
 $ for e in *.jpeg ; do echo  $e ${e%jpeg}  --psm 6 2>/dev/null ; done | head | xargs -P 8 -n 1 echo tesseract
 ```

 - To convert the parsed text into a CSV
 ```
 python generate_csv.py /path/to/folder/having/txt/files /path/to/dump/csv
 ```
