from operator import truediv
from time import sleep


class guessNumber:
    def __init__(self,min,max):
        self.min = min
        self.max = max
        self.attempts = 0
        print("Welcome to the game: guess number")
        print(f"Guess the number from {self.min} to {self.max}")
        ready = input("Are you ready?: Enter")

    def play(self):
        self.attempts += 1
        number=(self.max+self.min)//2
        print(f"\nAttempt {self.attempts}. My guess is {number}")
        res=input("If I guessed input '=', if your number less input '<' if your number greater input '>' ")
        if res=='=':
            print(f"I guessed the correct number in {self.attempts} attempts!")
            return True
        elif res=='<':
            self.max=number-1
        elif res=='>': self.min=number+1
        else:
            print("You input a wrong symbol. Please try again")
            self.attempts -= 1
    """print(f"{self.min} to {self.max}")"""

game=guessNumber(1,10)
while True:
    if game.play()==True:
        break
