# Finnish SQuAD2.0

This repository contains the code for the experiment to translate the English
SQuAD2.0 to Finnish (or other languages).

## 1. Download and convert original SQuAD2.0 to docx

Download the original SQuAD2.0
[train](https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json) and
[dev](https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v2.0.json) files
and put them into the `squad2-en/` folder. Then run the script to convert them from
`.json` to `.docx` (`pip install -r requirements.txt` first if needed):

```
python3 squad2doc.py squad2-en/dev-v2.0.json squad2-en/train-v2.0.json
```

This will create a bunch of `.docx` files that respect the size limit of the
DeepL translation service and a `meta.jsonl` file that contains the information
to map the answers to the questions after translating the `.docx` files.

## 2. Run the .docx files through DeepL

Feed the `.docx` files to [DeepL](https://www.deepl.com/translator) and save the
translated files into the `squad2-fi-raw/` folder.

## 3. Convert the .docx files to html

Html files are easier to parse with Python so it makes sense to convert the
`.docx` files to html.

Easy way to do this is with something like LibreOffice:

```bash
for FILE in squad2-fi-raw/*.docx ; do libreoffice --convert-to html --outdir squad2-fi-raw/html "$FILE" ; done

```

## 4. Create a Finnish SQuAD2.0 dataset from those html files

The last step is to parse the html files to create the final Finnish JSON files:
(this will take a while)

```
python3 html2squad.py
```

The final dataset is then created into the `squad2_fi/` folder.
