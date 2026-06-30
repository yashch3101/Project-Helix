import os


def collect_files(repository_path):

    files = []

    for root, _, filenames in os.walk(repository_path):

        for filename in filenames:

            full_path = os.path.join(
                root,
                filename,
            )

            files.append(full_path)

    return files