from urllib.parse import urlparse


def get_repository_name(url: str):

    path = urlparse(url).path

    return path.strip("/").split("/")[-1].replace(".git", "")