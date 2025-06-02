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
            
    def __str__(self):
        return f"<GitRepository path={self.worktree}>"

    def repo_path(self, *path: str) -> str:
        """Compute path under the repo's gitdir"""
        return os.path.join(self.gitdir, *path)

    def repo_dir(self, *path: str, mkdir: bool = False) -> Optional[str]:
        """Same as repo_path, but mkdir *path if absent if mkdir"""

        path = self.repo_path(*path) 

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
        """Creates a new repository at path."""
        repo = GitRepository(path, True)

        if os.path.exists(repo.worktree):
            if not os.path.isdir(repo.worktree):
                raise Exception(f"{path} is not a directory!")
            if os.path.exists(repo.gitdir) and os.listdir(repo.gitdir):
                raise Exception(f"{path} is not empty!")
        else:
            os.makedirs(repo.worktree)

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
        """Sets the configuration settings"""
        config: configparser.ConfigParser = configparser.ConfigParser()

        config.add_section("core")
        config.set("core", "repositoryformatversion", "0")
        config.set("core", "filemode", "false")
        config.set("core", "bare", "false")
        
        return config

    @classmethod
    def repo_find(cls, path: str = '.', required: bool = True) -> Optional[str]:
        """Recursively searches the Git root from the directory"""
        path = os.path.realpath(path)

        if os.path.isdir(os.path.join(path, ".git")):
            return cls(path)
        
        parent = os.path.realpath(os.path.join(path, ".."))
        
        if parent == path:
            if required:
                raise Exception("No git directory.")
            else:
                return None
            
        return cls.repo_find(parent, required)
