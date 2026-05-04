import random

class GuessGame:

    def __init__(self):
        self.min_num = None
        self.max_num = None
        self.choice = None

    def start(self, min_num, max_num):
        self.min_num = min_num
        self.max_num = max_num
        self.choice = int(input("Загадайте число: "))
        self.guess()

    def guess(self):
        print('Начинаю угадывать')
        while True:
            number = random.randint(self.min_num, self.max_num)
            print(f'{number}, ', end='')
            if number == self.choice:
                print(f'\n Загаданное число {number}')
                break
            else:
                if number < self.choice:
                    self.min_num = number+1
                else:
                    self.max_num = number-1

    def __str__(self):
        return f'Guess game between {self.min_num} and {self.max_num}'

if __name__ == '__main__':
    isGame = 1
    game = GuessGame()
    while isGame == 1:
        game.start(1, 10)
        isGame = int(input('Хотите продолжить? \n1. Да \n2. Нет \n'))