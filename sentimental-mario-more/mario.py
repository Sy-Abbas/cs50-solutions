def inputNum():
    try:
        num = int(input("Height: "))  # Taking users input
        if num > 0 and num < 9:
            spaces = num - 1
            while spaces >= 0:  # Loop to print the pattern
                print(" " * spaces, end="")
                print("#" * (num - spaces), end="")
                print(" " * 2, end="")
                print("#" * (num - spaces), end="")
                print("")
                spaces -= 1
        else:
            inputNum()
    except:
        inputNum()


inputNum()

