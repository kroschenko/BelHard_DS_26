import random


class GuessNumberGame:
    def __init__(self, min_number: int = 1, max_number: int = 10) -> None:
        self.min_number = min_number
        self.max_number = max_number
        self.attempts = 0

    def start_new_round(self) -> None:
        self.attempts = 0

    @staticmethod
    def read_feedback(prompt: str) -> str:
        while True:
            answer = input(prompt).strip().lower()
            if answer in ("больше", "меньше", "верно"):
                return answer
            print('Ошибка: введите "больше", "меньше" или "верно".')

    def play_round(self) -> None:
        self.start_new_round()

        print(f"\nЗагадайте число от {self.min_number} до {self.max_number}.")
        input("Когда загадаете — нажмите Enter...")

        low = self.min_number
        high = self.max_number

        while True:
            guess = (low + high) // 2
            self.attempts += 1

            print(f"\nМоя догадка: {guess}")
            feedback = self.read_feedback('Ответ ("больше" / "меньше" / "верно"): ')

            if feedback == "верно":
                print(f"Ура! Я угадал число {guess} за {self.attempts} попыток.")
                break
            elif feedback == "больше":
                low = guess + 1
            else:  # меньше
                high = guess - 1

            if low > high:
                print("Кажется, вы меняли число или ошиблись в подсказках!")
                break

    def run(self) -> None:
        print("=== Игра «Угадай число» ===")
        print("Вы загадываете — я угадываю!")

        while True:
            self.play_round()

            answer = input("Сыграем ещё раз? (да/нет): ").strip().lower()
            if answer not in ("да", "д", "yes", "y"):
                print("Спасибо за игру!")
                break


if __name__ == "__main__":
    game = GuessNumberGame(1, 10)
    game.run()
