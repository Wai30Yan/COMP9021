# Written by *** for COMP9021


# Write a function ribbon(n) that prints a 4-line ASCII pattern.
#
# The argument n is an integer with n >= 2.
#
# The output must consist of exactly four lines,
# formatted exactly as shown in the example below.
#
# There must be:
# • no leading spaces on any line
# • no trailing spaces on any line
#
# Example: for n = 3, the output should be:
# <<=..==..=>>
# |\/||\/||\/|
# |/\||/\||/\|
# <<=  ==  =>>
#
# Your function must work for any valid value of n.
#
# Hint: Use string operations; loops are not required.


def ribbon(n):
    print('<<=' + ('..==' * (n - 2)) + '..=>>')
    print('|\/|' * n)
    print('|/\|' * n)
    print('<<=' + '  ==' * (n - 2) + '  =>>')

# ------------------------------------------------------------

# You are given a text file containing contact entries.
#
# Each valid (non-blank) line contains exactly three fields
# separated by semicolons:
#
#  FamilyName;GivenNames;Phone
#
# The first field (FamilyName) has no leading space
# and contains no spaces.
# The second field (GivenNames) may contain several names
# separated by single spaces.
#
# The third field (Phone):
#   • may begin with spaces or tabs
#   • after any leading whitespace, has the form:
#       +CC-XXXX-YYYY
#   • has no trailing space
#
# Some lines in the file may be blank.
# Blank lines may contain spaces or tabs.
#
# Write a function phonebook(filename) that:
#   • reads the file line by line
#   • skips blank lines
#   • prints one line per valid entry in the format:
#
#       FamilyName,FirstGiven -> CCXXXXYYYY
#
# where:
#   • FirstGiven is the first word in GivenNames
#   • CCXXXXYYYY is the phone number with '+' and '-' removed
#
# The output must:
#   • appear in the same order as the input
#   • contain no leading nor trailing spaces
#   • use exactly one space before and after '->'
#
# Your solution should work for any valid input file,
# not just the example provided.
#
# Hint: split(), isspace(), join(), and sequence indexing
# are sufficient.


def phonebook(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    
    for line in lines:
        if not line.isspace():
            L = line.split(';')
            print(L[0] + ',' + L[1].split()[0] + ' -> ' + L[2].strip().replace('+', '').replace('-', ''))
            
    # REPLACE THE PASS STATEMENT ABOVE WITH YOUR CODE

phonebook('contacts.txt')

# print('Daniel James'.split()[0])