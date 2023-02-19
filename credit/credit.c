#include <cs50.h>
#include <stdio.h>
#include <math.h>

// Luhn’s Algorithm
bool checksum(long num, int n)
{
    if (n == 0)
    {
        return false;
    }
    int sum = 0;
    for (int i = 2; i <= n; i += 2)
    {
        long a = 2 * ((num % (long)pow(10, i)) / (long)pow(10, i - 1));
        int b = (int)a;
        if (b > 9)
        {
            sum += b % 10 + (b % 100) / 10;
        }
        else
        {
            sum += b;
        }
    }
    for (int i = 1; i <= n; i += 2)
    {
        long a = (num % (long)pow(10, i)) / (long)pow(10, i - 1);
        sum += (int)a;
    }
    if ((sum % (int)pow(10, 1) == 0))
    {
        return true;
    }
    else
    {
        return false;
    }
}
int main(void)
{
    long num;
    int n;
    num = get_long("Number: ");

    // Calculating number of digits, if
    if (num < 1000000000000  || (num > 9999999999999 && num < 100000000000000) || num > 9999999999999999)
    {
        n = 0;
    }
    else if (num > 999999999999 && num < 10000000000000)
    {
        n = 13;
    }
    else if (num > 99999999999999 && num < 1000000000000000)
    {
        n = 15;
    }
    else
    {
        n = 16;
    }
    if (checksum(num, n))
        // if credit card number is valid, check for which credit card is it.
    {
        switch (n)
        {
            case 13:
                if (num >= 4000000000000 && num < 5000000000000)
                {
                    printf("VISA\n");
                }
                else
                {
                    printf("INVALID\n");
                }
                break;

            case 15:
                if ((num >= 340000000000000 && num < 350000000000000) || (num >= 370000000000000 && num < 380000000000000))
                {
                    printf("AMEX\n");
                }
                else
                {
                    printf("INVALID\n");
                }
                break;

            case 16:
                if (num >= 5100000000000000 && num < 5600000000000000)
                {
                    printf("MASTERCARD\n");
                }
                else if (num >= 4000000000000000 && num < 5000000000000000)
                {
                    printf("VISA\n");
                }
                else
                {
                    printf("INVALID\n");
                }
                break;
        }
    }
    else
    {
        printf("INVALID\n");
    }
}