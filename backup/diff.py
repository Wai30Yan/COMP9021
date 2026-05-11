# Insert your code in this file
import re

def extract_lines(file1, file2):
    list1, list2 = [], []

    with open(file1) as f:
        for line in f.readlines():
            list1.append(line.rstrip())

    with open(file2) as f:
        for line in f.readlines():
            list2.append(line.rstrip())

    return list1, list2

def longest_common_subsequence(file1, file2):
    list1, list2 = extract_lines(file1, file2)
    m, n = len(list1), len(list2)

    dp = [[0] * (n+1) for _ in range(m+1)]

    for i in range(1, m+1):
        for j in range(1, n+1):
            if list1[i-1] == list2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    i, j = m, n

    new_list = []
    while i > 0 and j > 0:
        if list1[i-1] == list2[j-1]:
            new_list.append(list1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    
    return list1, list2, list(reversed(new_list))

def get_transformations(file1, file2, lcs):
    i, j, k = 0, 0, 0
    m, n = len(file1), len(file2)
    ops = []
    while i < m or j < n:
        next_lcs = lcs[k] if k < len(lcs) else None
        start_i, start_j = i, j

        while i < m and (next_lcs is None or file1[i] != next_lcs):
            i += 1
        while j < n and (next_lcs is None or file2[j] != next_lcs):
            j += 1

        if i > start_i or j > start_j:
            f1_range = f'{start_i + 1}' if i == start_i + 1 else f'{start_i + 1},{i}'
            f2_range = f'{start_j + 1}' if j == start_j + 1 else f'{start_j + 1},{j}'

            if i > start_i and j > start_j:
                print(f'{f1_range}c{f2_range}')
                ops.append(f'{f1_range}c{f2_range}')
                # for line in file1[start_i : i]: print(f'< {line}')
                # print('---')
                # for line in file2[start_j : j]: print(f'> {line}')

            elif i > start_i:
                print(f'{f1_range}d{j}')
                ops.append(f'{f1_range}d{j}')
                # for line in file1[start_i : i]: print(f'< {line}')

            elif j > start_j:
                print(f'{i}a{f2_range}')
                ops.append(f'{i}a{f2_range}')
                # for line in file2[start_j : j]: print(f'> line')
        
        if k < len(lcs):
            i += 1
            j += 1
            k += 1
    return ops

# list1, list2, lcs = longest_common_subsequence('file_3_1.txt', 'file_3_2.txt') 
# get_transformations(list1, list2, lcs)

class DiffCommandsError(Exception):
    pass

class DiffCommands:
    def __init__(self, filename):
        self.file = filename
        self.commands = []

        pattern = re.compile(r'^(\d+)(?:,(\d+))?([adc])(\d+)(?:,(\d+))?$')
        
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()

                if not lines:
                    raise DiffCommandsError("Cannot possibly be the commands for the diff of two files")

                for line in lines:
                    line = line.rstrip()

                    if not line or ' ' in line or not pattern.match(line):
                        raise DiffCommandsError("Cannot possibly be the commands for the diff of two files")
                    
                    self.commands.append(line)
        except FileNotFoundError:
            raise


    def __str__(self):
        return '\n'.join(self.commands)



class OriginalNewFiles:

    def __init__(self, path_file1, path_file2):
        self.file1 = self._read_file(path_file1)
        self.file2 = self._read_file(path_file2)
        self.m, self.n = len(self.file1), len(self.file2)
        self.dp = self._build_dp()

    def _read_file(self, path):
        with open(path, 'r') as f:
            return [line.rstrip('\n') for line in f]
        
    def _build_dp(self):
        dp = [[0] * (self.n+1) for _ in range(self.m+1)]

        for i in range(1, self.m + 1):
            for j in range(1, self.n + 1):
                if self.file1[i-1] == self.file2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

        return dp

    def is_valid_diff(self, diff_obj):
        try:
            return self._verify_commands(diff_obj.commands)
        except:
            return False
        
    def _verify_commands(self, commands):
        current_file = list(self.file1)
        offset = 0 

        for cmd in commands:
            match = re.match(r'^(\d+)(?:,(\d+))?([adc])(\d+)(?:,(\d+))?$', cmd)
            s1, e1, op, s2, e2 = match.groups()
            
            # 1-based to 0-based
            s1, e1 = int(s1) - 1, int(e1 or s1)
            s2, e2 = int(s2) - 1, int(e2 or s2)

            if op == 'd':
                del current_file[s1 + offset : e1 + offset]
                offset -= (e1 - s1)
            elif op == 'a':
                to_add = self.file2[s2 : e2]
                current_file[s1 + offset + 1 : s1 + offset + 1] = to_add
                offset += (e2 - s2)
            elif op == 'c':
                current_file[s1 + offset : e1 + offset] = self.file2[s2 : e2]
                offset += (e2 - s2) - (e1 - s1)

        return current_file == self.file2

    def print_diff(self, diff_obj):
        for cmd in diff_obj.commands:
            print(cmd)
            self._print_cmd_content(cmd)

    def _print_cmd_content(self, cmd):
        match = re.match(r'^(\d+)(?:,(\d+))?([adc])(\d+)(?:,(\d+))?$', cmd)
        s1, e1, op, s2, e2 = match.groups()
        
        s1, e1 = int(s1) - 1, int(e1 or s1)
        s2, e2 = int(s2) - 1, int(e2 or s2)

        if op == 'd':
            for i in range(s1, e1):
                print(f"< {self.file1[i]}")
        elif op == 'a':
            for j in range(s2, e2):
                print(f"> {self.file2[j]}")
        elif op == 'c':
            for i in range(s1, e1):
                print(f"< {self.file1[i]}")
            print("---")
            for j in range(s2, e2):
                print(f"> {self.file2[j]}")

    def print_unmodified_from_original(self, diff_obj):
        self._print_lcs_with_ellipsis(self.file1)
        # print(' prints the lines of the longest common subsequence as they appear in the original file')

    def print_unmodified_from_new(self, diff_obj):
        self._print_lcs_with_ellipsis(self.file2)
        # print('prints the lines of the longest common subsequence as they appear in the new file')
    
    def _get_one_lcs(self):
        i, j = self.m, self.n
        lcs = []
        while i > 0 and j > 0:
            if self.file1[i-1] == self.file2[j-1]:
                lcs.append(self.file1[i-1])
                i -= 1
                j -= 1
            elif self.dp[i-1][j] >= self.dp[i][j-1]:
                i -= 1
            else:
                j -= 1
        return list(reversed(lcs))
    
    def _print_lcs_with_ellipsis(self, target_file):
        lcs_set = self._get_one_lcs()
        in_lcs = [line in lcs_set for line in target_file]

        i = 0
        while i < len(target_file):
            if in_lcs[i]:
                print(target_file[i])
                i += 1
            else:
                print('...')
                while i < len(target_file) and not in_lcs[i]:
                    i += 1

    def all_diff_commands(self):
        all_paths = []
        self._find_all_paths(self.m, self.n, [], all_paths)

        results = []
        for path in all_paths:
            cmds = self._path_to_cmds(path)
            results.append(DiffCommands.from_list(cmds))

        return sorted(results, key=lambda x: str(x))
    
    def _path_to_cmds(self, path_indices):
        cmds = []
        last_i, last_j = 0, 0
        
        path_indices.append((self.m + 1, self.n + 1))
        
        for i, j in path_indices:
            if i > last_i + 1 or j > last_j + 1:
                cmds.append(self._format_hunk(last_i + 1, i - 1, last_j + 1, j - 1))
            last_i, last_j = i, j
        return cmds
       
    def _find_all_paths(self, i, j, cur_lcs, all_paths):
        if i == 0 or j == 0:
            all_paths.append(list(reversed(cur_lcs)))
            return

        if self.file1[i-1] == self.file2[j-1]:
            self._find_all_paths(i-1, j-1, cur_lcs + [self.file1[i-1]], all_paths)
        else:
            if self.dp[i-1][j] >= self.dp[i][j-1]:
                self._find_all_paths(i-1, j, cur_lcs, all_paths)
            
            if self.dp[i][j-1] >= self.dp[i-1][j]:
                self._find_all_paths(i, j-1, cur_lcs, all_paths)



    def _format_hunk(self, s1, e1, s2, e2):
        has_f1 = s1 <= e1
        has_f2 = s2 <= e2
        
        f1_r = f"{s1}" if s1 == e1 else f"{s1},{e1}"
        f2_r = f"{s2}" if s2 == e2 else f"{s2},{e2}"
        
        if has_f1 and has_f2: return f"{f1_r}c{f2_r}"
        if has_f1: return f"{f1_r}d{s2-1}"
        return f"{s1-1}a{f2_r}"
                

diff_1 = DiffCommands('diff_1.txt')
# print(diff_1)

diff_2 = DiffCommands('diff_2.txt')
# print(diff_2)

diff_3 = DiffCommands('diff_3.txt')
# print(diff_3)

files = OriginalNewFiles('file_1_1.txt', 'file_1_2.txt')

# print(files.is_valid_diff(diff_1))
# print(files.is_valid_diff(diff_2))
# print(files.is_valid_diff(diff_3))

# files.print_diff(diff_1)
# files.print_unmodified_from_original(diff_1)
# files.print_unmodified_from_new(diff_1)

files.all_diff_commands()


