import re
from app.modules.parser.utils import find_block_end


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

        export_default_pattern = re.compile(
            r"export\s+default\s+function\s+([A-Za-z0-9_]+)"
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
            r"(?:const|let|var)\s+([A-Za-z0-9_]+)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[A-Za-z0-9_]+)\s*=>"
        )

        export_arrow_pattern = re.compile(
            r"export\s+const\s+([A-Za-z0-9_]+)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[A-Za-z0-9_]+)\s*=>"
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

                    "line_end": find_block_end(
                        lines,
                        line_no,
                    ),

                    "parent": None,

                    "docstring": None,

                    "inherits": [],

                    "decorators": [],

                    "parameters": [],

                    "return_type": None,

                    "is_async": False,

                })

            # ---------------- Export Default Function ----------------

            match = export_default_pattern.search(line)
            
            if match:
            
                symbols.append({
            
                    "name": match.group(1),
            
                    "type": "function",
            
                    "line_start": line_no,
            
                    "line_end": find_block_end(
                        lines,
                        line_no,
                    ),
            
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

                    "line_end": find_block_end(
                        lines,
                        line_no,
                    ),

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

            if match and not async_pattern.search(line) and not export_default_pattern.search(line):

                symbols.append({

                    "name": match.group(1),

                    "type": "function",

                    "line_start": line_no,

                    "line_end": find_block_end(
                        lines,
                        line_no,
                    ),

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

                    "line_end": find_block_end(
                        lines,
                        line_no,
                    ),

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

                    "line_end": find_block_end(
                        lines,
                        line_no,
                    ),

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

                    "line_end": find_block_end(
                        lines,
                        line_no,
                    ),

                    "parent": None,

                    "docstring": None,

                    "inherits": [],

                    "decorators": [],

                    "parameters": [],

                    "return_type": None,

                    "is_async": False,

                })

            # ---------------- Export Arrow Function ----------------

            match = export_arrow_pattern.search(line)
            
            if match:
            
                symbols.append({
            
                    "name": match.group(1),
            
                    "type": "arrow_function",
            
                    "line_start": line_no,
            
                    "line_end": find_block_end(
                        lines,
                        line_no,
                    ),
            
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

                    "line_end": find_block_end(
                        lines,
                        line_no,
                    ),

                    "parent": None,

                    "docstring": None,

                    "inherits": [],

                    "decorators": [],

                    "parameters": [],

                    "return_type": None,

                    "is_async": False,

                })

        return symbols