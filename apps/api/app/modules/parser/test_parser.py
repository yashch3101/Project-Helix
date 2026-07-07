from app.modules.parser.python_ast_parser import PythonParser

symbols = PythonParser.parse(
    "app/storage/repositories/fastapi/fastapi/applications.py"
)

print(f"Total Symbols: {len(symbols)}")

for symbol in symbols:
    if symbol["type"] == "class":
        print(symbol)