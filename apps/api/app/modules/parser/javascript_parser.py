import re


class JavaScriptParser:

    @staticmethod
    def parse(file_path: str):

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as f:
            code = f.read()

        symbols = []

        lines = code.split("\n")

        # ----------------------------------------------------
        # IMPORTS
        # ----------------------------------------------------

        import_pattern = re.compile(
            r'^\s*import\s+(.*?)\s+from\s+[\'"](.*?)[\'"]'
        )

        # ----------------------------------------------------
        # EXPORTS
        # ----------------------------------------------------

        export_pattern = re.compile(
            r'^\s*export\s+'
        )

        # ----------------------------------------------------
        # FUNCTION
        # ----------------------------------------------------

        function_pattern = re.compile(
            r'function\s+([A-Za-z0-9_]+)'
        )

        # ----------------------------------------------------
        # ASYNC FUNCTION
        # ----------------------------------------------------

        async_pattern = re.compile(
            r'async\s+function\s+([A-Za-z0-9_]+)'
        )

        # ----------------------------------------------------
        # CLASS
        # ----------------------------------------------------

        class_pattern = re.compile(
            r'class\s+([A-Za-z0-9_]+)'
        )

        # ----------------------------------------------------
        # ARROW FUNCTION
        # ----------------------------------------------------

        arrow_pattern = re.compile(
            r'const\s+([A-Za-z0-9_]+)\s*=\s*(?:async\s*)?\('
        )

        # ----------------------------------------------------
        # VARIABLES
        # ----------------------------------------------------

        variable_pattern = re.compile(
            r'(?:const|let|var)\s+([A-Za-z0-9_]+)'
        )

        for index, line in enumerate(lines):

            line_no = index + 1

            # ---------------- Import ----------------

            match = import_pattern.search(line)

            if match:

                symbols.append({

                    "name": match.group(2),

                    "type": "import",

                    "line_start": line_no,

                    "line_end": line_no,

                    "parent": None,

                    "docstring": None,

                    "inherits": [],

                    "decorators": [],

                    "parameters": [],

                    "return_type": None,

                    "is_async": False,

                })

            # ---------------- Export ----------------

            if export_pattern.search(line):

                symbols.append({

                    "name": "export",

                    "type": "export",

                    "line_start": line_no,

                    "line_end": line_no,

                    "parent": None,

                    "docstring": None,

                    "inherits": [],

                    "decorators": [],

                    "parameters": [],

                    "return_type": None,

                    "is_async": False,

                })

            # ---------------- Function ----------------

            match = function_pattern.search(line)

            if match:

                symbols.append({

                    "name": match.group(1),

                    "type": "function",

                    "line_start": line_no,

                    "line_end": line_no,

                    "parent": None,

                    "docstring": None,

                    "inherits": [],

                    "decorators": [],

                    "parameters": [],

                    "return_type": None,

                    "is_async": False,

                })

            # ---------------- Async Function ----------------

            match = async_pattern.search(line)

            if match:

                symbols.append({

                    "name": match.group(1),

                    "type": "function",

                    "line_start": line_no,

                    "line_end": line_no,

                    "parent": None,

                    "docstring": None,

                    "inherits": [],

                    "decorators": [],

                    "parameters": [],

                    "return_type": None,

                    "is_async": True,

                })

            # ---------------- Class ----------------

            match = class_pattern.search(line)

            if match:

                symbols.append({

                    "name": match.group(1),

                    "type": "class",

                    "line_start": line_no,

                    "line_end": line_no,

                    "parent": None,

                    "docstring": None,

                    "inherits": [],

                    "decorators": [],

                    "parameters": [],

                    "return_type": None,

                    "is_async": False,

                })

            # ---------------- Arrow Function ----------------

            match = arrow_pattern.search(line)

            if match:

                symbols.append({

                    "name": match.group(1),

                    "type": "arrow_function",

                    "line_start": line_no,

                    "line_end": line_no,

                    "parent": None,

                    "docstring": None,

                    "inherits": [],

                    "decorators": [],

                    "parameters": [],

                    "return_type": None,

                    "is_async": False,

                })

            # ---------------- Variables ----------------

            match = variable_pattern.search(line)

            if match:

                symbols.append({

                    "name": match.group(1),

                    "type": "variable",

                    "line_start": line_no,

                    "line_end": line_no,

                    "parent": None,

                    "docstring": None,

                    "inherits": [],

                    "decorators": [],

                    "parameters": [],

                    "return_type": None,

                    "is_async": False,

                })

        return symbols