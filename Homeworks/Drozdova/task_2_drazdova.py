import random
from numpy._core.strings import upper

print(f'Игра Угадайка\n')
while True:
    userAnswer = input('Загадай число от 1 до 10\n Загадала? - ответь - Д/Н \n ').upper().strip()
    try:
        match userAnswer:
            case 'Д':
                print(f'your answer is {userAnswer}')
                # Определить, в какой половине искать
                is_less_than_6 = input('Ваше число меньше 6? (Д/Н): ').upper().strip()

                if is_less_than_6 == 'Д':
                    min_val, max_val = 1, 5
                elif is_less_than_6 == 'Н':
                    min_val, max_val = 6, 10
                else:
                    print(f'выш ответ {is_less_than_6} некорректен! \n ')

                # Список возможных чисел для этой половины
                possible_numbers = list(range(min_val, max_val + 1))
                random.shuffle(possible_numbers)  # Перемешиваем для эффекта "угадывания"

                found = False
                for num in possible_numbers:
                    ans = input(f'Вы загадали {num}? (Д/Н): ').upper().strip()
                    if ans == 'Д':
                       print(f'Ура! Число {num} угадано!')
                       found = True
                       break

                if not found:
                    print("Хм, вы забыли загаданное число?...\n")

                        #  предложение новой игры
                new_round = input('\nПродолжим игру? (Д/Н): ').strip().upper()
                if new_round != 'Д':
                    print('Спасибо за игру! До встречи.')
                    break  # Выход из главного цикла while True
            case 'Н':
                print(f'Ваш ответ -- {userAnswer}. \n Очень жаль, до новой игры!')
                exit()
            case _:
                print(f'Ваш ответ -- {userAnswer} -- не корректен!')
    except ValueError as e:
        print("Сведения об исключении", e)
        exit()

