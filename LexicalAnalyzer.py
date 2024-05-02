import re

TOKEN_REGEX = {
    "LABEL": r"^([A-Za-z][A-Z-a-z0-9_]*)\s*:",
    "MNEMONIC": r"^([A-Za-z]+)",
    "OPERAND": r"^([#@]?[A-Za-z0-9]+)",
    "COMMENT": r"^\s*;.*",
    "NEWLINE": r"^\n",
    "WHITESPACE": r"^\s",
}


def tokenize_asm(asm_code):
    tokens = []
    lineCount = 1

    while asm_code:
        matched = False
        for token_type, regex in TOKEN_REGEX.items():
            match = re.match(regex, asm_code)
            if match:
                if token_type != "NEWLINE" and token_type != "WHITESPACE":
                    value = match.group(1) if match.lastindex else match.group(0)
                    tokens.append(
                        {
                            "type": token_type,
                            "value": value,
                            "linenumber": lineCount,
                        }
                    )
                asm_code = asm_code[len(match.group(0)) :]
                matched = True
                break

        if not matched:
            raise SyntaxError(
                f"Unexpected charachter at line {lineCount}:{asm_code[0]}"
            )
        if match.group(0) == "\n":
            lineCount += 1

    return tokens


# Example of assembly code
asm_code = """
START: LDA #20    ; Loading value into accumlator
       ADD #32    ; Adding value with value in accumlator
       STA RESULT ; Storing result in RESULT
       HTL        ; halt
"""

# tokenizing the assembly code
tokens = tokenize_asm(asm_code)

# printing the tokens
for token in tokens:
    print(token)
