"""A wrapper for various shell based functions found in the os & shutil modules."""

import os
import shutil
import platform
import tarfile
import hashlib
import sys

__author__ = 'PencilShavings'
__version__ = '0.0.10'


def envar_parser(path):
    """Parses environment variables from strings."""

    if str(path).startswith('~/'):
        path = path.replace('~', '$HOME')

    if system() == 'Windows':
        if '$HOME' in path:
            path = path.replace('$HOME', str(os.getenv('HOMEDRIVE') + os.getenv('HOMEPATH')).replace('\\', '/'))
        if '$USER' in path:
            path = path.replace('$USER', os.getenv('USERNAME'))

    for y in os.environ:
        if '$' + y in path:
            path = path.replace('$' + y, os.environ[y])

    return path


def system():
    """Returns the base OS"""

    kernel = platform.system()
    if kernel == 'Linux':
        return 'Linux'
    elif kernel == 'Darwin':
        return 'Mac'
    elif kernel == 'Windows':
        return 'Windows'
    elif kernel.rpartition('-')[0] == 'CYGWIN_NT':
        return 'Cygwin'
    else:
        return 'UNKNOWN'


def get_cwd():
    """Changes directories"""

    # os.getenv('PWD') does not funtion the same as getcwd(). It doesnt seem to respect the cd's.
    return os.getcwd()


def get_hash(target, hashtype='sha1', parse=False):
    """Calculates the hash of a file. Simplifies usage of hashlib"""

    if parse:
        target = envar_parser(target)

    # Calls hashlib.[md5, sha1, sha224, sha256, sha384, sha512]
    method_to_call = getattr(hashlib, hashtype)
    h = method_to_call(target)
    return h.hexdigest()


def dir_exists(target, parse=False):
    """Checks if a directory exists"""

    if parse:
        target = envar_parser(target)
    if os.path.isdir(target):
        return True
    else:
        return False


def file_exists(target, parse=False):
    """Checks if a file exists"""

    if parse:
        target = envar_parser(target)
    if os.path.isfile(target):
        return True
    else:
        return False


def link_exist(target, parse=False):
    """Checks if a system link exists"""

    if parse:
        target = envar_parser(target)
    if os.path.islink(target):
        return True
    else:
        return False


def is_dir(target, parse=False):
    """Checks if the target is a directory. Calls dir_exists()"""

    if parse:
        target = envar_parser(target)
    return dir_exists(target)


def is_file(target, parse=False):
    """Checks if the target is a file. Calls file_exists()"""

    if parse:
        target = envar_parser(target)
    return file_exists(target)


def is_link(target, parse=False):
    """Checks if the target is a system link. Calls link_exists()"""

    if parse:
        target = envar_parser(target)
    return link_exist(target)


def does_this_exist(target, parse=False):
    """Checks if the target exists, whether it's a file or directory"""

    if parse:
        target = envar_parser(target)
    # Check if the target is a directory
    if is_dir(target):
        return True
    else:
        # Check if the target is a file
        if is_file(target):
            return True
        else:
            return False


def ln(src, dst, parse=False):
    """Creates a system link"""

    if parse:
        src = envar_parser(src)
        dst = envar_parser(dst)
    os.symlink(src, dst)


def mkdir(target, path=True, verbose=False, msg=None, parse=False):
    """Creates a directory"""

    if parse:
        target = envar_parser(target)
        if type(msg) == str and parse:
            msg = envar_parser(msg)

    if verbose:
        if not type(msg) == str:
            msg = 'Creating: ' + target
        echo(msg)

    if path:
        os.makedirs(target)
    else:
        os.mkdir(target)


def rm(target, verbose=False, msg=None, parse=False):
    """Deletes a file or directory, recursively)"""

    if parse:
        target = envar_parser(target)
        if type(msg) == str and parse:
            msg = envar_parser(msg)

    if verbose:
        if not type(msg) == str:
            msg = 'Removing: "' + target + '"'
        echo(msg)

    if is_dir(target):
        shutil.rmtree(target)

    if is_file(target):
        os.remove(target)


def mv(src, dst, verbose=False, msg=None, parse=False):
    """Moves a file or directory, recursively)"""

    if parse:
        src = envar_parser(src)
        dst = envar_parser(dst)
        if type(msg) == str and parse:
            msg = envar_parser(msg)

    if verbose:
        if not type(msg) == str:
            msg = 'Moving: "' + src + '" to: "' + dst + '"'
        echo(msg)

    shutil.move(src, dst)


def cp(src, dst, verbose=False, msg=None, parse=False):
    """Copies a file or directory, recursively)"""

    if parse:
        src = envar_parser(src)
        dst = envar_parser(dst)
        if type(msg) == str and parse:
            msg = envar_parser(msg)

    if verbose:
        if not type(msg) == str:
            msg = 'Copying: "' + src + '" to: "' + dst + '"'
        echo(msg)

    if is_dir(src):
        shutil.copytree(src, dst)

    if is_file(src):
        shutil.copy(src, dst)


def cd(dst, parse=False):
    """Changes the working directory)"""

    if parse:
        dst = envar_parser(dst)
    os.chdir(dst)


def ls(target, show_dirs=True, show_files=True, show_hidden=False, parse=False, recursive_ls=False):
    """Lists the contents of a directory"""

    if parse:
        target = envar_parser(target)

    # Fix path issue
    if not str(target).endswith('/'):
        target += '/'

    # Gets the contents of the specified path
    tmp_list = []
    target_listing = []
    # TODO: recursive_ls will show hidden directories & files!!
    if recursive_ls:
        for path, subdirs, files in os.walk(target):
            tmp_list.append(path)
            for name in files:
                element = os.path.join(path, name)
                element = element.replace('\\', '/')
                tmp_list.append(element)
        # Remove prefix
        for x in tmp_list:
            target_listing.append(x.replace(target, ''))

    else:
        target_listing = os.listdir(target)

    if '' in target_listing:
        target_listing.remove('')

    dirs = []
    files = []
    hdirs = []
    hfiles = []

    # The sorting mechanism
    for x in target_listing:
        if is_dir(target + x):
            if x.startswith('.'):
                hdirs.append(x)
            else:
                dirs.append(x)
        elif is_file(target + x):
            if x.startswith('.'):
                hfiles.append(x)
            else:
                files.append(x)

    listing = []
    if show_dirs and show_hidden:
        listing += hdirs
    if show_dirs:
        listing += dirs
    if show_files and show_hidden:
        listing += hfiles
    if show_files:
        listing += files

    listing.sort()

    return listing


def echo(msg, dst='', append=False, parse=False):
    """Print text to the console or save it to a file"""

    if parse:
        msg = envar_parser(msg)
        dst = envar_parser(dst)

    if dst == '':
        print(msg)
    else:

        if append:
            mode = 'a'
        else:
            mode = 'w'

        tmp = open(dst, mode)
        tmp.write(msg)
        tmp.close()


def cat(target, aslist=False, strip=True, isurl=False, parse=False, comment=""):
    """Reads the contents of a text file, whether it be a local or remote file"""

    # parse the file path
    if parse:
        target = envar_parser(target)

    # if tartget is url cat the url
    if isurl:
        if sys.version_info.major == 2:
            from urllib import urlopen
        else:
            from urllib.request import urlopen
        f = urlopen(target)
    # if target is a local file, open the file
    else:
        f = open(target, 'r')

    s = f.read()

    if sys.version_info.major == 3 and type(s) is bytes:
     	s = s.decode()

    # Remove comment lines
    if comment != "":
        newstring = ""
        for line in s.splitlines():
            if line.startswith(comment):
                pass
            else:
                newstring += "\n"
                newstring += line
            s = newstring

    # Convert to list, removing empty lines
    if aslist:
        s = s.splitlines()
        if strip:
            for x in s[:]:
                if x == '':
                    s.remove(x)
    # Strip the trailing newline
    else:
        if strip:
            s = s.rstrip('\n')

    # Close the original file
    f.close()

    # Return the end result
    return s


def targz(target, dst='', extract=False, into=False, verbose=False, parse=False):
    """Creates a tar.gz file of a directory"""

    if parse:
        target = envar_parser(target)
        dst = envar_parser(envar_parser(dst))

    cwd = get_cwd() + '/'

    target_fullpath = os.path.abspath(target)
    target_dir = str(target_fullpath.rpartition('/')[2])
    parent_path = str(target_fullpath.rpartition('/')[0]) + '/'

    if dst == '':
        dst = parent_path
    if not dst.endswith('/'):
        dst += '/'
    # TODO: envar_parser(dst)
    # TODO: Raise Errors
    # TODO: Loop through to find exact dir that does not exist
    if not does_this_exist(target):
        echo('"' + target_fullpath + '" does not exist!')
        exit()

    if not does_this_exist(dst):
        echo('"' + dst + '" does not exist!')
        exit()

    if not extract:
        # ARCHIVE
        cd(parent_path)
        if verbose:
            echo('Archiving: "' + target_fullpath + '" to "' + dst + target_dir + '.tar.gz"')
        tar = tarfile.open(dst + target_dir + '.tar.gz', 'w:gz')
        tar.add(target_dir)
        tar.close()
    else:
        # EXTRACT
        cd(dst)
        if verbose:
            echo('Extracting: "' + target_fullpath + '" to "' + dst + '"')
        tar = tarfile.open(target_fullpath)

        if not into:
            tar.extractall()
        else:
            for member in tar.getmembers():
                if not member.name == target_dir:  # example.tar.gz is somehow being read as example
                    member.name = './' + str(member.name).partition('/')[2]
                    tar.extract(member)
        tar.close()
    cd(cwd)

