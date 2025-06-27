class BFInterpreter:
    def __init__(self, program, debug=False):
        self.program = program
        self.memory = [0] * 30000
        self.ptr = 0
        self.pc = 0
        self.debug = debug
        self.steps = 0

    def run(self, input_data=b''):
        input_buffer = list(input_data)
        output_buffer = []

        while self.pc < len(self.program):
            cmd = self.program[self.pc]
            self.steps += 1

            if self.debug and self.steps % 100 == 0:
                self._debug_state()

            if cmd == '>':
                self.ptr += 1
            elif cmd == '<':
                self.ptr -= 1
            elif cmd == '+':
                self.memory[self.ptr] = (self.memory[self.ptr] + 1) % 256
            elif cmd == '-':
                self.memory[self.ptr] = (self.memory[self.ptr] - 1) % 256
            elif cmd == '.':
                output_buffer.append(self.memory[self.ptr])
            elif cmd == ',':
                if input_buffer:
                    self.memory[self.ptr] = input_buffer.pop(0)
                else:
                    self.memory[self.ptr] = 0
            elif cmd == '[':
                if self.memory[self.ptr] == 0:
                    bracket_count = 1
                    while bracket_count > 0:
                        self.pc += 1
                        if self.program[self.pc] == '[':
                            bracket_count += 1
                        elif self.program[self.pc] == ']':
                            bracket_count -= 1
            elif cmd == ']':
                if self.memory[self.ptr] != 0:
                    bracket_count = 1
                    while bracket_count > 0:
                        self.pc -= 1
                        if self.program[self.pc] == ']':
                            bracket_count += 1
                        elif self.program[self.pc] == '[':
                            bracket_count -= 1

            self.pc += 1

        if self.debug:
            print(f"\nTotal steps: {self.steps}")

        return bytes(output_buffer)

    def _debug_state(self):
        """Show memory visualization"""
        cells = self.memory[:16]
        print(f"\nStep {self.steps}:")
        print("Memory: " + " ".join(f"[{c:03d}]" for c in cells))
        print("        " + "  ^  " * self.ptr if self.ptr < 16 else f"Ptr at {self.ptr}")