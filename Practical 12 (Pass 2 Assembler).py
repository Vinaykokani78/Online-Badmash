class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, symbol, address):
        self.symbols[symbol] = address

    def get_address(self, symbol):
        return self.symbols.get(symbol, None)

class LiteralTable:
    def __init__(self):
        self.literals = {}

    def add_literal(self, literal, address):
        self.literals[literal] = address

    def get_address(self, literal):
        return self.literals.get(literal, None)

class OpCodeTable:
    def __init__(self):
        # Opcodes for the pseudo-machine instructions
        self.opcodes = {
            "LOAD": "01",
            "STORE": "02",
            "ADD": "03",
            "SUB": "04",
            "MULT": "05",
            "DIV": "06",
            "JUMP": "07",
            "JUMPZ": "08",
            "JUMPN": "09",
            "END": "FF"
            # Add more opcodes as needed
        }

    def get_opcode(self, mnemonic):
        return self.opcodes.get(mnemonic, None)

class PassTwoAssembler:
    def __init__(self, intermediate_code, symbol_table, literal_table):
        self.intermediate_code = intermediate_code
        self.symbol_table = symbol_table
        self.literal_table = literal_table
        self.opcode_table = OpCodeTable()
        self.object_code = []

    def resolve_operand(self, operand):
        # Check if operand is a symbol
        address = self.symbol_table.get_address(operand)
        if address is not None:
            return address

        # Check if operand is a literal
        address = self.literal_table.get_address(operand)
        if address is not None:
            return address

        # If operand is numeric, return it directly
        if operand.isdigit():
            return int(operand)

        # Return None if operand cannot be resolved
        return None

    def generate_object_code(self):
        for loc_counter, opcode, operand in self.intermediate_code:
            opcode_hex = self.opcode_table.get_opcode(opcode)
            if opcode_hex is None:
                raise ValueError(f"Error: Unknown opcode '{opcode}'")

            # Resolve operand to its address or value
            operand_address = self.resolve_operand(operand)
            if operand and operand_address is None:
                raise ValueError(f"Error: Undefined symbol or literal '{operand}'")

            # Format object code line (e.g., "01 005" for LOAD A at address 5)
            object_code_line = f"{loc_counter:03} {opcode_hex} {operand_address:03}" if operand else f"{loc_counter:03} {opcode_hex} 000"
            self.object_code.append(object_code_line)

    def print_object_code(self):
        print("Object Code:")
        for line in self.object_code:
            print(line)

# Example input from Pass-I
intermediate_code = [
    (100, "LOAD", "A"),
    (101, "ADD", "B"),
    (102, "STORE", "C"),
]

# Symbol and Literal Tables from Pass-I
symbol_table = SymbolTable()
symbol_table.add_symbol("A", 5)
symbol_table.add_symbol("B", 10)
symbol_table.add_symbol("C", 20)

literal_table = LiteralTable()
# Add literals if any were encountered

# Create Pass-II Assembler instance and generate object code
assembler = PassTwoAssembler(intermediate_code, symbol_table, literal_table)
assembler.generate_object_code()
assembler.print_object_code()
