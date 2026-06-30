from pathlib import Path

from git import Repo

BASE_PATH = Path("storage/repositories")


class GitService:

    @staticmethod
    def clone(url: str, repository_name: str):

        path = BASE_PATH / repository_name

        if path.exists():
            return str(path)

        Repo.clone_from(
            url,
            path,
        )

        return str(path)