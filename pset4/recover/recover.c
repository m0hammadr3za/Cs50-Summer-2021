#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    FILE *file = fopen("card.raw", "r");
    if (file == NULL)
    {
        printf("File can not be opend!\n");
        return 1;
    }

    int img_found_count = 0;
    FILE *img = NULL;
    BYTE buffer[512];

    while(!(fread(buffer, sizeof(BYTE), 512, file) < 512))
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (img_found_count > 0)
            {
                fclose(img);
            }

            char filename[8];
            sprintf(filename, "%03i.jpg", img_found_count);
            img = fopen(filename, "w");
            fwrite(buffer, sizeof(BYTE), 512, img);
            img_found_count++;
        }
        else
        {
            if (img_found_count > 0)
            {
                fwrite(buffer, sizeof(BYTE), 512, img);
            }
        }
    }


    fclose(img);
    fclose(file);
}