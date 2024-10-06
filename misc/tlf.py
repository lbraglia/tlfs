# import tlf

from dataclasses import dataclass, field
from multimethod import multimethod

def _def_quant_display():
    return ("missing", "not missing", "min", "25pct",
            "mean", "median", "75pct", "max", "sd", "iqr")

def _def_quali_groups():
    return ("All")


@dataclass
class Quant:
    desc: str = None   # long variable description
    unit: str = None   # unit of measure
    min: float = None  # minimum
    max: float = None  # maximum
    display: list[str]|tuple[str] = field(default_factory = _def_quant_display)
    cell_content: str = "x"  # default cell content (single number)

@dataclass
class Quali:
    desc: str   # variable description
    groups: list[str]|tuple[str] = field(default_factory = _def_quali_groups)
    display: str = "n (col %)"
    cell_content: str = "x (x)"  # default cell content (single number)

    
@dataclass
class Table():
    x: Quant|Quali
    y: Quant|Quali|None = None # none if univariate
    row_tot: bool = True
    col_tot: bool = False
    
    def to_df(self):
        self.df(a = self.x, b = self.y)

    @multimethod
    def df(self, a, b):
        print("boo")

    @df.register
    def df(self, a: Quant, b: None):
        print("univariate quant")

    @df.register
    def df(self, a: Quant, b: None):
        print("univariate quali")

    @df.register
    def df(self, a: Quant, b: Quali):
        print("quant x quali")

    @df.register
    def df(self, a: Quali, b: Quali):
        print("quant x quali")
        
    
    
    
age  = Quant("Age")
age2 = Quant("Age", display = ["median", "25pct", "75pct"])
age3 = Quant("Age", display = "median (iqr)", cell_content = "xx (xx - xx)")
sex = Quali("Sex", groups = ["M", "F"])
sex2 = Quali("Sex", groups = ["M", "F"], display = "n", cell_content = "x")
trt = Quali("Treatment", groups = ["EXP", "CTRL"])


t1 = Table(age, sex)
t1.to_df()



Table(sex)
Table(age, trt)
Table(sex, trt)


# As long as i use functions this works lovely
@multimethod
def disp(a, b):
    print("dunno")
    
@multimethod
def disp(a: int, b: None):
    print("int x none")

@multimethod
def disp(a: str, b: None):
    print("str x none")

@multimethod
def disp(a: int, b: str):
    print("int x str")

@multimethod
def disp(a: str, b: str):
    print("str x str")


disp(None, None) # dunno
disp(1, None)    # int x none
disp("test", None) # str x none
disp(1, "test")    # int x str
disp("test", "test") # str x str


 


@dataclass
class Test:
    x: int|str
    y: int|str|None = None
    
    def do(self):
        self._dispatch(self.x, self.y)

    @multimethod
    def _dispatch(self, a, b): # default case
        print("dunno")

    @multimethod
    def _dispatch(self, a: int, b: None):
        print("int x none")

    @multimethod
    def _dispatch(self, a: str, b: None):
        print("str x none")

    @multimethod
    def _dispatch(self, a: int, b: str):
        print("int x str")

    @multimethod
    def _dispatch(self, a: str, b: str):
        print("str x str")

    # etc..

## what is printed is always the default case
t1 = Test(1)
type(t1.x)
t1.y is None
t1.do() # should be int x none
Test("test").do()  # should be str x none
Test(1, "test").do()  # should be int x str
Test("test", "test").do()  # should be str x str




        

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
