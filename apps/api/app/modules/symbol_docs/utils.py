def extract_symbol_code(
    file_path,
    start,
    end,
):

    with open(
        file_path,
        encoding="utf-8",
    ) as f:

        lines = f.readlines()

    return "".join(

        lines[start - 1:end]

    )