from rply import LexerGenerator


class Lexer:
    def __init__(self):
        self.lg = LexerGenerator()

    def build(self):
        # --- Keywords --- #
        self.lg.add("LET", r"let")
        self.lg.add("FN", r"fn")
        self.lg.add("RET", r"return")

        self.lg.add("TO", r"to")

        # --- Reserved --- #
        self.lg.add("TRUE", r"true")
        self.lg.add("FALSE", r"false")

        # --- Modifiers --- #

        self.lg.add("PTR", r"ptr")
        self.lg.add("REF", r"ref")
        self.lg.add("DEREF", r"deref")
        self.lg.add("ADDR", r"addr")

        # --- Punctuations --- #
        self.lg.add("(", r"\(")
        self.lg.add(")", r"\)")

        self.lg.add("{", r"\{")
        self.lg.add("}", r"\}")

        self.lg.add("=", r"\=")
        self.lg.add(";", r"\;")
        self.lg.add(",", r"\,")

        # --- Base Tokens --- #
        self.lg.add("FLOAT", r"[-]?\d+[.]\d+")
        self.lg.add("NUMBER", r"[-]?\d+")
        self.lg.add("IDENTIFIER", r"[_\w]+[_\w0-9]*")

        self.lg.ignore(r"\s+")

        return self.lg.build()
