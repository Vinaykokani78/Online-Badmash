class MacroProcessorPassOne:
    def __init__(self):
        self.MNT = {}  # Macro Name Table (MNT)
        self.MDT = []  # Macro Definition Table (MDT)
        self.intermediate_code = []  # Intermediate code generated
        self.macro_name = None
        self.macro_params = None

    def process_macro_definition(self, line):
        """
        Process a macro definition (MACRO ... MEND).
        """
        tokens = line.strip().split()
        if tokens[0] == "MACRO":
            self.macro_name = tokens[1]  # Macro name
            self.macro_params = tokens[2:]  # Parameters for the macro
            self.MNT[self.macro_name] = {"params": self.macro_params, "mdt_index": len(self.MDT)}
        elif tokens[0] == "MEND":
            self.macro_name = None
            self.macro_params = None

    def process_macro_body(self, line):
        """
        Process the body of the macro and add it to MDT.
        """
        if self.macro_name:
            self.MDT.append(line.strip())

    def pass_one(self, source_code):
        """
        Process the source code to generate MNT, MDT, and intermediate code.
        """
        for line in source_code:
            tokens = line.strip().split()
            
            # Check for MACRO definition and MEND
            if tokens and tokens[0] == "MACRO":
                self.process_macro_definition(line)
            elif tokens and tokens[0] == "MEND":
                self.process_macro_definition(line)
            elif self.macro_name:
                # Process macro body lines
                self.process_macro_body(line)
            else:
                # Normal code (non-macro lines)
                self.intermediate_code.append(line.strip())

    def print_mnt_mdt(self):
        print("Macro Name Table (MNT):")
        for macro_name, info in self.MNT.items():
            print(f"{macro_name}: {info}")
        print("\nMacro Definition Table (MDT):")
        for line in self.MDT:
            print(line)

    def print_intermediate_code(self):
        print("\nIntermediate Code (Pass-I Output):")
        for line in self.intermediate_code:
            print(line)

# Example input for source code containing macro definitions and calls
source_code = [
    "MACRO INCR &ARG1",
    "LOAD &ARG1",
    "ADD =1",
    "STORE &ARG1",
    "MEND",
    "MACRO DECR &ARG1",
    "LOAD &ARG1",
    "SUB =1",
    "STORE &ARG1",
    "MEND",
    "START 100",
    "INCR A",  # Macro call
    "DECR B",  # Macro call
    "END"
]

# Initialize Pass-I to generate MNT and MDT
macro_processor_pass_one = MacroProcessorPassOne()
macro_processor_pass_one.pass_one(source_code)

# Now Pass-I is complete, let's print MNT, MDT, and Intermediate Code
macro_processor_pass_one.print_mnt_mdt()
macro_processor_pass_one.print_intermediate_code()