from pathlib import Path

from git import Repo
from git.exc import GitCommandError

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
    def clone(
        url: str,
        repository_name: str,
    ):

        repo_path = BASE_PATH / repository_name

        if repo_path.exists():
            return str(repo_path)

        try:

            Repo.clone_from(
                url,
                repo_path,
            )

        except GitCommandError as e:

            message = str(e)

            if "Repository not found" in message:

                raise ValueError(
                    "Repository not found."
                )

            if "Authentication failed" in message:

                raise ValueError(
                    "Private repository. Authentication required."
                )

            if "could not read Username" in message:

                raise ValueError(
                    "Private repository. Authentication required."
                )

            if "not authorized" in message.lower():

                raise ValueError(
                    "You are not authorized to access this repository."
                )

            raise ValueError(
                "Failed to clone repository."
            )

        return str(repo_path)

    @staticmethod
    def pull(repository_path: str):

        repo = Repo(repository_path)

        origin = repo.remotes.origin

        origin.pull()

        return repository_path