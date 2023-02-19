#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int r = 0; r < height; r++)
    {
        for (int c = 0; c < width; c++)
        {
            int av = round((image[r][c].rgbtBlue + image[r][c].rgbtRed + image[r][c].rgbtGreen) / 3.0);
            image[r][c].rgbtBlue = av;
            image[r][c].rgbtRed = av;
            image[r][c].rgbtGreen = av;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int c = 0; c < width / 2; c++)
    {
        for (int r = 0; r < height; r++)
        {
            int tempb = image[r][c].rgbtBlue;
            int tempr = image[r][c].rgbtRed;
            int tempg = image[r][c].rgbtGreen;

            image[r][c].rgbtBlue = image[r][(width - 1) - c].rgbtBlue;
            image[r][c].rgbtRed = image[r][(width - 1) - c].rgbtRed;
            image[r][c].rgbtGreen = image[r][(width - 1) - c].rgbtGreen;

            image[r][(width - 1) - c].rgbtBlue = tempb;
            image[r][(width - 1) - c].rgbtRed = tempr;
            image[r][(width - 1) - c].rgbtGreen = tempg;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int r = 0; r < height; r++)
    {
        for (int c = 0; c < width; c++)
        {
            copy[r][c] = image[r][c];
        }
    }
    for (int r = 0; r < height; r++)
    {
        for (int c = 0; c < width; c++)
        {
            int sumB = 0;
            int sumR = 0;
            int sumG = 0;
            float count = 0.00;
            for (int x = -1; x < 2; x++)
            {
                for (int y = -1; y < 2; y++)
                {
                    int row = r + x;
                    int col = c + y;
                    if ((row >= 0 && row < height) && (col >= 0 && col < width))
                    {
                        sumB += copy[row][col].rgbtBlue;
                        sumR += copy[row][col].rgbtRed;
                        sumG += copy[row][col].rgbtGreen;
                        count += 1;
                    }
                }
            }
            image[r][c].rgbtBlue = round(sumB / count);
            image[r][c].rgbtRed = round(sumR / count);
            image[r][c].rgbtGreen = round(sumG / count);
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int r = 0; r < height; r++)
    {
        for (int c = 0; c < width; c++)
        {
            copy[r][c] = image[r][c];
        }
    }
    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
    for (int r = 0; r < height; r++)
    {
        for (int c = 0; c < width; c++)
        {
            double gxB = 0;
            double gxR = 0;
            double gxG = 0;

            double gyB = 0;
            double gyR = 0;
            double gyG = 0;

            for (int x = -1; x < 2; x++)
            {
                for (int y = -1; y < 2; y++)
                {
                    int row = r + x;
                    int col = c + y;
                    if ((row >= 0 && row < height) && (col >= 0 && col < width))
                    {
                        gxB += copy[row][col].rgbtBlue * gx[1 + x][1 + y];
                        gxR += copy[row][col].rgbtRed * gx[1 + x][1 + y];
                        gxG += copy[row][col].rgbtGreen * gx[1 + x][1 + y];

                        gyB += copy[row][col].rgbtBlue * gy[1 + x][1 + y];
                        gyR += copy[row][col].rgbtRed * gy[1 + x][1 + y];
                        gyG += copy[row][col].rgbtGreen * gy[1 + x][1 + y];

                    }
                }
            }
            image[r][c].rgbtBlue = round(sqrt(pow(gxB, 2.00) + pow(gyB, 2.00))) > 255 ? 255 : round(sqrt(pow(gxB, 2.00) + pow(gyB, 2.00)));
            image[r][c].rgbtRed = round(sqrt(pow(gxR, 2.00) + pow(gyR, 2.00))) > 255 ? 255 : round(sqrt(pow(gxR, 2.00) + pow(gyR, 2.00)));
            image[r][c].rgbtGreen = round(sqrt(pow(gxG, 2.00) + pow(gyG, 2.00))) > 255 ? 255 : round(sqrt(pow(gxG, 2.00) + pow(gyG, 2.00)));

        }
    }
    return;
}
