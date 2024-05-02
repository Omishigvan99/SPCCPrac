import re


class Assembler:
    mnemonicTable = {
        "LD": "0001",
        "ADD": "0010",
        "HLT": "1111",
    }
    registerTable = {
        "R0": "00",
        "R1": "01",
        "R2": "10",
        "R3": "11",
    }

    def __init__(self) -> None:
        self.symbolTable = {}
        self.literalTable = {}
        self.registerTable = {}
        self.machineCode = []

    def pass1(self, asm_code):
        address = 0
        literalCount = 0
        for line in asm_code:
            if line.endswith(":"):
                line = line[:-1]
                self.symbolTable[line] = address
            elif line.startswith("."):
                line = line[1:]
                self.registerTable[line] = address
            else:
                tokens = line.split()
                for token in tokens:
                    if token.startswith("="):
                        if token[1:] not in self.literalTable:
                            self.literalTable[token[1:]] = f"L{literalCount}"
                            literalCount += 1
                address += 1

    def pass2(self, asm_code):
        for line in asm_code:
            if line.endswith(":"):
                continue
            elif line.startswith("."):
                continue
            else:
                tokens = re.split(r"[,\s]+", line)
                print(tokens)
                for i, token in enumerate(tokens):
                    if token in self.symbolTable:
                        tokens[i] = str(self.symbolTable[token])
                    if token in self.literalTable:
                        tokens[i] = str(self.literalTable[token])
                    if token in Assembler.mnemonicTable:
                        tokens[i] = str(Assembler.mnemonicTable[token])
                    if token in Assembler.registerTable:
                        tokens[i] = str(Assembler.registerTable[token])

                self.machineCode.append(" ".join(tokens))

    def printMachineCode(self):
        for code in self.machineCode:
            print(code)


asm_code = [
    "START:",
    ".ORG 100",
    "LD R0 , #10",
    "LD R1 , =20",
    "ADD R2 , R0 , R1",
    "HLT",
    ".DC 'HELLO', 0",
]

asm = Assembler()
asm.pass1(asm_code)
asm.pass2(asm_code)

# Output
print("Symbol Table:")
for symbol, address in asm.symbolTable.items():
    print(symbol + ":", address)

print("\nLiteral Table:")
for literal, address in asm.literalTable.items():
    print(literal + ":", address)

print("\nPseudo Opcode Table:")
for pseudo_opcode, address in asm.registerTable.items():
    print(pseudo_opcode + ":", address)

print("\nMachine Code:")
for instruction in asm.machineCode:
    print(instruction)
