import re

class DiffCommandsError(Exception):
    pass

class DiffCommands:
    def __init__(self, filename):
        pattern = re.compile(r'^(\d+)(?:,(\d+))?([adc])(\d+)(?:,(\d+))?$')

        if isinstance(filename, list):
            self.commands = []
            for line in filename:
                if not pattern.match(line):
                    raise DiffCommandsError("Cannot possibly be the commands for the diff of two files")
                self.commands.append(line)
            return

        self.commands = []

        try:
            with open(filename, 'r') as f:
                lines = f.readlines()

                if not lines:
                    raise DiffCommandsError("Cannot possibly be the commands for the diff of two files")

                for line in lines:
                    line = line.rstrip('\n')  # important fix

                    if not line or ' ' in line:
                        raise DiffCommandsError("Cannot possibly be the commands for the diff of two files")

                    match = pattern.match(line)
                    if not match:
                        raise DiffCommandsError("Cannot possibly be the commands for the diff of two files")

                    # Optional but recommended: logical validation
                    l1, l2, op, r1, r2 = match.groups()

                    if l2 and int(l1) > int(l2):
                        raise DiffCommandsError("Cannot possibly be the commands for the diff of two files")
                    if r2 and int(r1) > int(r2):
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
        dp = [[0] * (self.n + 1) for _ in range(self.m + 1)]
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
            s1 = int(s1) - 1
            e1 = int(e1) - 1 if e1 else s1

            s2 = int(s2) - 1
            e2 = int(e2) - 1 if e2 else s2

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
            match = re.match(r'^(\d+)(?:,(\d+))?([adc])(\d+)(?:,(\d+))?$', cmd)
            s1, e1, op, s2, e2 = match.groups()
            
            # Convert to 0-based indexing and ranges
            r1_start, r1_end = int(s1), int(e1 or s1)
            r2_start, r2_end = int(s2), int(e2 or s2)

            if op in 'dc':
                for i in range(r1_start, r1_end + 1):
                    print(f"< {self.file1[i-1]}")
            if op == 'c':
                print("---") #
            if op in 'ac':
                for i in range(r2_start, r2_end + 1):
                    print(f"> {self.file2[i-1]}")

    def print_unmodified_from_original(self, diff_obj):
        self._print_unmodified(self.file1)

    def print_unmodified_from_new(self, diff_obj):
        self._print_unmodified(self.file2)

    def _get_lcs_lines(self):
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
        return lcs[::-1]
    
    def _print_unmodified(self, source_file):
        lcs = self._get_lcs_lines()
        if not lcs: return
        
        lcs_idx = 0
        in_gap = False
        for line in source_file:
            if lcs_idx < len(lcs) and line == lcs[lcs_idx]:
                if in_gap:
                    print("...")
                    in_gap = False
                print(line)
                lcs_idx += 1
            else:
                in_gap = True
        
        if in_gap:
            print("...")

    def all_diff_commands(self):
        if self.file1 == self.file2:
            return [DiffCommands([])]
        
        all_paths = []

        self._backtrack(self.m, self.n, [], all_paths, set())

        diff_objects = []
        for path in all_paths:
            formatted_cmds = self._format_path(path)
            diff_objects.append(DiffCommands(formatted_cmds))

        diff_objects.sort(key=lambda x: str(x))
        return diff_objects

    def _backtrack(self, i, j, current_path, all_paths, memo):
        if (i, j) in memo:
            return
        memo.add((i, j))

        if i == 0 and j == 0:
            all_paths.append(list(reversed(current_path)))
            return

        if i > 0 and j > 0 and self.file1[i-1] == self.file2[j-1]:
            current_path.append(('match', i, j))
            self._backtrack(i-1, j-1, current_path, all_paths, memo)
            current_path.pop()
            return

        if i > 0 and self.dp[i-1][j] == self.dp[i][j]:
            current_path.append(('delete', i, j))
            self._backtrack(i-1, j, current_path, all_paths, memo)
            current_path.pop()

        if j > 0 and self.dp[i][j-1] == self.dp[i][j]:
            current_path.append(('add', i, j))
            self._backtrack(i, j-1, current_path, all_paths, memo)
            current_path.pop()
    
    def _format_path(self, path):
        commands = []
        
        curr_i = 0  # position in file1
        curr_j = 0  # position in file2

        i = 0
        while i < len(path):
            if path[i][0] == 'match':
                curr_i += 1
                curr_j += 1
                i += 1
                continue

            start_i = curr_i
            start_j = curr_j

            deletes = 0
            adds = 0

            # collect consecutive deletes/adds
            while i < len(path) and path[i][0] in ('delete', 'add'):
                if path[i][0] == 'delete':
                    deletes += 1
                    curr_i += 1
                else:  # add
                    adds += 1
                    curr_j += 1
                i += 1

            # Now build command
            if deletes > 0 and adds > 0:
                # change
                l1_start = start_i + 1
                l1_end = start_i + deletes
                l2_start = start_j + 1
                l2_end = start_j + adds

                left = f"{l1_start},{l1_end}" if deletes > 1 else f"{l1_start}"
                right = f"{l2_start},{l2_end}" if adds > 1 else f"{l2_start}"

                commands.append(f"{left}c{right}")

            elif deletes > 0:
                # delete
                l1_start = start_i + 1
                l1_end = start_i + deletes

                left = f"{l1_start},{l1_end}" if deletes > 1 else f"{l1_start}"
                pos = start_j  # IMPORTANT: "after line start_j" in file2

                commands.append(f"{left}d{pos}")

            elif adds > 0:
                # add
                pos = start_i  # IMPORTANT: "after line start_i" in file1

                l2_start = start_j + 1
                l2_end = start_j + adds

                right = f"{l2_start},{l2_end}" if adds > 1 else f"{l2_start}"

                commands.append(f"{pos}a{right}")

        return commands

        
        


diff_1 = DiffCommands('diff_1.txt')
# print(diff_1, '\n')
diff_2 = DiffCommands('diff_2.txt')
# print(diff_2, '\n')
diff_3 = DiffCommands('diff_3.txt')
# print(diff_3, '\n')
files1 = OriginalNewFiles('file_1_1.txt', 'file_1_2.txt')
files3 = OriginalNewFiles('file_3_1.txt', 'file_3_2.txt')

files2_1 = OriginalNewFiles('file_2_1.txt', 'file_2_2.txt')
files2_2 = OriginalNewFiles('file_2_2.txt', 'file_2_1.txt')
diffs = files2_1.all_diff_commands()
print(len(diffs), '\n')
for diff in diffs:
    print(diff, '\n')
diffs = files2_2.all_diff_commands()
print(len(diffs), '\n')
for diff in diffs:
    print(diff, '\n')

# print(files.is_valid_diff(diff_1))
# print(files.is_valid_diff(diff_2))
# print(files.is_valid_diff(diff_3))

# files.print_diff(diff_3)
# files1.print_unmodified_from_original(diff_1)
# print()
# files1.print_unmodified_from_new(diff_1)

# files.all_diff_commands()


       
