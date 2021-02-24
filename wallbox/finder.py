"""
Implements file finder function
"""

import os
from typing import Optional

DEFAULT_MAX_SIZE:int = 14 * (2 ** 20)


def file_finder(path: str, max_size=DEFAULT_MAX_SIZE) -> Optional[str]:
    """
    A function that given a path of the file system finds
    the first file that meets the following requirements
    a. The file owner is admin
    b. The file is executable
    c. The file has a size lower than 14*2^20 bytes

    :param path: Valid folder path
    :param max_size: File max size
    :return: Absolute path of the first file
    """

    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file_basename in files:
                file_abspath = os.path.join(root, file_basename)
                if (
                    _has_admin_owner(file_abspath)
                    and _is_executable(file_abspath)
                    and _has_size_lower(file_abspath, max_size)
                ):
                    return file_abspath
    return None


def _has_admin_owner(file_abspath: str) -> bool:
    """
    Check if a file owner is admin

    :param file_abspath: Absolute path
    :return: True or False
    """
    return os.stat(file_abspath).st_uid == 0


def _is_executable(file_abspath: str) -> bool:
    """
    Check if a file is executable

    :param file_abspath: Absolute path
    :return: True or False
    """
    return os.access(file_abspath, os.X_OK)


def _has_size_lower(file_abspath: str, max_size: int) -> bool:
    """
    Check if a file has a lower size than the specified in max_size

    :param file_abspath: Absolute path
    :param max_size: Size to compare
    :return: True or False
    """
    return os.stat(file_abspath).st_size <= max_size
