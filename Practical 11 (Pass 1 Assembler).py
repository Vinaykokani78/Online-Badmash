# Updated Code with Proper Handling

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, symbol, address):
        self.symbols[symbol] = address

    def get_address(self, symbol):
        return self.symbols.get(symbol, None)

class OpCodeTable:
    def __init__(self):
        self.opcodes = {
            "LOAD": "01",
            "STORE": "02",
            "ADD": "03",
            "SUB": "04",
            # Add more opcodes as needed
        }

    def get_opcode(self, mnemonic):
        return self.opcodes.get(mnemonic, None)

class LiteralTable:
    def __init__(self):
        self.literals = {}

    def add_literal(self, literal, address):
        self.literals[literal] = address

    def get_address(self, literal):
        return self.literals.get(literal, None)

class PassOneAssembler:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.opcode_table = OpCodeTable()
        self.literal_table = LiteralTable()
        self.location_counter = 0
        self.intermediate_code = []

    def process_line(self, line):
        tokens = line.split()
        label, opcode, operand = None, None, None

        if len(tokens) == 3:
            label, opcode, operand = tokens
        elif len(tokens) == 2:
            opcode, operand = tokens
        elif len(tokens) == 1:
            opcode = tokens[0]

        if label:
            if label in self.symbol_table.symbols:
                raise ValueError(f"Error: Duplicate symbol '{label}'")
            self.symbol_table.add_symbol(label, self.location_counter)

        if opcode == "START":
            self.location_counter = int(operand)
            return
        elif opcode == "END":
            return
        elif opcode == "EQU":
            if label:
                self.symbol_table.add_symbol(label, operand)
            return

        opcode_code = self.opcode_table.get_opcode(opcode)
        if opcode_code:
            if operand and operand.startswith("="):
                self.literal_table.add_literal(operand, None)
            self.intermediate_code.append((self.location_counter, opcode, operand))
            self.location_counter += 1
        else:
            raise ValueError(f"Error: Unknown opcode '{opcode}'")

    def assemble(self, source_code):
        for line in source_code:
            self.process_line(line.strip())

        for literal in self.literal_table.literals.keys():
            if self.literal_table.literals[literal] is None:
                self.literal_table.add_literal(literal, self.location_counter)
                self.location_counter += 1

    def print_symbol_table(self):
        print("Symbol Table:")
        for symbol, address in self.symbol_table.symbols.items():
            print(f"{symbol} : {address}")

    def print_literal_table(self):
        print("Literal Table:")
        for literal, address in self.literal_table.literals.items():
            print(f"{literal} : {address}")

    def print_intermediate_code(self):
        print("Intermediate Code:")
        for entry in self.intermediate_code:
            print(entry)


# Example usage
source_code = [
    "START 100",
    "LOAD A",
    "ADD B",
    "STORE C",
    "A EQU 5",
    "B EQU 10",
    "C EQU 20",
    "END"
]

assembler = PassOneAssembler()
assembler.assemble(source_code)
assembler.print_symbol_table()
assembler.print_literal_table()
assembler.print_intermediate_code()
