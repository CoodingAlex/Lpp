from abc import (
    ABC,
    abstractmethod,
)

from typing import (
    List,
    Optional
)

from lpp.token import Token


class ASTNode(ABC):

    @abstractmethod
    def token_literal(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class Statement(ASTNode):

    def __init__(self, token: Token):
        self.token = token

    def token_literal(self) -> str:
        return self.token.literal


class Expression(ASTNode):

    def __init__(self, token: Token):
        self.token = token

    def token_literal(self) -> str:
        return self.token.literal


class Program(ASTNode):

    def __init__(self, statements: List[Statement]) -> None:
        self.statements = statements

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literal()

        return ''

    def __str__(self) -> str:
        out: List[str] = []
        for statements in self.statements:
            out.append(str(statements))

        return ''.join(out)


class Identifier(Expression):

    def __init__(self,
                 token: Token,
                 value: str) -> None:
        super().__init__(token)
        self.value = value

    def __str__(self) -> str:
        return self.value


class LetStatement(Statement):

    def __init__(self,
                 token: Token,
                 name: Optional[Identifier] = None,
                 value: Optional[Expression] = None) -> None:

        super().__init__(token)
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return f'{self.token_literal()} {str(self.name)} = {str(self.value)};'


class ReturnStatement(Statement):

    def __init__(self,
                 token: Token,
                 return_value: Optional[Expression] = None) -> None:
        super().__init__(token)
        self.return_value = return_value

    def __str__(self) -> str:
        return f'{self.token_literal()} {str(self.return_value)};'


class ExpressionStatement(Statement):
    def __init__(self,
                 token: Token,
                 expression: Optional[Expression] = None) -> None:
        super().__init__(token)
        self.expression = expression

    def __str__(self) -> str:
        return str(self.expression)


class Integer(Expression):

    def __init__(self,
                 token: Token,
                 value: Optional[int] = None) -> None:
        super().__init__(token)
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Prefix(Expression):

    def __init__(self,
                 token: Token,
                 operator: str,
                 right: Optional[Expression] = None) -> None:
        super().__init__(token)
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return f'({self.operator}{str(self.right)})'
