# Written by *** for COMP9021

# Words in literary extracts are compared with a dictionary.
#
# You are given:
# - a file dictionary.txt containing one dictionary word per line;
# - a directory whose name is provided as an argument to the function;
# - that directory contains subdirectories only;
# - each subdirectory is named after an author;
# - each author directory contains one or more .txt files;
# - each such file is named after a work by that author;
# - each file contains a short extract from that work;
# - there are no deeper levels of subdirectories to explore.
#
# Write a function least_conformist_texts(directory_name) that:
# - reads all words from dictionary.txt;
# - scans all .txt files contained in the author subdirectories of directory_name;
# - extracts words from each file;
# - compares them with the dictionary;
# - computes, for each file:
#       total number of words
#       number of valid words
#       number of invalid words
#       nonconformity = invalid_words / total_words
# - prints the results grouped by author, in alphabetical order of authors;
# - for each author, prints works in alphabetical order of file name;
# - determines the least conformist work;
# - determines the least conformist author;
# - prints both.
#
# A word is defined as a sequence of letters only (A-Z or a-z),
# provided that it is delimited by separators.
#
# The only separators are:
# - space, newline, tab
# - the punctuation characters: . , ; : ! ? ( ) "
#
# Any token that contains a character other than a letter
# must be ignored entirely.
#
# In particular:
# - tokens containing an apostrophe (') are ignored;
# - tokens containing a hyphen (-) are ignored;
# - tokens containing a digit are ignored.
#
# This means for instance that:
# - "airport." contains the word airport
# - "Alice," contains the word Alice
# - "don't" is ignored
# - "well-known" is ignored
# - "X-37" is ignored
#
# The input files may contain apostrophes and hyphens.
# However, single quotes are not used as quotation marks;
# quoted text, when present, is always enclosed in double quotes.
#
# Comparisons with the dictionary are case-insensitive:
# words extracted from text files must be converted to uppercase
# before being looked up in the dictionary.
#
# If a file contains no words at all, then its nonconformity is defined to be 0.
#
# The least conformist work is the one with the highest nonconformity.
# If two WORKS have the same nonconformity, then:
# - the one with more invalid words is considered less conformist;
# - if there is still a tie, then the alphabetically smaller path
#   author_name/file_name is chosen.
#
# The least conformist author is determined by combining all words
# from all that author's files:
# - total words for the author
# - total valid words for the author
# - total invalid words for the author
# - author nonconformity = total_invalid / total_words
#
# If two AUTHORS have the same nonconformity, then:
# - the one with more invalid words is considered less conformist;
# - if there is still a tie, then the alphabetically smaller author name
#   is chosen.
#
# The output must have the following form:
# AuthorName:
#   work_name.txt:
#     words: ...
#     valid: ...
#     invalid: ...
#     nonconformity: ...
#
# After all authors and works have been printed, the program must print:
# LEAST CONFORMIST WORK
#   AuthorName/work_name.txt
#   nonconformity: ...
#
# LEAST CONFORMIST AUTHOR
#   AuthorName
#   nonconformity: ...
#
# Nonconformity must always be printed with exactly two digits after
# the decimal point.
#
# Formatting requirements:
# - There must be no blank line between works of the same author.
# - There must be exactly one blank line between two authors.
# - There must be exactly one blank line before "LEAST CONFORMIST WORK".
# - There must be exactly one blank line before "LEAST CONFORMIST AUTHOR".
#
# Important:
# The function least_conformist_texts(directory_name) must use the
# directory name provided as argument to locate and process files.
# In particular:
# - absolute paths must NOT be used;
# - hard-coded directory names must NOT be used;
# - all file accesses must be performed relative to directory_name.
#
# Any submission that does not correctly use the provided directory_name
# argument will fail the tests.
#
# Submissions that fail due to incorrect handling of paths will NOT be
# reconsidered or reassessed.
#
# Example:
# least_conformist_texts('A literary hierarchy') prints:
# Carroll:
#   alice.txt:
#     words: 123
#     valid: 89
#     invalid: 34
#     nonconformity: 0.28
#   looking_glass.txt:
#     words: 100
#     valid: 80
#     invalid: 20
#     nonconformity: 0.20
# 
# Wilde:
#   dorian_gray.txt:
#     words: 97
#     valid: 75
#     invalid: 22
#     nonconformity: 0.23
#   happy_prince.txt:
#     words: 94
#     valid: 79
#     invalid: 15
#     nonconformity: 0.16
#   importance_of_being_earnest.txt:
#     words: 78
#     valid: 58
#     invalid: 20
#     nonconformity: 0.26
# 
# LEAST CONFORMIST WORK
#   Carroll/alice.txt
#   nonconformity: 0.28
# 
# LEAST CONFORMIST AUTHOR
#   Carroll
#   nonconformity: 0.24


from pathlib import Path
import re

# POSSIBLY DEFINE OTHER FUNCTIONS

def get_less_conformity(current, best_so_far):
    if best_so_far is None:
            return current
        
    curr_nonconf, curr_invalid, curr_name = current
    best_nonconf, best_invalid, best_name = best_so_far

    # 1. Primary: Higher nonconformity
    if curr_nonconf > best_nonconf:
        return current
    if curr_nonconf < best_nonconf:
        return best_so_far

    # 2. Tie-breaker: More invalid words
    if curr_invalid > best_invalid:
        return current
    if curr_invalid < best_invalid:
        return best_so_far

    # 3. Final tie-breaker: Alphabetically smaller name
    if curr_name < best_name:
        return current
    return best_so_far   

def printing(work_file, work_total, work_valid, work_invalid, work_nonconformity):
    print(f'  {work_file.name}:')
    print(f'    words: {work_total}')
    print(f'    valid: {work_valid}')
    print(f'    invalid: {work_invalid}')
    print(f'    nonconformity: {work_nonconformity:.2f}')

def least_conformist_texts(directory_name):
    dictionary_path = Path('dictionary.txt')
    if not dictionary_path.exists():
        return
    
    with open(dictionary_path, 'r', encoding='utf-8') as f:
        valid_word_set = {line.strip().upper() for line in f}

    root = Path(directory_name)

    best_work = None
    best_author = None

    for author_dir in sorted(root.iterdir()):
        if not author_dir.is_dir():
            continue

        author_name = author_dir.name
        author_total = 0
        author_valid = 0
        author_invalid = 0

        print(f'{author_name}:')

        for work_file in sorted(author_dir.glob('*.txt')):
            separators = r'[ \n\t.,:;!?()"]'
            token = re.split(separators, work_file.read_text())
            valid_extracted_words = []
            for t in token:
                if not t: continue
                if t.isalpha():
                    valid_extracted_words.append(t.upper())


            work_total = len(valid_extracted_words)
            work_valid = sum(1 for w in valid_extracted_words if w in valid_word_set)
            work_invalid = work_total - work_valid
            work_nonconformity = work_invalid / work_total if work_total != 0 else 0
            
            author_total += work_total
            author_valid += work_valid
            author_invalid += work_invalid

            current_path = f"{author_name}/{work_file.name}"

            best_work = get_less_conformity((work_nonconformity, work_invalid, current_path), best_work)
            printing(work_file, work_total, work_valid, work_invalid, work_nonconformity)
        print()
        best_author = get_less_conformity((author_invalid / author_total if author_total != 0 else 0, author_invalid, author_name), best_author)

    print('LEAST CONFORMIST WORK')
    print(f'  {best_work[2]}')
    print(f'  nonconformity: {best_work[0]:.2f}')
    print()
    print('LEAST CONFORMIST AUTHOR')
    print(f'  {best_author[2].split('/')[0]}')
    print(f'  nonconformity: {best_author[0]:.2f}')




                

least_conformist_texts('Another literary hierarchy')  

    # REPLACE THE PASS STATEMENT ABOVE WITH YOUR CODE
