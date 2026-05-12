def count_runs(n):
    binary = f'{n:b}'
    total_runs = 0
    cur_one = False
    for i in binary:
        if i == '1' and cur_one == False:
            cur_one = True
            total_runs += 1
        if i == '0':
            cur_one = False

    return total_runs

def count_runs_2(n):
    binary = f'{n:b}'
    binary = binary.split('0')
    print(binary)
    total_runs = 0
    for i in binary:
        if '1' in i:
            total_runs += 1
    return total_runs

print(f'{100:b}', count_runs_2(100), 'runs')