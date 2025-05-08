class MacroProcessorPassOne:
    def __init__(self):
        # Data structures for Pass-I
        self.MNT = {}  # Macro Name Table
        self.MDT = []  # Macro Definition Table
        self.intermediate_code = []  # For storing non-macro code lines
        self.macro_def_start = False  # Indicates if we are inside a macro definition

    def define_macro(self, macro_name, params):
        # Adds the macro name and starting position in MDT to MNT
        self.MNT[macro_name] = {"params": params, "mdt_index": len(self.MDT)}

    def add_to_MDT(self, line):
        # Add line to MDT
        self.MDT.append(line)

    def process_line(self, line):
        # Splits the line into tokens
        tokens = line.strip().split()

        # Check for start of macro definition
        if tokens[0] == "MACRO":
            self.macro_def_start = True
            return

        # End of macro definition
        elif self.macro_def_start and tokens[0] != "MEND":
            # First line after MACRO keyword should be the macro name and its parameters
            macro_name, *params = tokens
            self.define_macro(macro_name, params)
            self.add_to_MDT(" ".join(tokens))
        elif tokens[0] == "MEND":
            # End of the current macro definition
            self.macro_def_start = False
            self.add_to_MDT(line)  # Add MEND to MDT
        else:
            if self.macro_def_start:
                # Within a macro definition, add to MDT
                self.add_to_MDT(line)
            else:
                # Outside of macro definition, add to intermediate code
                self.intermediate_code.append(line)

    def pass_one(self, source_code):
        for line in source_code:
            self.process_line(line)

    def print_results(self):
        print("Macro Name Table (MNT):")
        for macro_name, details in self.MNT.items():
            print(f"{macro_name}: Params={details['params']} MDT Index={details['mdt_index']}")

        print("\nMacro Definition Table (MDT):")
        for index, line in enumerate(self.MDT):
            print(f"{index}: {line}")

        print("\nIntermediate Code:")
        for line in self.intermediate_code:
            print(line)


# Example input for a source code containing macro definitions
source_code = [
    "MACRO",
    "INCR &ARG1",
    "LOAD &ARG1",
    "ADD =1",
    "STORE &ARG1",
    "MEND",
    "MACRO",
    "DECR &ARG1",
    "LOAD &ARG1",
    "SUB =1",
    "STORE &ARG1",
    "MEND",
    "START 100",
    "INCR A",
    "DECR B",
    "END"
]

# Initialize macro processor and process the source code
macro_processor = MacroProcessorPassOne()
macro_processor.pass_one(source_code)
macro_processor.print_results()
