from itertools import chain
from random import seed, shuffle
from collections import defaultdict

# INSERT YOUR CODE HERE
def get_card_unicode(card_index):
    suit_offsets = {0: 0x1F0B1, 1: 0x1F0C1, 2: 0x1F0D1, 3: 0x1F0A1}
    suit = card_index // 13
    rank = card_index % 13
    unicode_val = suit_offsets[suit] + rank + (1 if rank >= 11 else 0)
    return chr(unicode_val)

def format_stack_line(stacks):

    parts = []
    for s in stacks:
        if not s:
            parts.append("")
        else:
            display = "[" * (len(s) - 1) + get_card_unicode(s[-1])
            parts.append(display)
    
    res = "    " + parts[0].ljust(15) + parts[1].ljust(15) + parts[2].ljust(15) + parts[3]
    return res.rstrip()

def get_suit_and_rank(card):
    return card // 13, card % 13

def try_place_card(face_up_pile, inc_stacks, dec_stacks):
    if not face_up_pile:
        return False
    
    card = face_up_pile[-1]
    suit, rank = get_suit_and_rank(card)

    # RULE 1: start stack with Ace or King
    if rank == 0: # Ace
        inc_stacks[suit].append(face_up_pile.pop())
        return "Starting a stack."
    if rank == 12: # King
        dec_stacks[suit].append(face_up_pile.pop())
        return "Starting a stack."
    
    # RULE 2: extend existing stacks
    if inc_stacks[suit] and rank == (inc_stacks[suit][-1] % 13) + 1:
        inc_stacks[suit].append(face_up_pile.pop())
        return "Extending an increasing stack."
    
    if dec_stacks[suit] and rank == (dec_stacks[suit][-1] % 13) - 1:
        dec_stacks[suit].append(face_up_pile.pop())
        return "Extending a decreasing stack."
    
    # ROUND END CONDITION: if no card is placed, lose immediately
    return False

def placeholder(n):
    return f"{n}st" if n == 1 else f"{n}nd" if n == 2 else f"{n}rd" if n == 3 else f"{n}th"

def append_state(output_list, deck, face_up_pile, inc, dec, message=""):
    if message:
        output_list.append(message)
    
    output_list.append("]" * len(deck))
    
    if face_up_pile:
        output_list.append("[" * (len(face_up_pile) - 1) + get_card_unicode(face_up_pile[-1]))
    else:
        output_list.append("")
        
    inc_line = format_stack_line(inc)
    if inc_line: 
        output_list.append(inc_line)
    else: output_list.append("")
    
    dec_line = format_stack_line(dec)
    if dec_line: 
        output_list.append(dec_line)
    else: output_list.append("")
    
    output_list.append("") # Every state followed by an empty line

def play_game(seed_input):
    
    deck = list(range(52))
    seed(seed_input)
    shuffle(deck)
    deck.reverse()

    inc_stacks = [[] for _ in range(4)]
    dec_stacks = [[] for _ in range(4)]
    face_up_pile = []

    current_round_output = []
    current_round_output.append("\nDeck shuffled. Ready to start!")
    current_round_output.append("]" * 52)
    current_round_output.append("")

    round_num = 1

    while True:

        current_round_output.append(f"Starting the {placeholder(round_num)} round...")
        current_round_output.append("")

        card_placed_this_round = 0

        while True:
            res = try_place_card(face_up_pile, inc_stacks, dec_stacks)

            if res:
                card_placed_this_round += 1
                append_state(current_round_output, deck, face_up_pile, inc_stacks, dec_stacks, res)

                if sum(len(s) for s in inc_stacks + dec_stacks) == 52:
                    print("\nYou placed all cards. You won! 😀")
                    return 0, current_round_output
                continue

            if deck:
                num_to_draw = min(3, len(deck))
                for _ in range(num_to_draw):
                    face_up_pile.append(deck.pop(0))
                append_state(current_round_output, deck, face_up_pile, inc_stacks, dec_stacks)
                continue
            
            break

        if card_placed_this_round > 0 and face_up_pile:
            deck = list(face_up_pile)
            face_up_pile = []
            round_num += 1

        else:
            unplaced_cards = 52 - sum(len(s) for s in inc_stacks + dec_stacks)
            if unplaced_cards > 0:
                print(f"\nYou could not place {unplaced_cards} cards. You lost! 😞")
            else:
                print("\nYou could not place any cards. You lost! 😞")
            return unplaced_cards, current_round_output


def process_query(query, collected_output):
    total = len(collected_output)
    raw_query = query 
    query = raw_query.strip()

    if not query:
        return False
    if query == 'q':
        return True 
    if query == 'Q':
        return False

    # Check for Range: m--n (Strictly two dashes)
    if "--" in query and "---" not in query and "+" not in query:
        try:
            parts = query.split("--")
            if len(parts) == 2:
                m = int(parts[0].strip())
                n = int(parts[1].strip())
                if 1 <= m <= n <= total:
                    for i in range(m - 1, n):
                        print(collected_output[i])
                    # print() # Empty line after block 
        except ValueError:
            pass

    # Check for Single Integer
    else:
        try:
            # Reject "+1" and "- 4" 
            if query.startswith('+') or " " in query:
                return False
            
            val = int(query)
            if 1 <= val <= total:
                for i in range(val):
                    print(collected_output[i])
                # print() 
            elif -total <= val <= -1:
                # Calculate start index for last n lines 
                print() 
                for i in range(total + val, total):
                    print(collected_output[i])
        except ValueError:
            pass
            
    return False

def start_interactive_session(collected_output):
    total = len(collected_output)
    print(f"\nThere are {total} lines of output. What do you want me to do?")
    
    # Exact spaces to align cursor under 'q' 
    prompt = (
        "\nEnter: q to quit\n"
        "       a last line number (between 1 and {0})\n"
        "       a first line number (between -1 and -{0})\n"
        "       a range of line numbers (of the form m--n with 1 <= m <= n <= {0})\n"
        "       " 
    ).format(total)

    while True:
        try:
            # Use real input() for the actual assignment 
            user_input = input(prompt)
            if process_query(user_input, collected_output):
                break
        except EOFError:
            break


def simulation_games(seed_input):
    
    deck = list(range(52))
    seed(seed_input)
    shuffle(deck)
    deck.reverse()

    inc_stacks = [[] for _ in range(4)]
    dec_stacks = [[] for _ in range(4)]
    face_up_pile = []

    round_num = 1

    while True:

        card_placed_this_round = 0

        while True:
            res = try_place_card(face_up_pile, inc_stacks, dec_stacks)

            if res:
                card_placed_this_round += 1

                if sum(len(s) for s in inc_stacks + dec_stacks) == 52:
                    return 0
                continue

            if deck:
                num_to_draw = min(3, len(deck))
                for _ in range(num_to_draw):
                    face_up_pile.append(deck.pop(0))
                continue
            
            break

        if card_placed_this_round > 0 and face_up_pile:
            deck = list(face_up_pile)
            face_up_pile = []
            round_num += 1

        else:
            unplaced_cards = 52 - sum(len(s) for s in inc_stacks + dec_stacks)
            return unplaced_cards

def simulate(n, i):
    results = {}

    for g in range(n):
        unplaced = simulation_games(i + g)
        results[unplaced] = results.get(unplaced, 0) + 1

    print("Number of cards left | Relative frequency")
    print("-" * 41)

    for k in sorted(results.keys(), reverse=True):
        percentage = (results[k] / n) * 100
        print(f"{k:>20} | {percentage:>17.2f}%")

if __name__ == "__main__":
    try:
        seed_input = int(input("Enter an integer to pass to the seed() function: "))
        unplaced_cards, round_output = play_game(seed_input)
        round_output.pop()  
        start_interactive_session(round_output)
    except (EOFError, ValueError):
        pass


def start_query(collected_output):
    total = len(collected_output)
    print(f"\nThere are {total} lines of output. What do you want me to do?")
    
    # Note the spaces at the end of the last line for alignment
    prompt = (
        "\nEnter: q to quit\n"
        "       a last line number (between 1 and {0})\n"
        "       a first line number (between -1 and -{0})\n"
        "       a range of line numbers (of the form m--n with 1 <= m <= n <= {0})\n"
        "       "
    ).format(total)

    while True:
        choice = input(prompt).strip()
        if choice == 'q':
            break

        # Handle m--n
        if "--" in choice:
            try:
                m, n = map(int, choice.split("--"))
                if 1 <= m <= n <= total:
                    for i in range(m-1, n):
                        print(collected_output[i])

                    # break # ONLY FOR DEBUGGING, REMOVE AFTER TESTING
            except ValueError:
                pass
        # Handle single line or negative index
        else:
            try:
                val = int(choice)
                if 1 <= val <= total: # Positive: first val lines
                    for i in range(val):
                        print(collected_output[i])
                elif -total <= val <= -1: # Negative: last |val| lines
                    for i in range(total + val, total):
                        print(collected_output[i])

            except ValueError:
                pass
