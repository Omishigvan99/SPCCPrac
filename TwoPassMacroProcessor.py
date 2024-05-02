import re


class MDTFormat:
    def __init__(self, definition) -> None:
        self.definition = definition


class MNTFormat:
    def __init__(self, name, mdtIndex) -> None:
        self.name = name
        self.mdtIndex = mdtIndex


class ALAFormat:
    def __init__(self, arg1, arg2) -> None:
        self.argumentList = [arg1, arg2]


class MacroProcessor:
    def __init__(self):
        self.MNT = []
        self.MDT = []
        self.ALA = {}
        self.output_lines = []

    def pass1(self, input_lines):
        MNTC = 0
        MDTC = 0

        for lineNumber, line in enumerate(input_lines):
            tokens = line.split()
            if "MACRO" in tokens:
                self.MNT.append(MNTFormat(tokens[1], MDTC))
                arg1, arg2 = re.split(r"[,\s]", tokens[2])
                self.ALA[tokens[1]] = ALAFormat(arg1, arg2)
                MNTC += 1
                for def_line in input_lines[lineNumber + 1 :]:
                    def_tokens = def_line.split()
                    if "MEND" in def_tokens:
                        self.MDT.append(MDTFormat(def_line))
                        MDTC += 1
                        break

                    self.MDT.append(MDTFormat(def_line))
                    MDTC += 1

    def pass2(self, input_lines):
        MDTP = None
        macroNameRegex = ""
        # get all macro names
        for macroNameEntry in self.MNT:
            macroNameRegex += f"({macroNameEntry.name})|"
        macroNameRegex = macroNameRegex[: len(macroNameRegex) - 1]

        for line in input_lines:
            match = re.match(macroNameRegex, line)
            matched = False
            if match:
                matched = True
                macroName = match.group()
                for macroNameEntry in self.MNT:
                    if macroNameEntry.name == macroName:
                        MDTP = macroNameEntry.mdtIndex

                tokens = line.split()
                arg1, arg2 = re.split(r"[,\s]", tokens[1])

                for mdtEntry in self.MDT[MDTP:]:
                    definition = mdtEntry.definition
                    if re.match("MEND", definition):
                        break
                    definition = definition.replace(
                        self.ALA[macroName].argumentList[0], arg1
                    )
                    definition = definition.replace(
                        self.ALA[macroName].argumentList[1], arg2
                    )
                    self.output_lines.append(definition)
            if not matched:
                self.output_lines.append(line)

    def print_output(self):
        for line in self.output_lines:
            print(line)


if __name__ == "__main__":
    input_lines = [
        "START",
        "MACRO mADD &1,&2",
        "MOV A,&1",
        "ADD A,&2",
        "MEND",
        "MACRO mSUB &1,&2",
        "MOV A,&1",
        "SUB A,&2",
        "MEND",
        "CODE",
        "mADD 10,20",
        "mSUB 30,20",
        "END",
    ]

    macro_processor = MacroProcessor()
    macro_processor.pass1(input_lines)
    macro_processor.pass2(input_lines)
    macro_processor.print_output()
