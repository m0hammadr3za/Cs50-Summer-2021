from cs50 import get_string

text = get_string("Text: ")

letter_count = 0
space_count = 0
sentence_count = 0

for i in text:
    if ord(i.upper()) >= ord("A") and ord(i.upper()) <= ord("Z"):
        letter_count += 1
    if i == " ":
        space_count += 1
    if i in [".", "!", "?"]:
        sentence_count += 1

l = (letter_count * 100) / (space_count + 1)
s = (sentence_count * 100) / (space_count + 1)
index = round(0.0588 * l - 0.296 * s - 15.8)

if index > 16:
    print("Grade 16+")
elif index < 1:
    print("Before Grade 1")
else:
    print(f"Grade {index}")