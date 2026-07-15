from app.modules.parser.python_ast_parser import PythonParser
from app.modules.parser.javascript_parser import JavaScriptParser
from app.modules.parser.typescript_parser import TypeScriptParser


class ParserFactory:

    @staticmethod
    def get_parser(extension: str):

        if extension == ".py":
            return PythonParser

        if extension in [".js", ".jsx"]:
            return JavaScriptParser

        if extension in [".ts", ".tsx"]:
            return TypeScriptParser

        return None