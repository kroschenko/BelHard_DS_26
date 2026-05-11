def read_positive_number(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt).replace(",", "."))
            if value <= 0:
                print("Ошибка: число должно быть больше 0.")
                continue
            return value
        except ValueError:
            print("Ошибка: введите корректное число.")

def calculate_rectangle_area(width: float, height: float) -> float:
    return width * height

def main() -> None:
    print("=== Площадь прямоугольника ===")
    width = read_positive_number("Введите первую сторону: ")
    height = read_positive_number("Введите вторую сторону: ")
    area = calculate_rectangle_area(width, height)
    print(f"Площадь прямоугольника: {area}")

if __name__ == "__main__":
    main()
