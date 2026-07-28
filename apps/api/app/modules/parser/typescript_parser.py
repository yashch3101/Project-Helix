from app.modules.parser.javascript_parser import JavaScriptParser


class TypeScriptParser(JavaScriptParser):

    @staticmethod
    def parse(file_path: str):

        symbols = JavaScriptParser.parse(file_path)

        return symbols