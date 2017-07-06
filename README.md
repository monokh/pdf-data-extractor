# PDF Data Extractor

A python3 module that parses data from PDF files given a config with a set of rules

## Installation

This module is not available on PyPi yet so installation is only possible from this repository:

    pip install git+git://github.com/monokh/pdf-data-extractor.git

## Usage

The module expects a `config.yml` file.

The config yml file must have a `fields` object and under that any number of data fields to be extracted from the PDF file. 

```
fields:
  name:
    find:
      type: pageNumber
      value: 0
    extract:
      type: pattern
      value: (?<=My name is )(.*?)(?=.)
  address:
    find:
     type: pagePattern
     value: "Person Details"
    extract:
      type: pattern
      value: (?<=Address: )(.*?)(?=Gender)
```

Use within code like so:

```
from PDFDataExtractor.extractor import PDFDataExtractor
import json

extractor = PDFDataExtractor('file.pdf', 'config.yml')
data = extractor.get_data()
print(json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True))
```

```
{
    'name': 'Bob',
    'address': '622 Cedar Ave'
}
```

## Fields

A field object must have a `find` and `extract` defined. 

### find 

`find` defines a rule which is used to find the page which the data is on. Valid types are `pageNumber` and `pagePattern`.

`pageNumber`: The page number to find the data on - begins at 0
```
find:
  type: pageNumber
  value: 1
```

`pagePattern`: A regex matching the desired page
```
find:
  type: pagePattern
  value: "Person Details"
```

### extract

`extract` defines the rule that is used to extract the desired data. The only current option is `pattern`. This is a regex pattern with group 1 matching the desired value to be extracted.

```
extract:
  type: pattern
  value: (?<=Address: )(.*?)(?=Gender)
```
