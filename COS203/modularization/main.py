from modularization.logic_module import logic as lgm
import modularization.input_module as inm
from modularization.output_module import print_grade

grade = lgm(inm.score)
print(print_grade(inm.name, inm.score, grade))