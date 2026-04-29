import random

def main():
    print('Домашнее задание № 2')
    print('Игра «Угадай число»')
    while True:
        print('Загадайте число от 1 до 10 (я попробую угадать)')

        number = random.randint(1, 10)
        attempts = 0

        while True:
            attempts += 1
            answer = input(f'Это число {number}? [введите: больше(>) / меньше(<) / да(=)]: ').lower()

            if answer in ('да', '='):
                print(f'Угадал за {attempts} попыток!\n')
                break
            elif answer in ('больше', '>'):
                number += 1
                if number > 10:
                    number = 10
            elif answer in ('меньше','<'):
                number -= 1
                if number < 1:
                    number = 1
            else:
                print('Пожалуйста, введите: больше(>), меньше(<) или да(=)')

        again = input('Загадаете новое число? (да/нет): ').lower()
        if again != 'да':
            print('Игра завершена.')
            break

if __name__ == '__main__':
    main()
