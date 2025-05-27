import configparser
import os
from typing import Optional

class GitRepository:
    """To represent a git repository"""
    def __init__(self, path: str, force: bool = False):
        self.worktree: str = path
        self.gitdir: str = os.path.join(path, ".git")
        self.config: configparser.ConfigParser = configparser.ConfigParser()

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception(f"Not a Git Repository {path}")

        if not force:
            config_file: Optional[str] = self.repo_file("config")

            if config_file and os.path.exists(config_file):
                self.config.read([config_file])
            else:
                raise Exception("Configuration file missing")

            vers: int = int(self.config.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception(f"Unsupported repositoryformatversion: {vers}")


    def repo_path(self, *path: str) -> str:
        """Compute path under the repo's gitdir"""
        return os.path.join(self.gitdir, *path)


    def repo_dir(self, *path: str, mkdir: bool = False) -> Optional[str]:
        """Same as repo_path, but mkdir *path if absent if mkdir"""

        path = self.repo_path(*path)  # Use self, NOT repo parameter

        if os.path.exists(path):
            if os.path.isdir(path):
                return path
            else:
                raise Exception(f"Not a directory {path}")

        if mkdir:
            os.makedirs(path)
            return path
        else:
            return None


    def repo_file(self, *path: str, mkdir: bool = False) -> str:
        """Same as repo_path, but create dirname(*path) if absent."""

        if self.repo_dir(*path[:-1], mkdir=mkdir):
            return self.repo_path(*path)
        else:
            raise Exception(f"Could not create or find directory {'/'.join(path[:-1])}")


    @staticmethod
    def repo_create(path: str) -> 'GitRepository':
        repo = GitRepository(path, True)

        if os.path.exists(repo.worktree):
            if not os.path.isdir(repo.worktree):
                raise Exception(f"{path} is not a directory!")
            if os.path.exists(repo.gitdir) and os.listdir(repo.gitdir):
                raise Exception(f"{path} is not empty!")
        else:
            os.makedirs(repo.worktree)

        # Ensure .git directory exists
        if not os.path.exists(repo.gitdir):
            os.makedirs(repo.gitdir)

        assert repo.repo_dir("branches", mkdir=True)
        assert repo.repo_dir("objects", mkdir=True)
        assert repo.repo_dir("refs", "tags", mkdir=True)
        assert repo.repo_dir("refs", "heads", mkdir=True)

        with open(repo.repo_file("description"), "w") as f:
            f.write("Unnamed repository; edit this file 'description' to name the repository.\n")

        with open(repo.repo_file("HEAD"), "w") as f:
            f.write("ref: refs/heads/master\n")

        with open(repo.repo_file("config"), "w") as f:
            config = repo.repo_default_config()
            config.write(f)

        return repo

    def repo_default_config(self) -> 'configparser.ConfigParser':
        ret: configparser.ConfigParser = configparser.ConfigParser()

        ret.add_section("core")
        ret.set("core", "repositoryformatversion", "0")
        ret.set("core", "filemode", "false")
        ret.set("core", "bare", "false")
        
        return ret

    def repo_find(self, path: str = '.', required: bool = True) -> Optional[str]:
        pass
