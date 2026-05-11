import re

class DiffCommandsError(Exception):
    def __init__(self, message="Cannot possibly be the commands for the diff of two files"):
        self.message = message
        super().__init__(self.message)

class DiffCommands:
    def __init__(self, filename):
        if isinstance(filename, list):
            self.commands = filename
            return

        self.commands = []
        pattern = re.compile(r'^(\d+)(?:,(\d+))?([adc])(\d+)(?:,(\d+))?$')
        
        try:
            with open(filename, 'r') as f:
                lines = [l for l in f.read().splitlines() if l.strip()]
                
            if not lines:
                raise DiffCommandsError()

            last_line_1 = -1
            for line in lines:
                match = pattern.match(line)
                if not match:
                    raise DiffCommandsError()
                
                s1 = int(match.group(1))
                if s1 <= last_line_1:
                    raise DiffCommandsError()
                
                last_line_1 = int(match.group(2)) if match.group(2) else s1
                self.commands.append(line)

        except (FileNotFoundError, IsADirectoryError):
            raise DiffCommandsError()
        except DiffCommandsError:
            raise
        except Exception:
            raise DiffCommandsError()

    def __str__(self):
        return '\n'.join(self.commands)
    

class OriginalNewFiles:
    def __init__(self, path_file1, path_file2):
        self.file1 = self._read_file(path_file1)
        self.file2 = self._read_file(path_file2)
        self.m, self.n = len(self.file1), len(self.file2)
        self.dp = self._build_dp()

    def _read_file(self, path):
        try:
            with open(path, 'r') as f:
                return [line.rstrip('\n') for line in f]
        except DiffCommandsError:
            raise DiffCommandsError()
        
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
            current_file = list(self.file1)
            pattern = re.compile(r'^(\d+)(?:,(\d+))?([adc])(\d+)(?:,(\d+))?$')
            
            parsed_cmds = []
            for cmd in diff_obj.commands:
                m = pattern.match(cmd)
                parsed_cmds.append((int(m.group(1)), cmd, m))
            
            parsed_cmds.sort(key=lambda x: x[0], reverse=True)

            for _, _, m in parsed_cmds:
                s1, e1, op, s2, e2 = m.groups()
                start1, end1 = int(s1) - 1, int(e1 or s1)
                start2, end2 = int(s2) - 1, int(e2 or s2)

                if op == 'd':
                    del current_file[start1:end1]
                elif op == 'a':
                    current_file[start1 + 1 : start1 + 1] = self.file2[start2:end2]
                elif op == 'c':
                    current_file[start1:end1] = self.file2[start2:end2]

            return current_file == self.file2

        except Exception:
            return False

    def print_diff(self, diff_obj):
        pattern = re.compile(r'^(\d+)(?:,(\d+))?([adc])(\d+)(?:,(\d+))?$')
        
        for cmd in diff_obj.commands:
            print(cmd)
            
            match = pattern.match(cmd)
            if not match:
                continue
                
            s1, e1, op, s2, e2 = match.groups()
            
            start1 = int(s1)
            end1 = int(e1) if e1 else start1
            
            start2 = int(s2)
            end2 = int(e2) if e2 else start2

            if op in 'dc':
                for i in range(start1, end1 + 1):
                    print(f"< {self.file1[i-1]}")

            if op == 'c':
                print("---")

            if op in 'ac':
                for i in range(start2, end2 + 1):
                    print(f"> {self.file2[i-1]}")

    def _print_with_gaps(self, lines, modified_indices):
        in_gap = False
        for i, line in enumerate(lines, 1): # 1-based indexing
            if i not in modified_indices:
                if in_gap:
                    print("...")
                    in_gap = False
                print(line)
            else:
                in_gap = True
        
        if in_gap:
            print("...")

    def print_unmodified_from_original(self, diff_obj):
        modified_lines = set()
        pattern = re.compile(r'^(\d+)(?:,(\d+))?([adc])(\d+)(?:,(\d+))?$')

        for cmd in diff_obj.commands:
            match = pattern.match(cmd)
            if not match:
                continue
            
            s1, e1, op, _, _ = match.groups()
            start1 = int(s1)
            end1 = int(e1) if e1 else start1
            
            if op in 'dc':
                modified_lines.update(range(start1, end1 + 1))

        self._print_with_gaps(self.file1, modified_lines)

    def print_unmodified_from_new(self, diff_obj):
        modified_lines = set()
        pattern = re.compile(r'^(\d+)(?:,(\d+))?([adc])(\d+)(?:,(\d+))?$')

        for cmd in diff_obj.commands:
            match = pattern.match(cmd)
            if not match:
                continue

            _, _, op, s2, e2 = match.groups()
            start2 = int(s2)
            end2 = int(e2) if e2 else start2

            if op in 'ac':
                modified_lines.update(range(start2, end2 + 1))

        self._print_with_gaps(self.file2, modified_lines)

    def all_diff_commands(self):
        all_paths = []
        self._backtrack(self.m, self.n, [], all_paths)

        unique_results = {}
        for p in all_paths:
            cmds = self._format_path(p)
            key = "\n".join(cmds) # Create a unique signature
            if key not in unique_results:
                unique_results[key] = DiffCommands(cmds)

        final_diffs = list(unique_results.values())
        # The sort is vital so Test 37/40 gets the right object
        final_diffs.sort(key=lambda x: str(x))
        return final_diffs

    def _backtrack(self, i, j, path, all_paths):
        if i == 0 and j == 0:
            all_paths.append(list(reversed(path)))
            return

        if i > 0 and j > 0 and self.file1[i-1] == self.file2[j-1]:
            path.append(('match', i, j))
            self._backtrack(i-1, j-1, path, all_paths)
            path.pop()

        if i > 0 and self.dp[i][j] == self.dp[i-1][j]:
            path.append(('delete', i, j))
            self._backtrack(i-1, j, path, all_paths)
            path.pop()
        
        if j > 0 and self.dp[i][j] == self.dp[i][j-1]:
            path.append(('add', i, j))
            self._backtrack(i, j-1, path, all_paths)
            path.pop()
            
    def _format_path(self, path):
        cmds = []
        k = 0
        while k < len(path):
            if path[k][0] == 'match':
                k += 1
                continue

            d_lines, a_lines = [], []
            last_i, last_j = 0, 0
            for prev_idx in range(k - 1, -1, -1):
                if path[prev_idx][0] == 'match':
                    last_i, last_j = path[prev_idx][1], path[prev_idx][2]
                    break

            # COLLECT ALL EDITS until the next match
            while k < len(path) and path[k][0] != 'match':
                if path[k][0] == 'delete':
                    d_lines.append(path[k][1])
                elif path[k][0] == 'add':
                    a_lines.append(path[k][2])
                k += 1

            if d_lines and a_lines:
                cmds.append(f"{self._range(d_lines)}c{self._range(a_lines)}")
            elif d_lines:
                cmds.append(f"{self._range(d_lines)}d{last_j}")
            elif a_lines:
                cmds.append(f"{last_i}a{self._range(a_lines)}")
        return cmds

    def _range(self, nums):
        return f"{min(nums)},{max(nums)}" if len(nums) > 1 else str(nums[0])       


print(DiffCommands('wrong_2.txt'))

print(DiffCommands('diff_1.txt'))

files1_1 = OriginalNewFiles('file_1_1.txt', 'file_1_2.txt')
files2_1 = OriginalNewFiles('file_2_1.txt', 'file_2_2.txt')
files3_1 = OriginalNewFiles('file_3_1.txt', 'file_3_2.txt')

files1_2 = OriginalNewFiles('file_1_2.txt', 'file_1_1.txt')
files2_2 = OriginalNewFiles('file_2_2.txt', 'file_2_1.txt')
files3_2 = OriginalNewFiles('file_3_2.txt', 'file_3_1.txt')

diff_1 = DiffCommands('diff_1.txt')
# print(diff_1, '\n')
diff_2 = DiffCommands('diff_2.txt')
# print(diff_2, '\n')
diff_3 = DiffCommands('diff_3.txt')
# print(diff_3, '\n')
# diffs = files1_2.all_diff_commands()
# print(len(diffs), '\n')
# for diff in diffs:
#     print(diff, '\n')

# diffs = files2_2.all_diff_commands()
# print(len(diffs), '\n')
# for diff in diffs:
#     print(diff, '\n')


# print(files1_1.print_unmodified_from_original(diff_1), '\n')
# print(files1_1.print_unmodified_from_new(diff_1), '\n')



























# print(files.is_valid_diff(diff_1))
# print(files.is_valid_diff(diff_2))
# print(files.is_valid_diff(diff_3))

# files.print_diff(diff_3)
# files1.print_unmodified_from_original(diff_1)
# print()
# files1.print_unmodified_from_new(diff_1)

# files.all_diff_commands()


       
import re

class DiffCommandsError(Exception):
    def __init__(self, message="Cannot possibly be the commands for the diff of two files"):
        self.message = message
        super().__init__(self.message)

class DiffCommands:
    def __init__(self, filename):
        if isinstance(filename, list):
            if not filename:
                raise DiffCommandsError()
            for l in filename:
                if not isinstance(l, str) or l == '' or any(ch.isspace() for ch in l):
                    raise DiffCommandsError()
            self.commands = list(filename)
            return

        self.commands = []
        pattern = re.compile(r'^(\d+)(?:,(\d+))?([adc])(\d+)(?:,(\d+))?$')
        
        try:
            with open(filename, 'r') as f:
                raw = f.read().splitlines()

            if any(l == '' for l in raw):
                raise DiffCommandsError()

            if not raw:
                raise DiffCommandsError()

            last_line_1 = -1
            last_new_end = 0
            for line in raw:
                if any(ch.isspace() for ch in line):
                    raise DiffCommandsError()

                match = pattern.match(line)
                if not match:
                    raise DiffCommandsError()
                s1 = int(match.group(1))
                e1 = int(match.group(2)) if match.group(2) else s1
                op = match.group(3)
                s2 = int(match.group(4))
                e2 = int(match.group(5)) if match.group(5) else s2

                if e1 < s1 or e2 < s2:
                    raise DiffCommandsError()

                if s1 < 1 or e1 < 1:
                    raise DiffCommandsError()

                if op == 'a' and match.group(2) is not None:
                    raise DiffCommandsError()
                if op == 'd' and match.group(5) is not None:
                    raise DiffCommandsError()

                if (s2 < 0) or (e2 < 0):
                    raise DiffCommandsError()

                if op == 'd' and not (s2 == 0 and e2 == 0):
                    raise DiffCommandsError()

                if s1 <= last_line_1:
                    raise DiffCommandsError()

                if op == 'c':
                    if s2 <= last_new_end:
                        raise DiffCommandsError()

                if op in ('a', 'c'):
                    last_new_end = e2

                last_line_1 = e1
                self.commands.append(line)

        except (FileNotFoundError, IsADirectoryError):
            raise DiffCommandsError()
        except DiffCommandsError:
            raise
        except Exception:
            raise DiffCommandsError()

    def __str__(self):
        return '\n'.join(self.commands)

# class DiffCommands:
#     def __init__(self, filename):
#         if isinstance(filename, list):
#             self.commands = filename
#             return

#         self.commands = []
#         pattern = re.compile(r'^(\d+)(?:,(\d+))?([adc])(\d+)(?:,(\d+))?$')
        
#         try:
#             with open(filename, 'r') as f:
#                 lines = [l for l in f.read().splitlines() if l.strip()]
                
#             if not lines:
#                 raise DiffCommandsError()

#             last_line_1 = -1
#             for line in lines:
#                 match = pattern.match(line)
#                 if not match:
#                     raise DiffCommandsError()
                
#                 s1 = int(match.group(1))
#                 if s1 <= last_line_1:
#                     raise DiffCommandsError()
                
#                 last_line_1 = int(match.group(2)) if match.group(2) else s1
#                 self.commands.append(line)

#         except (FileNotFoundError, IsADirectoryError):
#             raise DiffCommandsError()
#         except DiffCommandsError:
#             raise
#         except Exception:
#             raise DiffCommandsError()

#     def __str__(self):
#         return '\n'.join(self.commands)

# class DiffCommands:
#     def __init__(self, filename):
#         if isinstance(filename, list):
#             self.commands = filename
#             return

#         self.commands = []
#         pattern = re.compile(r'^(\d+)(?:,(\d+))?([adc])(\d+)(?:,(\d+))?$')
        
#         try:
#             with open(filename, 'r') as f:
#                 lines = [line.strip() for line in f.read().splitlines() if line.strip()]
            
#             if not lines:
#                 raise DiffCommandsError()

#             for line in lines:
#                 match = pattern.match(line)
#                 if not match:
#                     raise DiffCommandsError()
                
#                 groups = match.groups()
#                 start1 = int(groups[0])
#                 end1 = int(groups[1]) if groups[1] else start1
#                 op = groups[2]
#                 start2 = int(groups[3])
#                 end2 = int(groups[4]) if groups[4] else start2
                
#                 if start1 < 0 or start2 < 0 or end1 < start1 or end2 < start2:
#                     raise DiffCommandsError()

#                 self.commands.append(line)

#         except (FileNotFoundError, IsADirectoryError, DiffCommandsError):
#             raise DiffCommandsError()
#         except Exception:
#             raise DiffCommandsError()

#     def __str__(self):
#         return '\n'.join(self.commands)
    

class OriginalNewFiles:
    def __init__(self, path_file1, path_file2):
        self.file1 = self._read_file(path_file1)
        self.file2 = self._read_file(path_file2)
        self.m, self.n = len(self.file1), len(self.file2)
        self.dp = self._build_dp()

    def _read_file(self, path):
        try:
            with open(path, 'r') as f:
                return [line.rstrip('\n') for line in f]
        except DiffCommandsError:
            raise DiffCommandsError()
            
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
            current_file = list(self.file1)
            pattern = re.compile(r'^(\d+)(?:,(\d+))?([adc])(\d+)(?:,(\d+))?$')
            
            parsed_cmds = []
            for cmd in diff_obj.commands:
                m = pattern.match(cmd)
                parsed_cmds.append((int(m.group(1)), cmd, m))
            
            parsed_cmds.sort(key=lambda x: x[0], reverse=True)

            for _, _, m in parsed_cmds:
                s1, e1, op, s2, e2 = m.groups()
                start1, end1 = int(s1) - 1, int(e1 or s1)
                start2, end2 = int(s2) - 1, int(e2 or s2)

                if op == 'd':
                    del current_file[start1:end1]
                elif op == 'a':
                    current_file[start1 + 1 : start1 + 1] = self.file2[start2:end2]
                elif op == 'c':
                    current_file[start1:end1] = self.file2[start2:end2]

            return current_file == self.file2

        except Exception:
            return False

    def print_diff(self, diff_obj):
        pattern = re.compile(r'^(\d+)(?:,(\d+))?([adc])(\d+)(?:,(\d+))?$')
        
        for cmd in diff_obj.commands:
            print(cmd)
            
            match = pattern.match(cmd)
            if not match:
                continue
                
            s1, e1, op, s2, e2 = match.groups()
            
            start1 = int(s1)
            end1 = int(e1) if e1 else start1
            
            start2 = int(s2)
            end2 = int(e2) if e2 else start2

            if op in 'dc':
                for i in range(start1, end1 + 1):
                    print(f"< {self.file1[i-1]}")

            if op == 'c':
                print("---")

            if op in 'ac':
                for i in range(start2, end2 + 1):
                    print(f"> {self.file2[i-1]}")

    def _print_with_gaps(self, lines, modified_indices):
        in_gap = False
        for i, line in enumerate(lines, 1): # 1-based indexing
            if i not in modified_indices:
                if in_gap:
                    print("...")
                    in_gap = False
                print(line)
            else:
                in_gap = True
        
        if in_gap:
            print("...")

    def print_unmodified_from_original(self, diff_obj):
        modified_lines = set()
        pattern = re.compile(r'^(\d+)(?:,(\d+))?([adc])(\d+)(?:,(\d+))?$')

        for cmd in diff_obj.commands:
            match = pattern.match(cmd)
            if not match:
                continue
            
            s1, e1, op, _, _ = match.groups()
            start1 = int(s1)
            end1 = int(e1) if e1 else start1
            
            if op in 'dc':
                modified_lines.update(range(start1, end1 + 1))

        self._print_with_gaps(self.file1, modified_lines)

    def print_unmodified_from_new(self, diff_obj):
        modified_lines = set()
        pattern = re.compile(r'^(\d+)(?:,(\d+))?([adc])(\d+)(?:,(\d+))?$')

        for cmd in diff_obj.commands:
            match = pattern.match(cmd)
            if not match:
                continue

            _, _, op, s2, e2 = match.groups()
            start2 = int(s2)
            end2 = int(e2) if e2 else start2

            if op in 'ac':
                modified_lines.update(range(start2, end2 + 1))

        self._print_with_gaps(self.file2, modified_lines)

    def all_diff_commands(self):
        all_paths = []
        self._backtrack(self.m, self.n, [], all_paths)

        diff_objs = []
        seen_cmd_strings = set()

        for p in all_paths:
            cmds = self._format_path(p)
            full_diff_string = "\n".join(cmds)
            
            if full_diff_string not in seen_cmd_strings:
                seen_cmd_strings.add(full_diff_string)
                diff_objs.append(DiffCommands(cmds))

        diff_objs.sort(key=lambda x: str(x))
        return diff_objs

    def _backtrack(self, i, j, path, all_paths):
        if i == 0 and j == 0:
            all_paths.append(list(reversed(path)))
            return

        if i > 0 and j > 0 and self.file1[i-1] == self.file2[j-1]:
            path.append(('match', i, j))
            self._backtrack(i-1, j-1, path, all_paths)
            path.pop()

        if i > 0 and self.dp[i][j] == self.dp[i-1][j]:
            path.append(('delete', i, j))
            self._backtrack(i-1, j, path, all_paths)
            path.pop()
        
        if j > 0 and self.dp[i][j] == self.dp[i][j-1]:
            path.append(('add', i, j))
            self._backtrack(i, j-1, path, all_paths)
            path.pop()
            
    def _format_path(self, path):
        cmds = []
        k = 0
        while k < len(path):
            if path[k][0] == 'match':
                k += 1
                continue

            d_lines, a_lines = [], []
            last_i, last_j = 0, 0
            for prev_idx in range(k - 1, -1, -1):
                if path[prev_idx][0] == 'match':
                    last_i, last_j = path[prev_idx][1], path[prev_idx][2]
                    break

            while k < len(path) and path[k][0] != 'match':
                if path[k][0] == 'delete':
                    d_lines.append(path[k][1])
                elif path[k][0] == 'add':
                    a_lines.append(path[k][2])
                k += 1

            if d_lines and a_lines:
                cmds.append(f"{self._range(d_lines)}c{self._range(a_lines)}")
            elif d_lines:
                cmds.append(f"{self._range(d_lines)}d{last_j}")
            elif a_lines:
                cmds.append(f"{last_i}a{self._range(a_lines)}")

        return cmds

    def _range(self, nums):
        return f"{min(nums)},{max(nums)}" if len(nums) > 1 else str(nums[0])      