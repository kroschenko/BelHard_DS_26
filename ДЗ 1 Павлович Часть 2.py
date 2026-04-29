import random  


secret_number = random.randint(0, 10)

print("Привет! Я загадал число от 0 до 10.")
print("Попробуй угадать его!")

attempts = 0  
while True: 
    attempts += 1  

    
    try:
        guess_str = input(f"Попытка №{attempts}: Введи число: ")
        guess = int(guess_str)
        
        if not (0 <= guess <= 10):
            print("Пожалуйста, введи число от 0 до 10.")
            continue
        
        if guess < secret_number:
            print("Мое число БОЛЬШЕ твоего.")
        elif guess > secret_number:
            print("Мое число МЕНЬШЕ твоего.")
        else:  
            print(f"\n УРА! Ты угадал число {secret_number} за {attempts} попыток!")
            break  

    except ValueError:
        
        print("Некорректный ввод! Пожалуйста, вводи только целые числа.")

    


