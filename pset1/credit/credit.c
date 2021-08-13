#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    long credit = get_long("Number: ");

    int sum = 0;
    bool finish_looping = false;
    int counter = 1;
    while (!finish_looping)
    {
        long digit = credit % (long) pow(10, counter);
        if (digit == credit)
        {
            finish_looping = true;
        }

        digit = digit / (long) pow(10, counter - 1);

        if (counter % 2 == 0)
        {
            digit = digit * 2;

            if (digit >= 10)
            {
                sum += 1;
                sum += digit % 10;
            }
            else
            {
                sum += digit;
            }
        }
        else
        {
            sum += digit;
        }

        counter++;
    }

    int credit_length = counter - 1;
    bool has_valid_sum = sum % 10 == 0;
    int first_two_digits = credit / (long) pow(10, credit_length - 2);
    int first_digit = first_two_digits / 10;

    if (has_valid_sum && credit_length == 15 && (first_two_digits == 34 || first_two_digits == 37))
    {
        printf("AMEX\n");
        return 0;
    }
    else if(has_valid_sum && credit_length == 16 && (first_two_digits == 51 || first_two_digits == 52 ||
                                                      first_two_digits == 53 || first_two_digits == 54 ||
                                                      first_two_digits == 54))
    {
        printf("MASTERCARD\n");
        return 0;
    }

    else if(has_valid_sum && (credit_length == 13 || credit_length == 16) && first_digit == 4)
    {
        printf("VISA\n");
        return 0;
    }

    printf("INVALID\n");
}