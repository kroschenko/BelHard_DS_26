class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_area(self):
        return self.width * self.height


width = float(input('Введите ширину: '))
height = float(input('Введите высоту: '))

rectangle = Rectangle(width, height)
print(f'Площадь прямоугольника: {rectangle.get_area()}')
