import pandas as pd

from dataclasses import dataclass, field
from multimethod import multimethod

    

def _def_quant_display():
    return ["n", "NA",
            "min", "25pct", "75pct", "max",
            "median", "iqr",
            "mean", "sd"]


@dataclass
class Quant:
    desc: str          # long variable description
    unit: str = None   # unit of measure
    min: float = None  # minimum
    max: float = None  # maximum
    display: list[str] = field(default_factory = _def_quant_display)
    cell_content: str = "x"  # default cell content (single number)

    def __post_init__(self):
        # normalize display so that user can specify a single string
        if type(self.display) is str:
            self.display = [self.display]
    
age  = Quant("Age")

@dataclass
class Quali:
    desc: str   # variable description
    groups: list[str]
    display: str = "n (col %)"
    cell_content: str = "x (x)"  # default cell content (single number)
    add_NA: bool = True
    add_tot: bool = True

    def __post_init__(self):
        # check quali has at least two groups
        if len(self.groups) < 2:
            raise Exception("At least two groups are required")
        # add NA and Tot to the group
        add_groups = ["NA"] * self.add_NA + ["Tot"] * self.add_tot
        self.actual_groups = self.groups + add_groups
        
sex = Quali("Sex", groups = ["M", "F"])
trt = Quali("Treatment", groups = ["EXP", "CTRL"])
        
@dataclass
class Table():
    x: Quant|Quali
    y: Quant|Quali|None = None # none if univariate
    
    def __post_init__(self):
        # check input
        if self.x is None:
            raise Exception("x cannot be None")
               
        # generate the pd.DataFrame representing the table
        self._make_df(self.x, self.y)


    def to_csv(self, f):
        self.df.to_csv(f, header = False, index = False)

    def add_to_docx(self):
        pass
        
    def _print_info(self):
        report = """
        caption = {0} (tabtype = {1}),
        header_nrows = {2}, nrows = {3},  ncols = {4}
        """.format(
            self.caption,
            self.tabtype,
            self.header_nrows,
            self.nrows,
            self.ncols)
        print(report)

        
    @multimethod
    def _make_df(self, a, b):
        print("boo")

    @_make_df.register
    def _make_df(self, a: Quant, b: None):
        # table infos
        self.tabtype = "univariate quant"
        self.caption = a.desc
        self.header_nrows = 1
        self.nrows = self.header_nrows + len(a.display)
        self.ncols = 2
        self._print_info()
        # table creation
        main_header = "{0} ({1})".format(a.desc, a.unit) if a.unit is not None else a.desc
        col1 = pd.Series([""] + a.display)
        col2 = pd.Series([main_header] + [a.cell_content]*len(a.display))
        self.df = pd.concat([col1, col2], axis = 1)
        print(self.df)
        
    @_make_df.register
    def _make_df(self, a: Quali, b: None):
        # table infos
        self.caption = a.desc
        self.tabtype = "univariate quali"
        self.header_nrows = 1
        self.nrows = self.header_nrows + len(a.actual_groups) 
        self.ncols = 2
        self._print_info()
        # table creation
        col2_head = a.desc + ", "+ a.display
        col1 = pd.Series([""] + a.actual_groups)
        col2 = pd.Series([col2_head] + [a.cell_content]*len(a.actual_groups))
        self.df = pd.concat([col1, col2], axis = 1)
        print(self.df)

    @_make_df.register
    def _make_df(self, a: Quant, b: Quali):
        # table infos
        self.tabtype = "quant x quali"
        self.header_nrows = 2
        self.nrows = self.header_nrows + len(a.display)
        self.ncols = 1 + len(b.groups) + 2
        self.caption = "{0} by {1}".format(a.desc, b.desc.lower())
        self._print_info()
        # table creation
        y_header = b.desc
        x_header = "{0} ({1})".format(a.desc, a.unit) if a.unit is not None else a.desc
        row1_header = ["", y_header] + [""] * (len(b.actual_groups) - 1)
        row2_header = [x_header] + b.actual_groups
        df   = pd.DataFrame(row1_header).transpose()
        row2 = pd.DataFrame(row2_header).transpose()
        df = pd.concat([df, row2])
        # fill the table rowwise
        for x in a.display:
            content = [x] + [a.cell_content] * (self.ncols - 1)
            new_row = pd.DataFrame(content).transpose()
            df = pd.concat([df, new_row])
        self.df = df
        print(self.df)

    @_make_df.register
    def _make_df(self, a: Quali, b: Quali):
        # table infos
        self.tabtype = "quali x quali"
        self.header_nrows = 2
        self.nrows = self.header_nrows + len(a.actual_groups)
        self.ncols = 1 + len(b.actual_groups)
        self.caption = "{0} by {1}".format(a.desc, b.desc.lower())
        self._print_info()
        # table creation
        # table creation
        y_header = b.desc + ", " + b.display
        x_header = a.desc
        row1_header = ["", y_header] + [""] * (len(b.actual_groups) - 1)
        row2_header = [x_header] + b.actual_groups
        df   = pd.DataFrame(row1_header).transpose()
        row2 = pd.DataFrame(row2_header).transpose()
        df = pd.concat([df, row2])
        # fill the table rowwise
        for x in a.actual_groups:
            content = [x] + [b.cell_content] * (self.ncols - 1)
            new_row = pd.DataFrame(content).transpose()
            df = pd.concat([df, new_row])
        self.df = df
        print(self.df)

    

Table(age)
Table(sex)
Table(age, trt)
Table(sex, trt)
Table(sex, trt)

# Change display
age2 = Quant("Age",
             display = ["median", "25pct", "75pct"],
             unit = 'years')
Table(age2)
Table(age2, trt)
age3 = Quant("Age",
             display = "median (iqr)",
             cell_content = "xx (xx - xx)")
Table(age3, trt)
sex2 = Quali("Sex", groups = ["M", "F"],
             display = "n", cell_content = "x")
Table(sex2)




        

# sections composition
univariate = tlf.Section(label = 'Univariate demographics', seq = [age, sex, trt])
bivariate = tlf.Section(label = 'Stratified demographics', seq = [sex * trt, age * trt])

#  custom tables: choose caption and cell content: strata just in case
stacked_univariate = tlf.Stacked(caption = 'Stacked/stratified demographics',x = [sex, age, trt, mmhg_t0, mmhg_t1])
stacked_bivariate = tlf.Stacked(caption = 'Stacked/stratified demographics', x = [sex, age, mmhg_t0, mmhg_t1], y = trt)
tab_custom = tlf.Table(caption = 'Age by treatment (n)', x = age, y = trt, cell_content = "x")
lst1 = tlf.Listing(variable = other)
    
custom = tlf.Section(label = "Other miscellaneous tests", seq = [stacked_uni, stacked_biv, tab_custom, lst1])

out = tlf.TLF(sections = [univariate, bivariate, custom])
out.to_doc("/tmp/tlf.doc")
out.to_latex("/tmp/tlf.tex")
