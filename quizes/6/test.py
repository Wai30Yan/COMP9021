import re
from pathlib import Path

p = Path('.')
print('---------------')

def load_dictionary():
    with open('dictionary.txt', 'r', encoding='utf-8') as f:
        # Convert all to uppercase for case-insensitive comparison
        return {line.strip() for line in f}
    
def get_words_from_file(file_path):
    # Read text and handle the encoding issue we discussed earlier
    text = file_path.read_text(encoding='utf-8')
    
    # Replace separators with a space
    separators = r'[ \n\t.,;:!?()"]'
    tokens = re.split(separators, text)
    
    valid_extracted_words = []
    for t in tokens:
        if not t: continue # skip empty strings from split
        # Rule: Only letters A-Z or a-z. No digits, hyphens, or apostrophes.
        if t.isalpha():
            valid_extracted_words.append(t.upper())
            
    return valid_extracted_words

paths = [] 
with open('output.txt', 'w', encoding='utf-8') as f:
    for path_obj in p.rglob('*'):
        if path_obj.is_file():
            paths.append(path_obj)
            # content = get_words_from_file(path_obj)
            # print(content, file=f)
print(paths)
print('---------------')

            # if best_work is None or work_nonconformity > best_work[0]:
            #     best_work = (work_nonconformity, work_invalid, current_path)
            # else:
            #     if work_nonconformity > best_work[0]:
            #         best_work = (work_nonconformity, work_invalid, current_path)
            #     elif work_nonconformity == best_work[0]:
            #         if work_invalid == best_work[1]:
            #             if current_path < best_work[2]:
            #                 best_work = (work_nonconformity, work_invalid, current_path)