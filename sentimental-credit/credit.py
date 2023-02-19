def getInt():  # Function to check if input is a number or not
    try:
        num = int(input("Number: "))
        return num
    except:
        getInt()


num = getInt()
sum = 0
strNum = str(num)
i = 0
for x in range(len(strNum)-1, -1, -1):  # Calculating checksum
    if i % 2 == 0:
        sum += int(strNum[x])
    else:
        c = strNum[x]
        a = int(c) * 2
        b = str(a)
        if len(b) > 1:
            sum += int(b[0])
            sum += int(b[1])
        else:
            sum += a
    i += 1
if sum % 10 == 0:  # If sum has a 0 as its last digit, number has passed checksum
    a = (str(strNum))[0:2]
    lenNum = len(str(strNum))
    if lenNum == 15:
        if a in ["34", "37"]:
            print("AMEX")
    elif lenNum == 16:
        if a in ["51", "52", "53", "54", "55"]:
            print("MASTERCARD")
        elif (str(strNum))[0] == "4":
            print("VISA")
    elif lenNum == 13:
        if (str(strNum))[0] == "4":
            print("VISA")
    else:
        print("INVA2LID")
else:
    print("INVALID")