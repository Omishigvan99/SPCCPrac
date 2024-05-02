OPCODES = {
    "ADD": 0b000,
    "MUL": 0b001,
    "SUB": 0b010,
}

REGISTERS = {
    "R1": 0b000,
    "R2": 0b001,
    "R3": 0b010,
    "R4": 0b011,
}


def convertToMachineCode(instruction):
    parts = instruction.split()
    opcode = OPCODES[parts[0]]
    dest = REGISTERS[parts[1]]
    src1 = REGISTERS[parts[2]]
    src2 = REGISTERS[parts[3]]

    # Machine code format: opcode(3 bits) dest(3 bits) src1(3 bits) src2( 3 bits)
    machine_code = opcode << 9 | dest << 6 | src1 << 3 | src2
    return machine_code


# three address code instruction
instructions = [
    "ADD R2 R3 R4",
    "MUL R3 R2 R1",
    "SUB R4 R1 R3",
]

# converting instructions to machine code
for instruction in instructions:
    machine_code = convertToMachineCode(instruction)
    print(f"{instruction} --> {bin(machine_code)}")
