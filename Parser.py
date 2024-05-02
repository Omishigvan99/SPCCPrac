def calculate_first(grammar):
    first = {}
    terminals = set()
    non_terminals = set(grammar.keys())
    visited = set()
    for productions in grammar.values():
        for production in productions:
            terminals |= set(production)

    terminals -= non_terminals

    for symbol in non_terminals:
        first[symbol] = set()

    def recursiveFirst(symbol):
        firstSet = set()
        for productions in grammar[symbol]:
            for index, production in enumerate(productions):
                if production in terminals:
                    firstSet.add(production)
                    break

                if production in non_terminals:
                    if production not in visited:
                        visited.add(production)
                        firstSet |= recursiveFirst(production)

                        if "" in firstSet and index != len(productions) - 1:
                            firstSet.remove("")
                            continue
                        break

        return firstSet

    for symbol in grammar.keys():
        first[symbol] = recursiveFirst(symbol)
        visited.clear()

    return first


def calculate_follow(grammar, startSymbol):
    follow = {}
    terminals = set()
    non_terminals = set(grammar.keys())
    visited = set()
    for productions in grammar.values():
        for production in productions:
            terminals |= set(production)

    terminals -= non_terminals

    for symbol in non_terminals:
        follow[symbol] = set()

    follow[startSymbol] = {"$"}

    def recurrsiveFollow(symbol):
        followSet = set()

        if symbol in visited:
            return follow[symbol]

        for grammarKey, grammarValue in grammar.items():
            for productions in grammarValue:
                if symbol in productions:
                    followIndex = productions.index(symbol) + 1

                    if followIndex >= len(productions):
                        followSet = recurrsiveFollow(grammarKey)
                        visited.add(grammarKey)
                    else:
                        if productions[followIndex] in terminals:
                            followSet.add(productions[followIndex])

                        if productions[followIndex] in non_terminals:
                            followSet |= first[productions[followIndex]]
                            if "" in followSet:
                                followSet.remove("")
                                continue

        return followSet

    for symbol in grammar.keys():
        follow[symbol] |= recurrsiveFollow(symbol)
        visited.add(follow)


if __name__ == "__main__":
    grammar = {
        "S": [["A", "B"]],
        "A": [["a", "B"], [""]],
        "B": [["b"], [""]],
    }
    first = calculate_first(grammar)
    follow = calculate_follow(grammar, "S")
