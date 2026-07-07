from pathlib import Path
from git import Repo

# apps/api/app/storage/repositories
BASE_PATH = (
    Path(__file__)
    .resolve()
    .parents[2]
    / "storage"
    / "repositories"
)

BASE_PATH.mkdir(parents=True, exist_ok=True)


class GitService:

    @staticmethod
    def clone(url: str, repository_name: str):

        repo_path = BASE_PATH / repository_name

        if repo_path.exists():
            return str(repo_path)

        Repo.clone_from(
            url,
            repo_path,
        )

        return str(repo_path)