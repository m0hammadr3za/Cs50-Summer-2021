from cs50 import get_string

number = get_string("Number: ")

digits_sum = 0

for i in range(len(number) - 2 , -1, -2):
    digit = int(number[i]) * 2
    if digit >= 10:
        digits_sum += 1
        digits_sum += digit % 10
    else:
        digits_sum += digit

for i in range(len(number) - 1, -1, -2):
    digits_sum += int(number[i])

valid_sum = digits_sum % 10 == 0;
if valid_sum and len(number) == 15 and int(number[0:2]) in [34, 37]:
    print("AMEX")
elif valid_sum and len(number) == 16 and int(number[0:2]) in [51, 52, 53, 54, 55]:
    print("MASTERCARD")
elif valid_sum and len(number) in [13, 16] and int(number[0:1]) == 4:
    print("VISA")
else:
    print("INVALID")