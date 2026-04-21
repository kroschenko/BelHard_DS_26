min_dig=1
max_dig=10
iter_n=int(max_dig/2)
print("Гадалка, v1.0")
print(f"Загадайте число от {min_dig} до {max_dig}")
while True:
    print(f"Число больше {iter_n}?")
    while True:
            answer=input("Д (да)/Н (нет) :")
            if answer=="Д" or answer=="д": 
                min_dig=iter_n+1
                iter_n=int((max_dig+min_dig)/2)
                break
            elif answer=="Н" or answer=="н":
                max_dig=iter_n
                iter_n=int((max_dig+min_dig)/2)
                break
            else:
                print("Повторите ответ")
    if min_dig==max_dig:
        print(f"Загаданное число :{iter_n}")
        break
