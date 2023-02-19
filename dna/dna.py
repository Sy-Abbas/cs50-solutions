import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py DATABASEFILE SEQUENCEFILE")

    # Read database file into a variable
    data = []
    with open(sys.argv[1], "r") as file:
        reader = csv.reader(file)
        for row in reader:
            a = []
            for x in row:
                a.append(x)
            data.append(a)

    # Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as file:
        se = file.readline()

    # Find longest match of each STR in DNA sequence
    dna = ["Values"]
    for x in range(1, len(data[0])):
        num = str(longest_match(se, data[0][x]))
        dna.append(num)

    # Check database for matching profiles
    for y in range(1, len(data)):
        match = True
        for v in range(1, len(data[0])):
            if data[y][v] != dna[v]:
                match = False
                break
        if (match == True):
            print(data[y][0])
            return
    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
