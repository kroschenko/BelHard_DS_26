def main():
    print('Домашнее задание № 1')
    print('Найдём площадь прямоугольника.')

    while True:
        try:
            x = float(input('Сторона А: '))
            if x <= 0:
                print("Ошибка: число должно быть положительным.")
                continue
            break
        except ValueError:
            print("Ошибка: введите корректное число.")

    while True:
        try:
            y = float(input('Сторона Б: '))
            if y <= 0:
                print("Ошибка: число должно быть положительным.")
                continue
            break
        except ValueError:
            print("Ошибка: введите корректное число.")

    print('Площадь прямоугольника =', x * y)


if __name__ == '__main__':
    main()