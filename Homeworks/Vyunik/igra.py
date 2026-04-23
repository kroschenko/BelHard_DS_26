from __future__ import annotations

import random


class GuessNumberGame:
    def __init__(self, min_number: int = 1, max_number: int = 10) -> None:
        self.min_number = min_number
        self.max_number = max_number
        self.secret_number = 0
        self.attempts = 0

    def start_new_round(self) -> None:
        self.secret_number = random.randint(self.min_number, self.max_number)
        self.attempts = 0

    @staticmethod
    def read_guess(prompt: str) -> int:
        while True:
            try:
                guess = int(input(prompt))
                return guess
            except ValueError:
                print("Ошибка: введите целое число.")

    def play_round(self) -> None:
        self.start_new_round()

        print(f"\nЯ загадал число от {self.min_number} до {self.max_number}.")
        print("Попробуй угадать его!")

        while True:
            guess = self.read_guess("Ваш вариант: ")
            self.attempts += 1

            if guess < self.min_number or guess > self.max_number:
                print(f"Число должно быть в диапазоне от {self.min_number} до {self.max_number}.")
                continue

            if guess < self.secret_number:
                print("Загаданное число больше.")
            elif guess > self.secret_number:
                print("Загаданное число меньше.")
            else:
                print(f"Верно! Вы угадали число {self.secret_number} за {self.attempts} попыток.")
                break

    def run(self) -> None:
        print("=== Игра «Угадай число» ===")

        while True:
            self.play_round()

            answer = input("Сыграем ещё раз? (да/нет): ").strip().lower()
            if answer not in ("да", "д", "yes", "y"):
                print("Спасибо за игру!")
                break


if __name__ == "__main__":
    game = GuessNumberGame(1, 10)
    game.run()
