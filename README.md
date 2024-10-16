# tlfs

[![PyPI - Version](https://img.shields.io/pypi/v/tlfs.svg)](https://pypi.org/project/tlfs)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tlfs.svg)](https://pypi.org/project/tlfs)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install tlfs
```

## License

`tlfs` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Example usage
For some "standard" (opinionated) stuff you could do the following
(which is what is done in the [web version on streamlit](https://webtlfs.streamlit.app/)):
``` python
tlf = TLF("Test")
tlf.from_xlsx("path-to-your.xlsx")
tlf
tlf.to_docx("path-to-your.docx")
```
For custom stuff do program by hand

``` python

# overloading * Quant/Quali/Itemset to create Tables quickly
age = Quant("Age")
sex = Quali("Sex", groups = ["M", "F"])
trt = Quali("Treatment", groups = ["EXP", "CTRL"])
prices = Itemset("Unit costs",
                 items = ["Dentist", "Hospice", "Blood test"],
                 contents = ["unit cost", "per", "source"])
nation = Quali("Nation", groups = ["UK", "ITA"])

age * trt
[var * trt for var in [age, sex]] + [prices * nation]


# Changing display default in a table
age2 = Quant("Age", display = ["median", "25pct", "75pct"], unit = 'years')
age3 = Quant("Age", display = "median (iqr)", cell_content = "xx (xx - xx)")
sex2 = Quali("Sex", groups = ["M", "F"], display = "n", cell_content = "x")


univ = Section("Univariate tables", [Table(age), Table(sex)])
changed_def = Section("Some changed defaults", [Table(age2), age2 * trt, age3 * trt, Table(sex2)])
listings = Section("Listings", [Table(prices), prices * nation])
tlf2 = TLF("Table, Listings, Figure examples", [univ, biv, changed_def, listings])
tlf.to_doc("whatever.docx")
```


## TODO
- overload + in `Table` to stack them
- overload + in `Sections` to concatenate them
- just do `Section("Univariate tables", [age, sex])` instead of 
  `Section("Univariate tables", [Table(age), Table(sex)])`

