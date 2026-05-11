def rectan(x,y):
    return x*y

while True:
    try:
        len_r=int(input("Введите длину : "))
        break
    except ValueError:
        print("Это не число")
while True:
    try:
        wid_r=int(input("Введите ширину : "))
        break
    except ValueError:
        print("Это не число")
print("Площадь : ",rectan(len_r,wid_r))
