from typing import (
    cast,
    List
)
from unittest import TestCase

from lpp.ast import (
    Program,
    LetStatement,
    Identifier,
    LetStatement
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
        parser:Parser =  Parser(lexer)

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
        parser:Parser =  Parser(lexer)

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
        print(parser.errors)

        self.assertEquals(len(parser.errors), 1)
