"""A wrapper for various shell based functions found in the os & shutil modules."""

__author__ = 'PencilShavings'
__version__ = '0.0.7'

import os
import shutil
import platform
import tarfile

def system():
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

def getenv_hostname():
	return os.getenv('HOSTNAME')

def getenv_user():
	if system() == 'Windows':
		return os.getenv('USERNAME')
	else:
		return os.getenv('USER')

def getenv_home():
	if system() == 'Windows':
		return str(os.getenv('HOMEDRIVE') + os.getenv('HOMEPATH')).replace('\\', '/')
	else:
		return os.getenv('HOME')


def get_cwd():
	# os.getenv('PWD') does not funtion the same as getcwd(). It doesnt seem to respect the cd's.
	return os.getcwd()

def get_pid():
	return str(os.getpid())


def dir_exists(target):
	if os.path.isdir(target):
		return True
	else:
		return False

def file_exists(target):
	if os.path.isfile(target):
		return True
	else:
		return False

def link_exist(target):
	if os.path.islink(target):
		return True
	else:
		return False

def pid_exists(pid):
	return dir_exists('/proc/' + pid)

def is_dir(target):
	return dir_exists(target)

def is_file(target):
	return file_exists(target)

def is_link(target):
	return link_exist(target)

def does_this_exist(target):
	# Check if the target is a directory
	if is_dir(target):
		return True
	else:
		# Check if the target is a file
		if is_file(target):
			return True
		else:
			return False


def ln(src, dst):
	os.symlink(src, dst)

def mkdir(target, path=True, verbose=False, msg=None):
	if verbose:
		if not type(msg) == str:
			msg = 'Creating: ' + target
		echo(msg)

	if path:
		os.makedirs(target)
	else:
		os.mkdir(target)

def rm(target, verbose=False, msg=None):
	if verbose:
		if not type(msg) == str:
			msg = 'Removing: "' + target + '"'
		echo(msg)

	if is_dir(target):
		shutil.rmtree(target)

	if is_file(target):
		os.remove(target)

def mv(src, dst, verbose=False, msg=None):
	if verbose:
		if not type(msg) == str:
			msg = 'Moving: "' + src + '" to: "' + dst + '"'
		echo(msg)

	shutil.move(src, dst)

def cp(src, dst, verbose=False, msg=None):
	if verbose:
		if not type(msg) == str:
			msg = 'Copying: "' + src + '" to: "' + dst + '"'
		echo(msg)

	if is_dir(src):
		shutil.copytree(src, dst)

	if is_file(src):
		shutil.copy(src, dst)

def cd(dst):
	os.chdir(dst)

def ls(target, show_dirs=True, show_files=True,  show_hidden=False, extention=''):
	# TODO: Find a way to filter file without extentions.
	dirs = os.walk(target).next()[1]
	files = os.walk(target).next()[2]

	dirs.sort()
	files.sort()

	if not show_hidden:
		for x in dirs[:]:
			if x.startswith('.'):
				dirs.remove(x)
		for y in files[:]:
			if y.startswith('.'):
				files.remove(y)

	if extention != '':
		show_dirs = False

	filtered_files = []
	if extention != '':
		for i in files:
			if i.endswith(extention):
				filtered_files.append(i)
		files = filtered_files

	listing = []
	if show_dirs:
		listing += dirs
	if show_files:
		listing += files
	return listing

def echo(msg, dst='', append=False):

	if append:
		mode = 'a'
	else:
		mode = 'w'

	if dst == '':
		print msg
	else:
		tmp = open(dst, mode)
		tmp.write(msg)
		tmp.close()

def cat(target, aslist=False, strip=True):
	f = open(target, 'r')

	if aslist:
		s = f.read().splitlines()
		if strip:
			for x in s[:]:
				if x == '':
					s.remove(x)
	else:
		s = f.read()
		if strip:
			s = s.rstrip('\n')
	f.close()

	return s

def targz(target, dst='', extract=False, into=False, verbose=False):

	cwd = get_cwd() + '/'

	target_fullpath = os.path.abspath(target)
	target_dir = target_fullpath.rpartition('/')[2]
	parent_path = str(target_fullpath.rpartition('/')[0]) + '/'

	if dst == '':
		dst = parent_path
	if not dst.endswith('/'):
		dst += '/'

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
				if not member.name == target_dir: # example.tar.gz is somehow being read as example
					member.name = './' + str(member.name).partition('/')[2]
					tar.extract(member)
		tar.close()
	cd(cwd)
