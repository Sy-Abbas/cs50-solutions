text = input("Text: ")
words = 1
letters = 0
sentences = 0
for x in text:
    a = ord(x.lower())
    if a >= 97 and a <= 122:
        letters += 1
    elif a in [46, 63, 33]:
        sentences += 1
    elif a == 32:
        words += 1

L = (letters * 100.00) / words
S = (sentences * 100.00) / words

index = round((0.0588 * L) - (0.296 * S) - 15.8)
if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print("Grade " + str(index))
