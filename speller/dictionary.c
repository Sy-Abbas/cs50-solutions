// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <strings.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Choose number of buckets in hash table
const unsigned int N = 26;
unsigned int num = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int index = hash(word);
    node *cur = table[index];
    while (cur != NULL)
    {
        if (strcasecmp(cur->word, word) == 0)
        {
            return true;
        }
        else
        {
            cur = cur->next;
        }
    }
    // printf("MISSPELLED WORDS");
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        printf("Could not open file.\n");
        return false;
    }
    char word[46];
    while (fscanf(dict, "%s", word) != EOF)
    {
        node *newWord = malloc(sizeof(node));
        if (newWord == NULL)
        {
            printf("Error has occured!\n");
            return false;
        }
        strcpy(newWord->word, word);
        newWord->next = NULL;
        int index = hash(newWord->word);
        newWord->next = table[index];
        table[index] = newWord;
        num++;
    }
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return num;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *c = table[i];
        while (c != NULL)
        {
            node *temp = c;
            c = c->next;
            free(temp);
        }
    }
    return true;
}
