#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    // checking if user gave the key
    if (argc != 2)
    {
        printf("Usage: ./substitution KEY\n");
        return 1;
    }

    // checking if key is 26 characters long
    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters\n");
        return 1;
    }

    // checking if key contains only alphabetic characters
    for (int i = 0; i < 26; i++)
    {
        int ascii = tolower(argv[1][i]);
        if (ascii < 97 || ascii > 122)
        {
            printf("Key must only contain alphabetic characters.\n");
            return 1;
        }
    }

    // checking if every character is unique in the key
    for (int i = 0; i < 26; i++)
    {
        int same = 0;
        int ascii = tolower(argv[1][i]);
        for (int y = 0; y < 26; y++)
        {
            int asci = tolower(argv[1][y]);
            if (ascii == asci)
            {
                same++;
            }
        }
        if (same > 1)
        {
            printf("Key must not contain repeated characters.\n");
            return 1;
        }
    }

    // get input
    string pText = get_string("plaintext: ");

    // make a new array of char to store the ciphertext
    int len = strlen(pText);
    char cText[len];

    // cipher the plaintext
    printf("ciphertext: ");
    for (int i = 0; i < len; i++)
    {
        int ascii = pText[i];
        if (ascii >= 97 && ascii <= 122)
        {
            cText[i] = tolower(argv[1][ascii - 97]);
        }
        else if (ascii >= 65 && ascii <= 90)
        {
            cText[i] = toupper(argv[1][ascii - 65]);
        }
        else
        {
            cText[i] = pText[i];
        }
        printf("%c", cText[i]);
    }
    printf("\n");
}