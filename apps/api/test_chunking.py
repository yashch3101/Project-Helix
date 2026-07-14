from app.modules.chunking.splitter import CodeSplitter

chunks = CodeSplitter.split(
    "app/main.py"
)

print(len(chunks))

for chunk in chunks:

    print("=" * 80)

    print(chunk["start_line"])

    print(chunk["end_line"])

    print(chunk["content"][:150])