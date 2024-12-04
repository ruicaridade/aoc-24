import string
from dataclasses import dataclass
from typing import Literal


def read_input() -> str:
    with open("inputs/day3.txt") as f:
        return f.read()


TokenKind = (
    Literal["identifier"]
    | Literal["number"]
    | Literal["lparen"]
    | Literal["rparen"]
    | Literal["comma"]
)


@dataclass
class Token:
    kind: TokenKind
    value: str | None = None

    def __str__(self) -> str:
        return f"({self.kind}): {self.value}"


@dataclass
class Operation:
    identifier: str
    arguments: list[int]


class OperationMultiply(Operation):
    def __call__(self) -> int:
        value: int | None = None
        for arg in self.arguments:
            if value is None:
                value = arg
            else:
                value *= arg

        if value is None:
            return 0

        return value


class OperationEnable(Operation):
    pass


class OperationDisable(Operation):
    pass


VALID_CHARACTERS = (
    list(string.ascii_lowercase)
    + ["(", ")", ",", "'"]
    + [str(x) for x in list(range(10))]
)
VALID_IDENTIFIERS = {
    "mul": OperationMultiply,
    "do": OperationEnable,
    "don't": OperationDisable,
}


def tokenize(input: str) -> list[Token]:
    """
    Parse the input and return a list of tokens.
    """
    tokens: list[Token] = []
    register: str = ""
    kind: TokenKind | None = None

    def _append_variable_size_token() -> None:
        if len(register) > 0 and kind == "identifier" or kind == "number":
            tokens.append(
                Token(
                    kind=kind,
                    value=register,
                )
            )

    for ch in input.lower():
        if ch == "(":
            _append_variable_size_token()
            tokens.append(Token(kind="lparen"))
            register = ""
            kind = None
        elif ch == ")":
            _append_variable_size_token()
            tokens.append(Token(kind="rparen"))
            register = ""
            kind = None
        elif ch == ",":
            _append_variable_size_token()
            tokens.append(Token(kind="comma"))
            register = ""
            kind = None
        elif ch.isdigit() and kind != "identifier":
            kind = "number"
            register += ch
        else:
            kind = "identifier"
            register += ch

    return tokens


def parse(tokens: list[Token]) -> list[Operation]:
    """
    Parse a list of tokens.
    """
    operations: list[Operation] = []
    for i in range(len(tokens)):
        token = tokens[i]
        if token.kind == "identifier":
            value = token.value
            if value is None:
                continue

            for valid_identifier in VALID_IDENTIFIERS.keys():
                if value.endswith(valid_identifier):
                    arguments: list[int] = []

                    start_index = -1
                    end_index = -1
                    for j in range(len(tokens[i + 1 :])):
                        next_token = tokens[i + j + 1]
                        if start_index == -1 and next_token.kind == "lparen":
                            start_index = i + j + 1
                        elif end_index == -1 and next_token.kind == "rparen":
                            end_index = i + j + 1
                        elif next_token.kind == "identifier":
                            break

                    if start_index == -1 or end_index == -1:
                        break

                    is_valid = True
                    for k, next_token in enumerate(tokens[start_index + 1 : end_index]):
                        if k % 2 == 0:
                            if next_token.value is not None:
                                arguments.append(int(next_token.value))
                        elif k % 2 == 1 and next_token.kind != "comma":
                            is_valid = False
                            break

                    if is_valid:
                        OpCls = VALID_IDENTIFIERS[valid_identifier]
                        operations.append(
                            OpCls(
                                identifier=valid_identifier,
                                arguments=arguments,
                            )
                        )

                    break

    return operations


def execute(ops: list[Operation]) -> int:
    """
    Execute a list of operations.
    """
    result = 0
    enabled = True
    for op in ops:
        match op:
            case OperationEnable():
                enabled = True
            case OperationDisable():
                enabled = False
            case OperationMultiply():
                if enabled:
                    result += op()

    return result


def solve() -> None:
    input = read_input()
    tokens = tokenize(input)
    ops = parse(tokens)

    print("Part 1:", execute([op for op in ops if isinstance(op, OperationMultiply)]))
    print("Part 2:", execute(ops))


if __name__ == "__main__":
    solve()
