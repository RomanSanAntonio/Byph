import os
import sys

class BMinusVM:
    def __init__(self):
        self.memory = []
        self.registers = {
            "r0": 0,
            "r1": 0,
            "r2": 0,
            "r3": 0,
            "r4": 0,
            "r5": 0,
            "sp": 0,
            "ip": 0,
            "fl": 0
        }
        self.labels = {}
        self.program = []
        self.running = True

        self.memory_path = None
        self.persist = 0
        self.debug = 0

    # -------------------------
    # Load Program (.bh only)
    # -------------------------

    def load_program(self, filename):
        if not filename.endswith(".bh"):
            raise Exception("B- source files must use .bh extension")

        with open(filename, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        # Required headers
        mom = int(lines[0].split("=")[1].strip())
        self.memory_path = lines[1].split("=")[1].strip().strip("'")

        # Optional headers
        header_index = 2
        while "=" in lines[header_index]:
            key, value = lines[header_index].split("=")
            key = key.strip()
            value = value.strip()

            if key == "pers":
                self.persist = int(value)
            elif key == "dbg":
                self.debug = int(value)

            header_index += 1
            if header_index >= len(lines):
                break

        # Allocate memory
        self.memory = [0] * (mom * 1024)
        self.registers["sp"] = len(self.memory) - 1

        # Load persistent memory (binary only)
        if self.persist and self.memory_path.endswith(".bin"):
            if os.path.exists(self.memory_path):
                with open(self.memory_path, "rb") as f:
                    data = f.read()
                    for i in range(min(len(data), len(self.memory))):
                        self.memory[i] = data[i]

        # Remaining lines = program
        self.program = lines[header_index:]

        # Parse labels
        for i, line in enumerate(self.program):
            if line.endswith(":"):
                self.labels[line[:-1]] = i

    # -------------------------
    # Helpers
    # -------------------------

    def get_value(self, operand):
        if operand in self.registers:
            return self.registers[operand]
        elif operand.startswith("["):
            addr = int(operand[1:-1])
            return self.memory[addr]
        else:
            return int(operand)

    def set_value(self, dest, value):
        if dest in self.registers:
            self.registers[dest] = value
        elif dest.startswith("["):
            addr = int(dest[1:-1])
            self.memory[addr] = value

    def debug_print(self, instruction):
        print(f"IP={self.registers['ip']} | {instruction}")
        print("REG:", self.registers)
        print("-" * 40)

    # -------------------------
    # Execution
    # -------------------------

    def run(self):
        while self.running and self.registers["ip"] < len(self.program):
            line = self.program[self.registers["ip"]]

            if line.endswith(":"):
                self.registers["ip"] += 1
                continue

            parts = line.split()
            cmd = parts[0]

            if self.debug:
                self.debug_print(line)

            if cmd == "mov":
                self.set_value(parts[1], self.get_value(parts[2]))

            elif cmd == "add":
                self.set_value(parts[1],
                               self.get_value(parts[1]) + self.get_value(parts[2]))

            elif cmd == "sub":
                self.set_value(parts[1],
                               self.get_value(parts[1]) - self.get_value(parts[2]))

            elif cmd == "mul":
                self.set_value(parts[1],
                               self.get_value(parts[1]) * self.get_value(parts[2]))

            elif cmd == "div":
                self.set_value(parts[1],
                               self.get_value(parts[1]) // self.get_value(parts[2]))

            elif cmd == "iseq":
                self.registers["fl"] = int(
                    self.get_value(parts[1]) == self.get_value(parts[2])
                )

            elif cmd == "jum":
                self.registers["ip"] = self.labels[parts[1]]
                continue

            elif cmd == "jeq":
                if self.registers["fl"] == 1:
                    self.registers["ip"] = self.labels[parts[1]]
                    continue

            elif cmd == "jneq":
                if self.registers["fl"] == 0:
                    self.registers["ip"] = self.labels[parts[1]]
                    continue

            elif cmd == "push":
                self.memory[self.registers["sp"]] = self.get_value(parts[1])
                self.registers["sp"] -= 1

            elif cmd == "pop":
                self.registers["sp"] += 1
                self.registers[parts[1]] = self.memory[self.registers["sp"]]

            elif cmd == "call":
                self.memory[self.registers["sp"]] = self.registers["ip"] + 1
                self.registers["sp"] -= 1
                self.registers["ip"] = self.labels[parts[1]]
                continue

            elif cmd == "ret":
                self.registers["sp"] += 1
                self.registers["ip"] = self.memory[self.registers["sp"]]
                continue

            elif cmd == "int":
                code = int(parts[1])
                if code == 1:
                    print(self.registers["r0"])
                elif code == 2:
                    print(chr(self.registers["r0"]), end="")
                elif code == 3:
                    self.registers["r0"] = int(input())

            elif cmd == "end":
                self.running = False

            self.registers["ip"] += 1

        self.save_memory()

    # -------------------------
    # Save Memory
    # -------------------------

    def save_memory(self):
        if self.memory_path.endswith(".bin"):
            if self.persist:
                with open(self.memory_path, "wb") as f:
                    f.write(bytes(self.memory))

        elif self.memory_path.endswith(".txt"):
            with open(self.memory_path, "w") as f:
                f.write("=== REGISTERS ===\n")
                for r in self.registers:
                    f.write(f"{r}: {self.registers[r]}\n")

                f.write("\n=== STACK (top 20) ===\n")
                top = len(self.memory) - 1
                for i in range(top, max(top - 20, -1), -1):
                    f.write(f"{i}: {self.memory[i]}\n")

                f.write("\n=== MEMORY (first 64 bytes) ===\n")
                for i in range(64):
                    f.write(f"{i}: {self.memory[i]}\n")


if __name__ == "__main__":
    vm = BMinusVM()
    vm.load_program(sys.argv[1])
    vm.run()
