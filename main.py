import llvmlite.binding as llvm
import llvmlite.ir as ll
from rply import LexingError, ParsingError

from mini.analysis.lexer import Lexer
from mini.analysis.parser import Parser
from mini.internals.wrapper import InternalModuleLLVM
from mini.utils.file_io import Read, Write
from mini.utils.logger import setup_logger
from mini.analysis.state import State

from sys import argv

from os.path import splitext

logger = setup_logger()

root_state = State(current_file=argv[1], logger=logger)

module = InternalModuleLLVM(root_state)

data = Read(argv[1])

lexer = Lexer().build()
parser = Parser(root_state).build()

try:
    tokens = lexer.lex(data)
    tree = parser.parse(tokens)
    tree.build(root_state)

except LexingError as e:
    root_state.error_handler("Usage of unknown characters.", e.getsourcepos())

except ParsingError as e:
    root_state.error_handler("Usage of unknown keywords / characters.", e.getsourcepos())

Write(f"{splitext(root_state.current_file)[0]}.ll", module.build())
