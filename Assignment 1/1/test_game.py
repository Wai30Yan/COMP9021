import random


colours = 'spades', 'hearts', 'diamonds', 'clubs'

first_ace_code_point = 0x1F0A1

suit = range(14)

def default_suit_order(colour):
    return suit if colour in {'spades', 'diamonds'} else reversed(suit)

L = [(i, j, k) for i in 'abcd' if i in 'ac'
                   for j in '123'
                       for k in 'ABCD' if k in 'BD']



deck = [chr(first_ace_code_point + i * 16 + j) for i in (0, 2, 3, 1)
            for j in default_suit_order(colours[i])]


import random

def get_card_unicode(card_index):
    # Mapping based on assignment: 0-12 Hearts, 13-25 Diamonds, 26-38 Clubs, 39-51 Spades
    # Unicode block offsets: Hearts 0x1F0B1, Diamonds 0x1F0C1, Clubs 0x1F0D1, Spades 0x1F0A1
    suit_offsets = {0: 0x1F0B1, 1: 0x1F0C1, 2: 0x1F0D1, 3: 0x1F0A1}
    
    suit_id = card_index // 13
    rank = card_index % 13
    
    # SAFETY CHECK: The Unicode standard has a 'Knight' card between Jack and Queen.
    # To correctly map Rank 11 (Queen) and 12 (King), we must skip that position.
    unicode_rank_offset = rank + (1 if rank >= 11 else 0)
    
    return chr(suit_offsets[suit_id] + unicode_rank_offset)

def print_layout(layout):
    for row in range(4):
        line = ""
        for col in range(4):
            idx = row * 4 + col
            card = layout[idx]
            # Spacing rule: Exactly one tab before every card or vacancy
            line += "\t"
            if card is not None:
                line += get_card_unicode(card)
        print(line.rstrip())

# --- THE PROCESS FOR SEED 7 ---
# 1. Start with a sorted list of integers
deck = list(range(52))
deck.sort() 

# 2. Apply seed and shuffle
random.seed(0)
random.shuffle(deck)
deck.reverse()
print(deck) # Show the shuffled deck in reverse order
# 3. Draw the first 16 cards
layout = [deck.pop(0) for _ in range(16)]

print("Drawing 16 cards:")
print("]" * len(deck))
print_layout(layout)