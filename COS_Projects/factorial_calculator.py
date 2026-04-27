num = int(input("Enter the number for which you want to calculate a factorial "))
def factorial(num):
    if num == 0 or num == 1:
        return 1
    else:
        return num * factorial(num - 1)

print(factorial(num))