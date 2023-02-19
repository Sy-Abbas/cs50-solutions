#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    int spaces;

    // taking input from user
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // printing the pattern
    for (int i = 0; i < height; i++)
    {
        spaces = height - 1 - i;
        for (int y = 0; y < height; y++)
        {
            if (y < spaces)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }
        printf("\n");
    }
}