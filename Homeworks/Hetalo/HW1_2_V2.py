input('Загадай число от 1 до 10, для продолжения нажми Enter')

low = 1
high = 10
feedback = ''

while feedback != '=':
    guess = round((low + high) / 2)

    feedback = input(f'Твое число больше, меньше или равно числу {guess}? (введи: >, <, =): ')

    if feedback == '>':
        low = guess + 1
    elif feedback == '<':
        high = guess - 1
    elif feedback == '=':
        print(f'Ты загадал число {guess}')
    else:
        print('Пожалуйста, используй символы ">", "<" или "="')
