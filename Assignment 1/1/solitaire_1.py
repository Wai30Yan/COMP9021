from random import seed, shuffle

def get_card_unicode(card_index):
    suit_offsets = {0: 0x1F0B1, 1: 0x1F0C1, 2: 0x1F0D1, 3: 0x1F0A1}
    suit = card_index // 13
    rank = card_index % 13
    unicode_val = suit_offsets[suit] + rank + (1 if rank >= 11 else 0)
    return chr(unicode_val)

def print_layout(layout):

    for row in range(4):
        line = ""
        for col in range(4):
            idx = row * 4 + col  # Fill left-to-right, top-to-bottom
            card = layout[idx]
            line += "\t"
            if card != ' ':
                line += get_card_unicode(card)
            else:
                line += ' '  # Space for removed cards
        print(line.rstrip()) # No trailing spaces

def play_solitaire(seed_input):

    deck = list(range(52))
    total_removed = 0
    round_names = ["first", "second", "third", "fourth"]

    print("\nDeck shuffled. Ready to start!")

    for r_idx in range(4):
        deck.sort()
        seed(seed_input + r_idx)
        shuffle(deck)
        deck.reverse()

        if r_idx == 0:
            print("]" * 52)
            print(f"\nStarting the {round_names[r_idx]} round...") #
        else:
            print(f"\nAfter shuffling, starting the {round_names[r_idx]} round...")

        layout = [deck.pop(0) for _ in range(16)]

        print(f"\nDrawing 16 cards:\n{']' * len(deck)}")

        print_layout(layout)

        while True:
            pic_indices = [i for i, c in enumerate(layout) if c is not None and c % 13 >= 10]

            if not pic_indices:
                break

            num_rem = len(pic_indices)
            total_removed += num_rem

            
            for idx in pic_indices:
                layout[idx] = ' '

            print(f"\nRemoving {num_rem} picture card{'s' if num_rem > 1 else ''}:")

            print_layout(layout)
        
            if total_removed == 12:
                break
            
            to_draw = min(len(deck), num_rem)

            for i in range(to_draw):
                layout[pic_indices[i]] = deck.pop(0)

            print(f"\nDrawing {to_draw} card{'s' if to_draw > 1 else ''}:\n{']' * len(deck)}")

            print_layout(layout)

        if total_removed == 12:
            print("\nYou removed all picture cards. You won! 😀") 
            return
        
        deck += [c for c in layout if c is not None]

    # Final Result Messages
    if total_removed == 0:
        print("\nYou removed no picture cards. You lost! 😞")
    elif total_removed < 12:
        print(f"\nYou removed only {total_removed} picture card{'s' if total_removed > 1 else ''}. You lost! 😞")

def game_for_simulations(seed_input):

    total_removed = 0
    deck = list(range(52))
    for round in range(4):
        seed(seed_input + round)
        deck.sort()
        shuffle(deck)
        deck.reverse()
        layout = [deck.pop(0) for _ in range(16)]

        while True:
            pic_indices = [i for i, c in enumerate(layout) if c is not None and c % 13 >= 10]

            if not pic_indices:
                break

            num_rem = len(pic_indices)
            total_removed += num_rem

            if total_removed == 12:
                return total_removed
            
            for idx in pic_indices:
                layout[idx] = ' '
        
            to_draw = min(len(deck), num_rem)

            for i in range(to_draw):
                layout[pic_indices[i]] = deck.pop(0)

        if total_removed == 12:
            print("\nYou removed all picture cards. You won! 😀") #
        
        deck += [c for c in layout if c != ' ']

    # End of Game
    return total_removed


def simulate(n, i):
    results = {}
    for game in range(n):
        seed_value = i + game

        total_removed = game_for_simulations(seed_value)
        results[total_removed] = results.get(total_removed, 0) + 1

    if not results:
        pass
    else:
        print("Number of picture cards removed | Relative frequency")
        print("-" * 52)
        for k in sorted(results.keys()):
            freq = (results[k] / n) * 100
            # Right-aligned with specific widths [cite: 136]
            print(f"{str(k).rjust(31)} | {format(freq, '.2f').rjust(17)}%")
        

if __name__ == "__main__":

    try:
        prompt = "Enter an integer to pass to the seed() function: "
        seed_input = int(input(prompt))
        play_solitaire(seed_input)
        # simulate(10, 6)
        # simulate(500, 11)
    except (EOFError, ValueError):
        exit()
    # play_solitaire()