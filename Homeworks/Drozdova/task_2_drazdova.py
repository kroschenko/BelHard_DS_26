import random

from numpy._core.strings import upper

numberGuess = [0,1,2,3,4,5,6,7,8,9,10]
attemptNum = 1
print(f'Игра Угадайка\n')
userAnswer = upper(input('Загадай число от 0 до 10\n Загадала? - ответь - Д или Н \n '))
try:
    match userAnswer:
        case 'Д':
            print(f'your answer is {userAnswer}')
            useAnswOne = upper(input(f'Ваше число меньше 6? - ответь - Д или Н \n'))
            match useAnswOne:
                case 'Д':
                    print(f'your answer is {useAnswOne}')
                    oddNum = [0, 1, 2, 3, 4, 5]
                    attemptN = 1
                    while attemptN < len(oddNum):
                        taskNum = oddNum[attemptN]
                        userAnswTwo = input(f'Вы загадали {taskNum} Д или Н \n')
                        attemptN += 1
                        if userAnswTwo == 'Д':
                            print(f'Вы загадали  {taskNum}. Спасибо за игру')
                            break
                        else: continue



                case 'Н':
                  print(f'your answer is {useAnswOne}')
                  oddNum = [6, 7, 8, 9, 10]
                  attemptI = 0
                  while attemptI < len(oddNum):
                    taskNumT: int = oddNum[attemptI]
                    attemptI += 1
                    userAnswTwo = input(f'Вы загадали {taskNumT} Д или Н\n')
                    if userAnswTwo == 'Д':
                        print(f'Вы загадали  {taskNumT}. Спасибо за игру')
                        break
                    elif userAnswTwo == 'Н':
                        continue

        case 'Н':
            print(f'your answer is {userAnswer}. Очень жаль, до новой игры!')
        case _:
            print(f'your answer is {userAnswer} is not correct!')
except ValueError as e:
 print("Сведения об исключении", e)
 exit()

