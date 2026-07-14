import ast


class SymbolVisitor(ast.NodeVisitor):

    def __init__(self):
        self.symbols = []
        self.parent_stack = []
        self.current_function = None

    def visit_ClassDef(self, node):

        bases = []

        for base in node.bases:
            try:
                bases.append(ast.unparse(base))
            except Exception:
                bases.append("Unknown")

        self.symbols.append(
            {
                "name": node.name,
                "type": "class",
                "line_start": node.lineno,
                "line_end": node.end_lineno,
                "parent": self.parent_stack[-1] if self.parent_stack else None,
                "docstring": ast.get_docstring(node),
                "inherits": bases,
                "decorators": [
                    ast.unparse(d)
                    for d in node.decorator_list
                ],
                "parameters": [],
                "return_type": None,
                "is_async": False,
            }
        )

        self.parent_stack.append(node.name)
        self.generic_visit(node)
        self.parent_stack.pop()

    def visit_FunctionDef(self, node):

        self.symbols.append(
            {
                "name": node.name,
                "type": "function",
                "line_start": node.lineno,
                "line_end": node.end_lineno,
                "parent": self.parent_stack[-1] if self.parent_stack else None,
                "docstring": ast.get_docstring(node),
                "inherits": [],
                "decorators": [
                    ast.unparse(d)
                    for d in node.decorator_list
                ],
                "parameters": [
                    arg.arg
                    for arg in node.args.args
                ],
                "return_type": (
                    ast.unparse(node.returns)
                    if node.returns
                    else None
                ),
                "is_async": False,
            }
        )

        previous_function = self.current_function

        self.current_function = node.name

        self.parent_stack.append(node.name)

        self.generic_visit(node)

        self.parent_stack.pop()

        self.current_function = previous_function

    def visit_AsyncFunctionDef(self, node):

        self.symbols.append(
            {
                "name": node.name,
                "type": "function",
                "line_start": node.lineno,
                "line_end": node.end_lineno,
                "parent": self.parent_stack[-1] if self.parent_stack else None,
                "docstring": ast.get_docstring(node),
                "inherits": [],
                "decorators": [
                    ast.unparse(d)
                    for d in node.decorator_list
                ],
                "parameters": [
                    arg.arg
                    for arg in node.args.args
                ],
                "return_type": (
                    ast.unparse(node.returns)
                    if node.returns
                    else None
                ),
                "is_async": True,
            }
        )

        previous_function = self.current_function

        self.current_function = node.name

        self.parent_stack.append(node.name)

        self.generic_visit(node)

        self.parent_stack.pop()

        self.current_function = previous_function

    def visit_Import(self, node):

        for alias in node.names:

            self.symbols.append(
                {
                    "name": alias.name,
                    "type": "import",
                    "line_start": node.lineno,
                    "line_end": node.end_lineno,
                    "parent": self.parent_stack[-1] if self.parent_stack else None,
                    "docstring": None,
                    "inherits": [],
                    "decorators": [],
                    "parameters": [],
                    "return_type": None,
                    "is_async": False,
                }
            )

    def visit_ImportFrom(self, node):

            module = node.module or ""

            for alias in node.names:

                self.symbols.append(
                    {
                        "name": f"{module}.{alias.name}",
                        "type": "import",
                        "line_start": node.lineno,
                        "line_end": node.end_lineno,
                        "parent": self.parent_stack[-1] if self.parent_stack else None,
                        "docstring": None,
                        "inherits": [],
                        "decorators": [],
                        "parameters": [],
                        "return_type": None,
                        "is_async": False,
                    }
                )

            self.generic_visit(node)

    def visit_Call(self, node):

        if self.current_function:

            try:
                called = ast.unparse(node.func)

                if len(called) > 255:
                    called = called[:255]
                    
            except Exception:
                called = "unknown"

            self.symbols.append(
                {
                    "name": called,
                    "type": "call",
                    "line_start": node.lineno,
                    "line_end": node.end_lineno,
                    "parent": self.current_function,
                    "docstring": None,
                    "inherits": [],
                    "decorators": [],
                    "parameters": [],
                    "return_type": None,
                    "is_async": False,
                }
            )

        self.generic_visit(node)

class PythonParser:

    @staticmethod
    def parse(file_path: str):

        with open(
            file_path,
            encoding="utf-8",
            errors="ignore",
        ) as f:

            tree = ast.parse(f.read())

        visitor = SymbolVisitor()

        visitor.visit(tree)

        return visitor.symbols