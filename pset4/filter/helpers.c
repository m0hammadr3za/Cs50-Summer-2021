#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmp[height][width];
    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            tmp[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int r = tmp[i][j].rgbtRed;
            int g = tmp[i][j].rgbtGreen;
            int b = tmp[i][j].rgbtBlue;

            int average = round((r + g + b) / 3);

            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0, n = width / 2; j <= n; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][(width - 1) - j];
            image[i][(width - 1) - j] = temp;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmp[height][width];
    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            tmp[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red_sum = 0;
            int green_sum = 0;
            int blue_sum = 0;
            int pixel_count = 0;
            for (int k = i - 1; k < i + 2; k++)
            {
                for (int l = j - 1; l < j + 2; l++)
                {
                    if (k >= 0 && k <= height - 1 && l >= 0 && l <= width - 1)
                    {
                        red_sum += tmp[k][l].rgbtRed;
                        green_sum += tmp[k][l].rgbtGreen;
                        blue_sum += tmp[k][l].rgbtBlue;
                        pixel_count++;
                    }
                }
            }
            image[i][j].rgbtRed = round(red_sum / pixel_count);
            image[i][j].rgbtGreen = round(green_sum / pixel_count);
            image[i][j].rgbtBlue = round(blue_sum / pixel_count);
        }
    }
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmp[height][width];
    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            tmp[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int gx_red_sum = 0;
            int gy_red_sum = 0;

            int gx_green_sum = 0;
            int gy_green_sum = 0;

            int gx_blue_sum = 0;
            int gy_blue_sum = 0;

            for (int k = i - 1; k < i + 2; k++)
            {
                for (int l = j - 1; l < j + 2; l++)
                {
                    if (k >= 0 && k <= height - 1 && l >= 0 && l <= width - 1)
                    {
                        int gx = l - j;
                        if (k - i == 0)
                        {
                            gx *= 2;
                        }

                        int gy = k - i;
                        if (l - j == 0)
                        {
                            gy *= 2;
                        }

                        gx_red_sum += tmp[k][l].rgbtRed * gx;
                        gy_red_sum += tmp[k][l].rgbtRed * gy;

                        gx_green_sum += tmp[k][l].rgbtGreen * gx;
                        gy_green_sum += tmp[k][l].rgbtGreen * gy;

                        gx_blue_sum += tmp[k][l].rgbtBlue * gx;
                        gy_blue_sum += tmp[k][l].rgbtBlue * gy;
                    }
                }
            }

            int r = round(sqrt(pow(gx_red_sum, 2) + pow(gy_red_sum, 2)));
            int g = round(sqrt(pow(gx_green_sum, 2) + pow(gy_green_sum, 2)));
            int b = round(sqrt(pow(gx_blue_sum, 2) + pow(gy_blue_sum, 2)));

            if (r > 255)
            {
                r = 255;
            }

            if (g > 255)
            {
                g = 255;
            }

            if (b > 255)
            {
                b = 255;
            }

            image[i][j].rgbtRed = r;
            image[i][j].rgbtGreen = g;
            image[i][j].rgbtBlue = b;
        }
    }
}