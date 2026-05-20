import random
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print("Загадайте число от 1 до 10 в уме.")
while len(numbers) > 0:
    attempt = random.choice(numbers)
    answer = input(f"Вы загадали {attempt}? (да/нет): ").lower()
    if answer == "да":
        print("Ура! Я угадал!")
        # Спрашиваем про новую игру
        again = input("Еще раз? (да/нет): ").lower()
        if again == "да":
            numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] 
            print("Загадайте новое число!")
            continue 
        else:
            break 
    else:
        numbers.remove(attempt)
        print("Думаю дальше...")
if not numbers:
    print("Числа закончились!")
