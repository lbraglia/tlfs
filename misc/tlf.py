import tlf

trt = tlf.Category(label = "Treatment", groups = ["EXP", "CTRL"])
sex = tlf.Category(label = "Sex", groups = ["M", "F"])
age = tlf.Quantity(label = 'Age at diagnosis')
other = tlf.FreeText(label = 'Other specify')
mmhg_t0 = tlf.Quantity(label = 'Blood pressure at T0')
mmhg_t1 = tlf.Quantity(label = 'Blood pressure at T1')

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
