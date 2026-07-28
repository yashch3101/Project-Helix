def find_block_end(lines, start_line):
    """
    Finds the closing brace of a JS/TS block.
    Returns ending line number.
    """

    brace_count = 0
    started = False

    for i in range(start_line - 1, len(lines)):
        line = lines[i]

        brace_count += line.count("{")

        if "{" in line:
            started = True

        brace_count -= line.count("}")

        if started and brace_count == 0:
            return i + 1

    return start_line