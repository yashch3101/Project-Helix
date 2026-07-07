from app.modules.parser.file_scanner import FileScanner


files = FileScanner.scan(
    "app/storage/repositories/fastapi"
)

print(f"Total Files : {len(files)}")

for file in files[:10]:
    print(file)