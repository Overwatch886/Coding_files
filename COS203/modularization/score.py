def get_student_data():
    global score
    global name
    name = input("What's your name? ")
    score = int(input("What's your score: "))
def calculate_grade(score):
    if score >= 50:
        return "PASSED"
    else:
        return "FAILED"
def display_result(name, score, grade):
    return (f"{name} scored {score} and therefore {grade}")

get_student_data()
grade = calculate_grade(score)
print(display_result(name, score, grade))