import re

class DiffCommandsError(Exception):
    def __init__(self, message="Cannot possibly be the commands for the diff of two files"):
        self.message = message
        super().__init__(self.message)

class DiffCommands:
    def __init__(self, filename):
        pattern = re.compile(r'^(\d+)(?:,(\d+))?([adc])(\d+)(?:,(\d+))?$')

        lines = None
        if isinstance(filename, list):
            lines = list(filename)
            if not lines:
                self.commands = []
                return
        else:
            try:
                with open(filename, 'r') as f:
                    lines = f.read().splitlines()
            except (FileNotFoundError, IsADirectoryError):
                raise DiffCommandsError()

        if any(l == '' for l in lines):
            raise DiffCommandsError()

        self.commands = []
        last_orig_end = 0
        last_new_end = 0

        for line in lines:
            if any(ch.isspace() for ch in line):
                raise DiffCommandsError()

            m = pattern.match(line)
            if not m:
                raise DiffCommandsError()

            s1, e1, op, s2, e2 = m.groups()
            s1_i = int(s1)
            e1_i = int(e1) if e1 else s1_i
            s2_i = int(s2)
            e2_i = int(e2) if e2 else s2_i

            if e1_i < s1_i or e2_i < s2_i:
                raise DiffCommandsError()
            if op == 'a':
                if s1_i < 0 or e1_i < 0:
                    raise DiffCommandsError()
            else:
                if s1_i < 1 or e1_i < 1:
                    raise DiffCommandsError()

            if s2_i < 0 or e2_i < 0:
                raise DiffCommandsError()

            if op == 'a' and e1 is not None:
                raise DiffCommandsError()
            if op == 'd' and e2 is not None:
                raise DiffCommandsError()

            # Reject a `c` that follows a `d` at the immediately next original line
            if self.commands and s1_i <= last_orig_end:
                raise DiffCommandsError()

            if len(self.commands) > 0 and last_op == 'd' and op == 'c' and s1_i == last_orig_end + 1:
                raise DiffCommandsError()

            # enforce per-command matching-gap constraints between files
            orig_gap = s1_i - last_orig_end
            new_gap = s2_i - last_new_end

            if op == 'a':
                if orig_gap != new_gap - 1:
                    raise DiffCommandsError()
            elif op == 'd':
                if orig_gap - 1 != new_gap:
                    raise DiffCommandsError()
            elif op == 'c':
                if orig_gap != new_gap:
                    raise DiffCommandsError()

            last_orig_end = e1_i
            if op in ('a', 'c'):
                last_new_end = e2_i
            else:
                last_new_end = s2_i

            last_op = op

            self.commands.append(line)

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

def _validate_diff(pairs):
    print('=== Valid diffs ===')
    for diff_file, f1, f2 in pairs:
        try:
            d = DiffCommands(diff_file)
            print(f"{diff_file} OK ->")
            print(d)
            try:
                onf = OriginalNewFiles(f1, f2)
                valid = onf.is_valid_diff(d)
                print(f"  validates: {valid}")
            except Exception as e:
                print(f"  validation error: {type(e).__name__}")
        except Exception as e:
            print(f"{diff_file} ERR {type(e).__name__}")

def _validate_wrongs():
    print('\n=== Wrong diffs ===')
    for i in range(1, 8):
        fname = f'wrong_{i}.txt'
        try:
            d = DiffCommands(fname)
            print(f"{fname} OK ->")
            print(d)
        except Exception as e:
            if isinstance(e, DiffCommandsError):
                print(f"{fname} ERR DiffCommandsError")
            else:
                print(f"{fname} ERR {type(e).__name__}")

def _validate_all_diffs(pairs):
    print('\n=== All diffs ===')
    # accept either (f1, f2) or (diff_file, f1, f2) tuples
    for *_, f1, f2 in pairs:
        try:
            onf = OriginalNewFiles(f1, f2)
            all_diffs = onf.all_diff_commands()
            print(f"{f1} -> {f2} has {len(all_diffs)} diffs")
            for d in all_diffs:
                if not getattr(d, 'commands', None):
                    print('(no changes)')
                else:
                    print(d)
                print('---')
            onf = OriginalNewFiles(f2, f1)
            all_diffs = onf.all_diff_commands()
            print(f"{f2} -> {f1} has {len(all_diffs)} diffs")
            for d in all_diffs:
                print(d)
                print('---')
        except Exception as e:
            print(f"{f1} -> {f2} ERR {type(e).__name__}")

def _validate_prints(pairs):
    print('\n=== Print diffs ===')
    for diff_file, f1, f2 in pairs:
        try:
            d = DiffCommands(diff_file)
            onf = OriginalNewFiles(f1, f2)
            print(f"Diff: {diff_file}")
            onf.print_diff(d)
            print("\nUnmodified from original:")
            onf.print_unmodified_from_original(d)
            print("\nUnmodified from new:")
            onf.print_unmodified_from_new(d)
            print('---')
        except Exception as e:
            print(f"{diff_file} ERR {type(e).__name__}")

def _test_identical_files():
    onf = OriginalNewFiles('file_1_1.txt', 'file_1_1.txt')
    all_diffs = onf.all_diff_commands()
    print(f"file_1_1.txt -> file_1_1.txt has {len(all_diffs)} diffs")
    for d in all_diffs:
        if not getattr(d, 'commands', None):
            print('(no changes)')
        else:
            print(d)
        print('---')

def _run_tests():
    pairs = [
        ('diff_1.txt', 'file_1_1.txt', 'file_1_2.txt'),
        ('diff_2.txt', 'file_2_1.txt', 'file_2_2.txt'),
        ('diff_3.txt', 'file_3_1.txt', 'file_3_2.txt'),
    ]
    # _validate_diff(pairs)
    _validate_wrongs()
    # _validate_prints(pairs)
    _validate_all_diffs(pairs)
if __name__ == '__main__':
    _run_tests()
    
    

