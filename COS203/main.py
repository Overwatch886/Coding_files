from logic_module import logic as lgm
import input_module as inm
from output_module import print_grade

grade = lgm(inm.score)
print(print_grade(inm.name, inm.score, grade))