from app.modules.dependency_graph.python_dependency_parser import (
    PythonDependencyParser,
)

path = (
    "app/storage/repositories/"
    "fastapi/fastapi/applications.py"
)

deps = PythonDependencyParser.parse(path)

print("Dependencies:", len(deps))

for dep in deps[:20]:
    print(dep)