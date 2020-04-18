from apps.API_VK.command.CommonCommand import CommonCommand


class Calc(CommonCommand):
    def __init__(self):
        names = ["калькулятор", "кальк", "к", "="]
        help_text = "Калькулятор - считает простые выражения"
        detail_help_text = "=(выражение) - считает выражение. Умеет работать с + - * / ( )"
        super().__init__(names, help_text, detail_help_text)

    def accept(self, vk_event):
        if (vk_event.msg and vk_event.msg[0] == '=') or vk_event.command in self.names:
            return True
        return False

    def start(self):
        if self.vk_event.msg[0] == '=':
            expression = self.vk_event.msg[1:]
        else:
            self.check_args(1)
            expression = self.vk_event.original_args
        expression = expression.replace(' ', '')
        root = build_subtree(expression, compiled_grammars)
        if root is None:
            return "Не смог распартить выражение"
        else:
            if type(root.value) == float and root.value == int(root.value):
                return str(int(root.value))
            else:
                return str(root.value)


# By E.Dubovitsky and A.Popova

grams_raw = ["S->S+T",
             "S->S-T",
             "S->T",
             "T->T*F",
             "T->T/F",
             "T->F",
             "F->(S)",
             "F->R"]
compiled_grammars = []


class Symbol:

    def match(self, expr):
        pass

    def compute(self, left, right):
        pass

    def separations(self, expr):
        pass


class BinaryOperator(Symbol):

    def __init__(self, character):
        self.character = character

    def match(self, expr):
        return expr.find(self.character) > 0

    def separations(self, expr):
        split = expr.split(self.character)
        result = []
        for i in range(1, len(split)):
            left_expr = self.character.join(split[0:i])
            right_expr = self.character.join(split[i:len(split)])
            result.append((left_expr, right_expr))
        return result


class Plus(BinaryOperator):

    def __init__(self):
        super().__init__("+")

    def compute(self, left, right):
        return left + right


class Minus(BinaryOperator):

    def __init__(self):
        super().__init__("-")

    def compute(self, left, right):
        return left - right


class Multiply(BinaryOperator):

    def __init__(self):
        super().__init__("*")

    def compute(self, left, right):
        return left * right


class Divide(BinaryOperator):

    def __init__(self):
        super().__init__("/")

    def compute(self, left, right):
        return left / right


class Power(BinaryOperator):

    def __init__(self):
        super().__init__("^")

    def compute(self, left, right):
        left ** right


class Function(Symbol):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def match(self, expr):
        return expr.startswith(self.left) and expr.endswith(self.right)

    def separations(self, expr):
        return [(expr[len(self.left): -len(self.right)], None)]


class Brackets(Function):

    def __init__(self):
        super().__init__("(", ")")

    def compute(self, left, right):
        return left


# all possible arithmetic operations
computable_symbols = (Plus(), Minus(), Multiply(), Divide(), Power(), Brackets())


# searching arithmetic operation in grammar
def find_symbol(gram_raw_right):
    for symbol in computable_symbols:
        if symbol.match(gram_raw_right):
            return symbol
    return None


def get_possible_grammars(left_sign):
    result = []
    for grammar in compiled_grammars:
        if left_sign is grammar.gram_from:
            result.append(grammar)
    return result


def build_subtree(expr, grammars):
    if not expr:
        return None
    for possible_grammar in grammars:
        child_node = possible_grammar.parse(expr)
        if child_node:
            return child_node
    return None


# Node - parse tree
class Node:
    def __init__(self, grammar, digit=None, left_child=None, right_child=None):
        self.grammar = grammar
        self.left_child = left_child
        self.right_child = right_child
        if left_child is None:
            self.value = digit
        elif grammar.symbol is None:
            self.value = left_child.value
        elif right_child is None:
            self.value = grammar.symbol.compute(left_child.value, None)
        else:
            self.value = grammar.symbol.compute(left_child.value, right_child.value)


class Grammar:
    # splits expression by symbol
    # for example, S->T+S. gram_from = "S", left = "T", symbol = "+", right = "S"

    def __init__(self):
        self.gram_from = None
        self.left = None
        self.symbol = None
        self.right = None

    def parse(self, expr):
        if self.symbol is None:
            if self.left is "R":
                if expr.isdigit():
                    return Node(self, float(expr))
                else:
                    return None
            else:
                child_node = build_subtree(expr, get_possible_grammars(self.left))
                if child_node:
                    return Node(self, None, child_node)
                return None
        else:
            if not self.symbol.match(expr):
                return None
            splits = self.symbol.separations(expr)
            for split in splits:
                possible_node = self.check_separation(split[0], split[1])
                if possible_node is not None:
                    return possible_node
            return None

    def check_separation(self, left_expr, right_expr):
        left_child = build_subtree(left_expr, get_possible_grammars(self.left))
        if left_child is None:
            return None
        right_child = build_subtree(right_expr, get_possible_grammars(self.right))
        if right_expr and right_child is None:
            return None
        return Node(self, None, left_child, right_child)


# grammar compilation
# compiled_grammar is class Grammar instance
for gram_raw in grams_raw:
    compiled_grammar = Grammar()
    split = gram_raw.split("->", 1)
    compiled_grammar.gram_from = split[0]
    gram_to = split[1]
    compiled_grammar.symbol = find_symbol(gram_to)
    if compiled_grammar.symbol is None:
        compiled_grammar.left = gram_to
        compiled_grammar.right = None
    else:
        split = compiled_grammar.symbol.separations(gram_to)
        if len(split) != 1:
            raise Exception("Grammar " + gram_raw + " is not correct")
        compiled_grammar.left = split[0][0]  # left_expr
        compiled_grammar.right = split[0][1]  # right_expr
    compiled_grammars.append(compiled_grammar)
