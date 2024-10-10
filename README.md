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
``` python
tlf = TLF("Test")
tlf.from_xlsx()
tlf
tlf.to_docx(view = True)


    
# for custom shit do program by hand
# ----------------------------------

# overloading can be useful: * in variables to create Tables
age = Quant("Age")
sex = Quali("Sex", groups = ["M", "F"])
trt = Quali("Treatment", groups = ["EXP", "CTRL"])
prices = Itemset("Unit costs",
                 items = ["Dentist", "Hospice", "Blood test"],
                 contents = ["unit cost", "per", "source"])
nation = Quali("Nation", groups = ["UK", "ITA"])

age * trt
[var * trt for var in [age, sex]] + [prices * nation]


# changing default example
age2 = Quant("Age", display = ["median", "25pct", "75pct"], unit = 'years')
age3 = Quant("Age", display = "median (iqr)", cell_content = "xx (xx - xx)")
sex2 = Quali("Sex", groups = ["M", "F"], display = "n", cell_content = "x")


univ = Section("Univariate tables", [Table(age), Table(sex)])
changed_def = Section("Some changed defaults", [Table(age2), age2 * trt, age3 * trt, Table(sex2)])
listings = Section("Listings", [Table(prices), prices * nation])
tlf2 = TLF("Table, Listings, Figure examples", [univ, biv, changed_def, listings])
tlf.to_doc()


# todo instead of
univ = Section("Univariate tables", [Table(age), Table(sex)])
# just do
univ = Section("Univariate tables", [age, sex])
```


## TODO
- overload + in `Table` to stack them
- overload + in `Sections` to concatenate them

