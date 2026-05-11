from diff import *

class DiffCommands:
    def __init__(self, filename):
        if isinstance(filename, list):
            self.commands = filename
            return

        self.commands = []
        pattern = re.compile(r'^(\d+)(?:,(\d+))?([adc])(\d+)(?:,(\d+))?$')
        
        try:
            with open(filename, 'r') as f:
                lines = [line.strip() for line in f.read().splitlines() if line.strip()]
            
            if not lines:
                raise DiffCommandsError()

            for line in lines:
                match = pattern.match(line)
                if not match:
                    raise DiffCommandsError()
                
                groups = match.groups()
                start1 = int(groups[0])
                end1 = int(groups[1]) if groups[1] else start1
                op = groups[2]
                start2 = int(groups[3])
                end2 = int(groups[4]) if groups[4] else start2
                
                if start1 < 0 or start2 < 0 or end1 < start1 or end2 < start2:
                    raise DiffCommandsError()

                self.commands.append(line)

        except (FileNotFoundError, IsADirectoryError, DiffCommandsError):
            raise DiffCommandsError()
        except Exception:
            raise DiffCommandsError()
