# Creates a directory named First_10_words_per_letter with the
# following structure:
#   - a subdirectory Vowels
#   - a subdirectory Consonants
#
# For each uppercase letter:
#   - creates a file named <letter>.txt in Vowels if the letter is
#     a vowel (A, E, I, O, U, Y), and in Consonants otherwise;
#   - writes in that file the first 10 words from dictionary.txt
#     that start with that letter, in the order in which they
#     appear in the file.
#
# A directory named First_10_words_per_letter_sol contains a
# hierarchy with the same structure; it is provided for reference
# only and must not be used programmatically.

import os
from pathlib import Path
from string import ascii_uppercase

# INSERT YOUR CODE HERE
