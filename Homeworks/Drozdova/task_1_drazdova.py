a = 1.0
b = 1.0
print('Расчет площади прямоугольника')

try:
     a  = float(input(f'Введите ширину:\n'))
     b = float(input(f'Введите длину:\n'))

except ValueError:
     print('Это не число. Выходим.')
     exit()
else:

    print(f'Площадь прямоугольника: s = {a * b:0.2f}')
finally: print('Goodbye, user!')
