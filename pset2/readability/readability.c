#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <ctype.h>

int main(void)
{
    string input_text = get_string("Text: ");

    int number_of_letters = 0;
    int number_of_spaces = 0;
    int number_of_sentences = 0;

    for (int i = 0, n = strlen(input_text); i < n; i++)
    {
        if (toupper(input_text[i]) >= 'A' && toupper(input_text[i]) <= 'Z')
        {
            number_of_letters++;
        }

        if (input_text[i] == ' ')
        {
            number_of_spaces++;
        }

        if (input_text[i] == '.' || input_text[i] == '?' || input_text[i] == '!')
        {
            number_of_sentences++;
        }
    }

    int number_of_words = number_of_spaces + 1;

    float l = (number_of_letters * 100.0) / number_of_words;
    float s = (number_of_sentences * 100.0) / number_of_words;
    int index = round(0.0588 * l - 0.296 * s - 15.8);

    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}