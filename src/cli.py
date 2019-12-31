def cli():
    weight = int(input("Please insert weight of the table (default: (25))> "))
    heigth = int(input("Please insert heigth of the table (default: (25))> "))

    if not weight:
        weight = 25
    if not heigth:
        heigth = 25

    return weight, heigth