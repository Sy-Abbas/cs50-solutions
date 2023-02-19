#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    // Taking input from the user
    string text;
    do
    {
        text = get_string("Text: ");
    }
    while (strlen(text) <= 0);

    int len  = strlen(text);

    // Declaring variablea to count letters, words and sentences
    int letters = 0;
    int words = 1;
    int sentences = 0;

    // Iterating though the input to count number of letters, words and sentences
    for (int i = 0; i < len; i++)
    {
        int charNumber = (int) tolower(text[i]);
        if (charNumber >= 97 && charNumber <= 122)
        {
            letters += 1;
        }
        else if ((int)text[i] == 32)
        {
            words += 1;
        }
        else if ((int)text[i] == 46 || (int)text[i] == 63 || (int)text[i] == 33)
        {
            sentences += 1;
        }
    }

    // Find average letters per 100 words and average sentences per 100 words.
    float L = (letters * 100.00) / words;
    float S = (sentences * 100.00) / words;

    // Coleman-Liau index
    int index = (int) round((0.0588 * L) - (0.296 * S) - 15.8);

    // Printing the output
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}