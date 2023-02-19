#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./volume IMAGE\n");
        return 1;
    }

    // Open files
    FILE *memory = fopen(argv[1], "r");
    if (memory == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    uint8_t block[512];
    int open = 0;
    int numF = 0;
    char filename[8];
    FILE *output = NULL;
    while (fread(block, sizeof(uint8_t), 512, memory) == 512) // while-loop runs until end of file
    {
        // check for starting of a JPEG file
        if (block[0] == 0xff && block[1] == 0xd8 && block[2] == 0xff && (block[3] & 0xf0) == 0xe0)
        {
            // if one file open, close it first
            if (open == 1)
            {
                fclose(output);
                open = 0;
                numF++;
            }
            sprintf(filename, "%03i.jpg", numF);
            output = fopen(filename, "w");
            if (output == NULL)
            {
                printf("Could not open file.\n");
                return 1;
            }
            open = 1;
            fwrite(block, sizeof(uint8_t), 512, output);
        }
        // if not start of the new JPEG file, write into the current open file
        else
        {
            if (open == 1)
            {
                fwrite(block, sizeof(uint8_t), 512, output);
            }
        }
    }
    // close the last JPEG file
    fclose(output);
}

