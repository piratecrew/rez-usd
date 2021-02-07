#!/usr/bin/env python
from __future__ import print_function
import os
import argparse
from functools import partial
from os.path import relpath
import subprocess
import re


def which(command):
    """Get the path to a command

    Args:
        command (str): command to look for.

    Returns (str): path to command or None if not exists
    """
    try:
        path = subprocess.check_output(["which", command])
        path = path.strip()
        return path.decode()
    except subprocess.CalledProcessError as e:
        return None


def visit_files_recurse(top, filter=lambda x: True, visitor=print):
    """visit files recusively and call a visitor on files based on a filter.

    Args:
        root (str): Root directory to start the walk at.
        filter (callable): A filter callable to filter the files.
        visitor (callable): Visitor to call on each file.
    """
    for (root, _, files) in os.walk(top):
        for file in files:
            path = os.path.join(root, file)
            if filter(path):
                visitor(path)


def parse_ldd_output(output):
    """Parse the output from the command `ldd`.

    Args:
        output (str): The full output of `ldd`as a str.

    Returns:
        set: A set of library paths.
    """
    libraries = set()
    for line in output.splitlines():
        line = line.decode()
        match = re.match(r"\s(.*) => (.*) \(0x", line)
        if match:
            libraries.add(match.group(2))
    return libraries


def get_dependencies(sofile):
    """Get all linked dependencies of a .so file.

    Args:
        sofile (str): Path to a .so file.

    Returns:
        set: A set of library paths.
    """
    try:
        output = subprocess.check_output(["ldd", sofile])
        return parse_ldd_output(output)
    except Exception as e:
        print("Ignore:", e, type(e))


def filter_so(path, verbose=False):
    """Simple filter to check if a path is a .so file.

    Args:
        path (str): Path to check if it is an .so file.
        verbose (bool): Print files that are not executable

    Returns:
        bool: True if file is a .so file else False.
    """
    if not re.match(r".*\.so[\.\d]*$", path):
        return False
    if not os.access(path, os.X_OK):
        if verbose:
            print("{} is not executable, skipping".format(path))
        return False
    return True


def get_relative_rpath(root, path, libs):
    """Calculate the set of relative rpaths from a file to its libraries.

    Args:
        root (str): root directory to calculate the relative paths within.
        path (str): path to the library file.
        libs (list | iterable): list of dependent libraries.

    Returns:
        set: A set of rpaths in the form `$ORIGIN/../..`
    """

    relpaths = set()
    for lib_path in libs:
        if lib_path.startswith(root):
            relpath = os.path.join(
                "$ORIGIN",
                os.path.dirname(os.path.relpath(lib_path, os.path.dirname(path))),
            )
            relpaths.add(relpath)
    return relpaths


def set_rpath(path, rpaths, patchelf):
    """Set rpath of a library.

    Args:
        path (str): path to dynamic library file.
        rpaths (list | iterable): a list of rpaths.
        patchelf (str): provide a path to the patchelf command
    """

    rpath = ":".join(rpaths)
    subprocess.check_call([patchelf, "--set-rpath", rpath, path])


def handle_so(root, path, patchelf):
    """Visitor to handle .so files"""
    root = os.path.realpath(root)  # calculate symlinks
    path = os.path.realpath(path)  # calculate symlinks
    libs = get_dependencies(path)
    if libs is None:
        return

    relpaths = get_relative_rpath(root, path, libs)
    print("set rpath for: {}".format(path))
    set_rpath(path, relpaths, patchelf)


def main(arguments):
    root = arguments.root
    visit_files_recurse(
        root,
        filter=filter_so,
        visitor=partial(handle_so, root, patchelf=arguments.patchelf),
    )
    return 0


def command(command):
    """Make sure a command is available"""
    path = which(command)
    if path is None:
        raise argparse.ArgumentTypeError(
            "{}: command not found, try provide an absolute path".format(command)
        )
    return path


def parse_args():
    parser = argparse.ArgumentParser("Localize rpaths")
    parser.add_argument(
        "root", type=str, help="all rpaths within this root will be localized"
    )
    parser.add_argument(
        "--patchelf", type=command, default="patchelf", help="Path to patchelf command"
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    exit(main(args))
