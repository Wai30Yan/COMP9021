from string import ascii_uppercase

def letter_pascal(n):
    current_row = [1]
    alpha_row = ['A']
    for i in range(n):
        next_row = [1]
        for k in range(len(current_row)-1):
            next_row.append(current_row[k] + current_row[k+1])
        next_row.append(1)
        current_row = next_row
        print(' ' * (n-i-1), end='')
        print(' '.join(i for i in alpha_row))
        alpha_row = []
        for i in current_row:
            alpha_row.append(ascii_uppercase[(i-1)%26])


letter_pascal(1)
