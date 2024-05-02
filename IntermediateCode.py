import re


def isOperand(char):
    match = re.match(r"^([^+\-%*/^)([\]{}]+)", char)
    return True if match else False


def hasHigherPrecedence(stackChar, char):
    precendence = {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
        "%": 2,
        "^": 3,
        "(": 4,
        "[": 4,
        "{": 4,
    }

    # handle special case of right associativity
    if stackChar == "^" and char == "^":
        return False

    return True if precendence[stackChar] >= precendence[char] else False


class TreeNode:
    def __init__(self, value) -> None:
        self.left = None
        self.value = value
        self.right = None


def postfix(expression):
    postExpression = ""
    stack = []
    for char in expression.split():
        if char == "(":
            stack.append(char)
        elif char == ")":
            x = stack.pop()
            while x != "(":
                postExpression += " " + x
                x = stack.pop()
        elif isOperand(char):
            postExpression += " " + char
        elif not isOperand(char):
            if len(stack) == 0:
                stack.append(char)
            else:
                topOfStack = stack[len(stack) - 1]
                if hasHigherPrecedence(topOfStack, char) and topOfStack != "(":
                    while (
                        len(stack) != 0
                        and hasHigherPrecedence(stack[len(stack) - 1], char)
                        and stack[len(stack) - 1] != "("
                    ):
                        x = stack.pop()
                        postExpression += " " + x

                stack.append(char)

    while len(stack) != 0:
        x = stack.pop()
        if x != "(":
            postExpression += " " + x

    return postExpression


def threeAddressCode(postExpression):
    stack = []
    variableCount = 1
    for char in postExpression.split():
        if isOperand(char):
            stack.append(char)
        else:
            A = stack.pop()
            B = stack.pop()
            print(f"T{variableCount} := {A} {char} {B}")
            variable = f"T{variableCount}"
            stack.append(variable)
            variableCount += 1


def constructTree(postExpression):
    stack = []
    for char in postExpression.split():
        if isOperand(char):
            stack.append(TreeNode(char))
        else:
            A = stack.pop()
            B = stack.pop()
            operatorNode = TreeNode(char)
            operatorNode.left = A
            operatorNode.right = B
            stack.append(operatorNode)

    return stack.pop()


def printTree(node, depth):
    if node is None:
        return
    print("     " * depth + str(node.value))
    printTree(node.left, depth + 1)
    printTree(node.right, depth + 1)


expression = "a + 32 + b + ( c + 37 )"

pos = postfix(expression)
print("Postfix: ", pos)
print("TAC")
threeAddressCode(pos)
root = constructTree(pos)
print("Syntax tree")
printTree(root, 0)
