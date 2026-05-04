import random

# Создаем список один раз. list(range(1, 11)) создаст [1, 2, ..., 10]
initial_numbers = list(range(1, 11))
numbers = initial_numbers.copy()

print("Загадайте число от 1 до 10 в уме.")

while len(numbers) > 0:
    attempt = random.choice(numbers)
    answer = input(f"Вы загадали {attempt}? (да/нет): ").lower()
    
    if answer == "да":
        print("Ура! Я угадал!")
        again = input("Еще раз? (да/нет): ").lower()
        if again == "да":
            # Просто сбрасываем список к исходному состоянию
            numbers = initial_numbers.copy()
            print("Загадайте новое число!")
            continue 
        else:
            break 
    else:
        numbers.remove(attempt)
        print("Думаю дальше...")

if not numbers:
    print("Числа закончились!")