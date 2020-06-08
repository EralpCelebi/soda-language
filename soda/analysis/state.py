from linecache import getline
from colorama import Fore, Back, Style

from soda.internals.types import types


class State:
    def __init__(self, current_file=None, module=None, logger=None):
        self.current_file = current_file

        self.module = module
        self.builder = None
        self.basic_block = None

        self.logger = logger

        self.wanted_types = []

        self.current_function = None
        self.current_function_argument_wrapped_types = []
        self.current_function_argument_names = []
        self.current_function_return_type = None
        self.current_function_does_return = False
        self.current_function_has_returned = False

        self.current_call_arguments_values = []
        self.current_call_arguments_llvm_values = []
        self.current_call_arguments_types = []

        self.defined_functions = {}
        self.defined_functions_argument_types = {}

        self.defined_globals = {}
        self.defined_variables = {}
        self.defined_structures = {}

        self.types = types

    def cloneState(self, other):
        self = other

        self.wanted_types = []

        return self

    def enter_function(self):
        self.current_function = None
        self.current_function_argument_wrapped_types = []
        self.current_function_argument_names = []
        self.current_function_return_type = None
        self.current_function_does_return = False
        self.current_function_has_returned = False

    def exit_function(self):
        self.current_function = None
        self.current_function_argument_wrapped_types = []
        self.current_function_argument_names = []
        self.current_function_return_type = None
        self.current_function_does_return = False
        self.current_function_has_returned = False
        self.defined_variables = {}
        self.defined_variables = self.defined_globals

    def info_handler(self, value, span):
        self.logger.info(f"{Fore.WHITE}[{span.colno}:{span.lineno}] {Fore.BLUE} {value} {Fore.RESET}")

        self.logger.info(f"{Fore.GREEN}{getline(self.current_file, span.lineno).rstrip()}{Fore.RESET}")

        self.logger.info(" " * (span.colno - 1) + f"{Fore.CYAN}^{Fore.RESET}\n")

    def warning_handler(self, value, span):
        self.logger.warn(f"{Fore.WHITE}[{span.colno}:{span.lineno}] {Fore.YELLOW} {value} {Fore.RESET}")

        self.logger.warn(f"{Fore.GREEN}{getline(self.current_file, span.lineno).rstrip()}{Fore.RESET}")

        self.logger.warn(" " * (span.colno - 1) + f"{Fore.CYAN}^{Fore.RESET}\n")

    def error_handler(self, value, span):
        self.logger.error(f"{Fore.WHITE}[{span.colno}:{span.lineno}] {Fore.RED} {value} {Fore.RESET}")

        self.logger.error(f"{Fore.GREEN}{getline(self.current_file, span.lineno).rstrip()}{Fore.RESET}")

        self.logger.error(" " * (span.colno - 1) + f"{Fore.CYAN}^{Fore.RESET}\n")
        exit(1)