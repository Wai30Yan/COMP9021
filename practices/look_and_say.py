from itertools import groupby

def look_and_say(d, n):
    result = str(d)

    for _ in range(n):
        result = ''.join(f"{len(list(group))}{key}" for key, group in groupby(result))
        print(result)


look_and_say(0, 10)