from typing import (
    Any,
    cast,
    List,
    Type
)
from unittest import TestCase

from lpp.ast import (
    Program,
    Integer,
    LetStatement,
    Identifier,
    Expression,
    ExpressionStatement,
    LetStatement,
    Prefix,
    ReturnStatement,
)
from lpp.lexer import Lexer
from lpp.parser import Parser


class ParserTest(TestCase):

    def test_parse_program(self) -> None:
        source: str = 'variable x = 5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertIsNotNone(program)
        self.assertIsInstance(program, Program)

    def test_let_statements(self) -> None:
        source: str = '''
            variable x = 5;
            variable y = 10;
            variable foo = 20;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEqual(len(program.statements), 3)

        for statement in program.statements:
            self.assertEqual(statement.token_literal(), 'variable')
            self.assertIsInstance(statement, LetStatement)

    def test_name_in_let_statements(self) -> None:
        source: str = '''

            variable x = 5;
            variable y = 10;
            variable foo = 20;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        names: List[str] = []
        for statement in program.statements:
            statement = cast(LetStatement, statement)
            assert statement.name is not None
            names.append(statement.name.value)

        expected_names: List[str] = ['x', 'y', 'foo']

        self.assertEquals(names, expected_names)

        # self.assertEqual(cast(Identifier, cast(LetStatement, program.statements[0]).name).value ,'x')
        # self.assertEqual(cast(Identifier, cast(LetStatement, program.statements[1]).name).value ,'y')
        # self.assertEqual(cast(Identifier, cast(LetStatement, program.statements[2]).name).value ,'foo')

    def test_parse_errors(self) -> None:
        source: str = 'variable x 5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEquals(len(parser.errors), 1)

    def test_return_statement(self) -> None:
        source: str = '''
            regresa 5;
            regresa foo;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEquals(len(program.statements), 2)
        for statement in program.statements:
            self.assertEquals(statement.token_literal(), 'regresa')
            self.assertIsInstance(statement, ReturnStatement)

    def test_identifier_expression(self) -> None:
        source: str = 'foobar;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        expression_statement = cast(ExpressionStatement, program.statements[0])

        assert expression_statement.expression is not None
        self._test_literal_expression(
            expression_statement.expression, 'foobar')

    def test_integer_expressions(self):
        source: str = '5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program, expected_statements=1)

        expression_statement = cast(ExpressionStatement, program.statements[0])

        assert expression_statement.expression is not None
        self._test_literal_expression(expression_statement.expression, 5)

    def test_prefix_expression(self) -> None:
        source: str = '!5; -15;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program, expected_statements=2)
        for statement, (expected_operator, expected_value) in zip(
                program.statements, [('!', 5), ('-', 15)]):
            statement = cast(ExpressionStatement, statement)

            prefix = cast(Prefix, statement.expression)
            self.assertEquals(prefix.operator, expected_operator)

            assert prefix.right is not None
            self._test_literal_expression(prefix.right, expected_value)

    def _test_program_statements(self,
                                 parser: Parser,
                                 program: Program,
                                 expected_statements: int = 1) -> None:
        if parser.errors:
            print(parser.errors)

        self.assertEquals(len(parser.errors), 0)
        self.assertEquals(len(program.statements), expected_statements)
        self.assertIsInstance(program.statements[0], ExpressionStatement)

    def _test_literal_expression(self,
                                 expression: Expression,
                                 expected_value: Any) -> None:
        value_type: Type = type(expected_value)

        if value_type == str:
            self._test_identifier(expression, expected_value)
        elif value_type == int:
            self._test_integer(expression, expected_value)
        else:
            self.fail(f'Unhandled type of expression. Got={value_type}')

    def _test_identifier(self,
                         expression: Expression,
                         expected_value: str) -> None:
        self.assertIsInstance(expression, Identifier)

        identifier = cast(Identifier, expression)
        self.assertEquals(identifier.value, expected_value)
        self.assertEquals(identifier.token.literal, expected_value)

    def _test_integer(self,
                      expression,
                      expected_value) -> None:
        self.assertIsInstance(expression, Integer)

        integer = cast(Integer, expression)
        self.assertEquals(integer.value, expected_value)
        self.assertEquals(integer.token.literal, str(expected_value))
