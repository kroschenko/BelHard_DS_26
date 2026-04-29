try:
    a=float(input("Input size of the first side a:"))
    b=float(input("Input size of the second side b:"))
    if a<=0 or b<=0:
        print("ERROR: The sides of the rectangle must be only positive number")
    else:
        print(f"The area of rectangle is: {a*b}")
except ValueError:(
    print("ERROR: Invalid input. Please enter numbers, not text."))

