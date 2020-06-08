import warnings

from rply import ParserGenerator, Token
from rply.errors import ParserGeneratorWarning

from soda.generation.ast import *


class Parser:
    def __init__(self, state):
        self.pg = ParserGenerator(
            tokens=["FN",
                    "LET", "RET",
                    "(", ")", "=", ";",
                    "{", "}", ",",
                    "NUMBER", "FLOAT",
                    "FALSE", "TRUE",
                    "IDENTIFIER"],
            precedence=[
                ("left", ["NUMBER", "FLOAT"]),
                ("left", ["IDENTIFIER"]),
                ("left", [",", ";"]),
                ("left", ["FN", "LET", "RET"]),
                ("left", ["="]),
                ("left", ["{", "}"]),
                ("left", ["(", ")"]),

            ],
            cache_id="mini_cache"
        )

        self.state = state

    def build(self):
        # bug poop
        @self.pg.production("program : definitions")
        def program_definitions(p):
            return ProgramNode(p[0])

        @self.pg.production("definitions : definitions definitions")
        @self.pg.production("definitions : definition")
        def definitions_all(p):
            return DefinitionsNode(p)

        @self.pg.production("definition : statements")
        @self.pg.production("definition : functions")
        def definition_all(p):
            return p[0]

        @self.pg.production("functions : functions functions")
        @self.pg.production("functions : function")
        def functions_all(p):
            return FunctionsNode(p)

        @self.pg.production("function : FN type IDENTIFIER arguments closure")
        def function_def(p):
            return FunctionNode(p[0], p[1], p[2], p[3], p[4])

        @self.pg.production("closure : { statements }")
        @self.pg.production("closure : { }")
        def closure_all(p):
            if len(p) == 3:
                return ClosureNode([p[1]])
            else:
                return ClosureNode([])

        @self.pg.production("arguments : ( internal_arguments )")
        @self.pg.production("arguments : ( )")
        def arguments_paren_internal(p):
            if len(p) == 3:
                return ArgumentsNode([p[1]])
            else:
                return ArgumentsNode([])

        @self.pg.production("internal_arguments : internal_arguments , internal_argument")
        @self.pg.production("internal_arguments : internal_argument , internal_argument")
        @self.pg.production("internal_arguments : internal_argument")
        def internal_arguments(p):
            tmp = []
            for tok in p:
                if not hasattr(tok, "gettokentype"):
                    tmp.append(tok)
            return ArgumentsNode(tmp)

        @self.pg.production("internal_argument : IDENTIFIER type")
        def internal_argument(p):
            return ArgumentNode(p[0], p[1])

        @self.pg.production("statements : statements statements")
        @self.pg.production("statements : statement")
        def statements_all(p):
            return StatementsNode(p)

        @self.pg.production("statement : IDENTIFIER call")
        @self.pg.production("expr : IDENTIFIER call")
        def statements_call(p):
            return CallNode(p[0], p[1])

        @self.pg.production("call : ( )")
        @self.pg.production("call : ( call_arguments )")
        def call_op(p):
            if len(p) == 2:
                return CallOpNode([])
            else:
                return CallOpNode([p[1]])

        @self.pg.production("call_arguments : call_arguments , call_arguments")
        @self.pg.production("call_arguments : expr , expr")
        @self.pg.production("call_arguments : expr")
        def call_arguments(p):
            temp = []
            for tok in p:
                if not isinstance(tok, Token):
                    temp.append(tok)

            return CallArgumentsNode(temp)

        @self.pg.production("statement : RET expr ;")
        def statement_return(p):
            return ReturnNode(p[0], p[1])

        @self.pg.production("statement : LET IDENTIFIER type = expr ;")
        def statements_let(p):
            return LetNode(p[1], p[2], p[4])

        @self.pg.production("statement : LET IDENTIFIER = expr ;")
        def statements_let(p):
            return LetNode(p[1], None, p[3])

        @self.pg.production("statement : LET IDENTIFIER type ;")
        def statements_let(p):
            return LetNode(p[1], p[2], None)

        @self.pg.production("expr : ( expr )")
        def expr_paren_expr(p):
            return p[1]

        @self.pg.production("expr : IDENTIFIER")
        def expr_identifier(p):
            return VariableNode(p[0])

        @self.pg.production("expr : TRUE")
        @self.pg.production("expr : FALSE")
        def expr_boolean(p):
            return BoolNode(p[0])

        @self.pg.production("expr : NUMBER")
        def expr_number(p):
            return NumberNode(p[0])

        @self.pg.production("expr : FLOAT")
        def expr_number(p):
            return FloatNode(p[0])

        @self.pg.production("expr : FLOAT")
        def expr_number(p):
            return FloatNode(p[0])

        @self.pg.production("type : ( IDENTIFIER )")
        def type_identifier(p):
            return TypeNode(p[1])

        @self.pg.error
        def error_handler(token):
            self.state.error_handler("Came across unexpected token.", token.getsourcepos())

        warnings.filterwarnings("ignore", category=ParserGeneratorWarning)
        return self.pg.build()
