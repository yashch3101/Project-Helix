import ast


class PythonDependencyParser:

    @staticmethod
    def parse(file_path: str):

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as f:
            source = f.read()

        tree = ast.parse(source)

        dependencies = []

        class Visitor(ast.NodeVisitor):

            def visit_Import(
                self,
                node,
            ):

                for alias in node.names:

                    dependencies.append(
                        {
                            "type": "import",
                            "target": alias.name,
                        }
                    )

                self.generic_visit(node)

            def visit_ImportFrom(
                self,
                node,
            ):

                module = node.module or ""

                for alias in node.names:

                    dependencies.append(
                        {
                            "type": "import",
                            "target": f"{module}.{alias.name}",
                        }
                    )

                self.generic_visit(node)

            def visit_Call(
                self,
                node,
            ):

                target = None

                if isinstance(
                    node.func,
                    ast.Name,
                ):
                    target = node.func.id

                elif isinstance(
                    node.func,
                    ast.Attribute,
                ):
                    target = node.func.attr

                if target:

                    dependencies.append(
                        {
                            "type": "call",
                            "target": target,
                        }
                    )

                self.generic_visit(node)

            def visit_ClassDef(
                self,
                node,
            ):

                for base in node.bases:

                    if isinstance(base, ast.Name):

                        dependencies.append(
                            {
                                "type": "inherits",
                                "source": node.name,
                                "target": base.id,
                            }
                        )

                    elif isinstance(base, ast.Attribute):

                        dependencies.append(
                            {
                                "type": "inherits",
                                "source": node.name,
                                "target": base.attr,
                            }
                        )

                self.generic_visit(node)

            def visit_FunctionDef(
                self,
                node,
            ):

                for decorator in node.decorator_list:

                    if isinstance(decorator, ast.Name):

                        dependencies.append(
                            {
                                "type": "decorator",
                                "source": node.name,
                                "target": decorator.id,
                            }
                        )

                    elif isinstance(decorator, ast.Attribute):

                        dependencies.append(
                            {
                                "type": "decorator",
                                "source": node.name,
                                "target": decorator.attr,
                            }
                        )

                    elif isinstance(decorator, ast.Call):

                        if isinstance(decorator.func, ast.Attribute):

                            dependencies.append(
                                {
                                    "type": "decorator",
                                    "source": node.name,
                                    "target": decorator.func.attr,
                                }
                            )

                self.generic_visit(node)

        Visitor().visit(tree)

        return dependencies