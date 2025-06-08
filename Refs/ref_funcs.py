from http.client import CannotSendHeader
import os
from typing import Optional, Union

from GitRepo.git_repository import GitRepository



def ref_resolve(repo: 'GitRepository', ref: str) -> str:
    path = GitRepository.repo_file(repo, ref)

    if not os.path.isfile(path):
        return None
    
    with open(path, 'r') as file_pointer:
        data = file_pointer.read()[:-1]

    if data.startswith("ref: "):
        return ref_resolve(repo, data[5:])
    else:
        return data

def ref_list(repo: 'GitRepository', path: Optional[str] = None) -> dict[str, Union[str, ]]:
    if not path:
        path = GitRepository.repo_dir(repo, "refs")
    
    ret = dict()

    for entry in sorted(os.listdir(path)):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            ret[entry] = ref_list(repo, full_path)
        else:
            ret[entry] = ref_resolve(repo, full_path)
    
    return ret