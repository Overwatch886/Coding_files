while True:
    try:
        user_grade = int(input("Kindly Input Your Overall Score in Numbers for the Course you want to calculate your Grade and Grade Points "))
        if 0 <= user_grade <= 100:
            break
        else:
            print("Input a Valid Grade between 0 and 100!!")
    except ValueError:
        print("Input a Valid Integer!!")

grade_ranges = [
    (0, 39, 'F', 0),
    (40, 44, 'E', 1),
    (45, 49, 'D', 2),
    (50, 59, 'C', 3),
    (60, 69, 'B', 4),
    (70, 100, 'A', 5)
]

for grade_range in grade_ranges:
    if grade_range[0] <= user_grade <= grade_range[1]:
        print("Congratulations!, You scored " + str(grade_range[2]) + " which gives you " + str(grade_range[3]) + " grade points")
        break