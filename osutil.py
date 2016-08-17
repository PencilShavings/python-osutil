import os
import shutil
import platform
import tarfile

__author__ = 'PencilShavings'
__version__ = '0.0.4'

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
		return os.getenv('HOMEDRIVE') + os.getenv('HOMEPATH')
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

def mkdir(target, path=True, verbose=False):
	if verbose:
		print 'Creating: ' + target

	if path:
		os.makedirs(target)
	else:
		os.mkdir(target)

def rm(target, verbose=False):
	if verbose:
		print 'Removing: "' + target + '"'

	if is_dir(target):
		shutil.rmtree(target)

	if is_file(target):
		os.remove(target)

def mv(src, dst, verbose=False):
	if verbose:
		print 'Moving: "' + src + '" to: "' + dst + '"'

	shutil.move(src, dst)

def cp(src, dst, verbose=False):
	if verbose:
		print 'Copying: "' + src + '" to: "' + dst + '"'

	if is_dir(src):
		shutil.copytree(src, dst)

	if is_file(src):
		shutil.copy(src, dst)

def cd(dst):
	os.chdir(dst)

def ls(target, show='', extention=''):
	dirs = os.walk(target).next()[1]
	files = os.walk(target).next()[2]

	dirs.sort()
	files.sort()

	filtered_files = []
	if extention != '':
		for i in files:
			if i.endswith(extention):
				filtered_files.append(i)
		files = filtered_files

	if show == 'dirs':
		return dirs
	elif show == 'files' or extention != '':
		return files
	else:
		return dirs + files


def targz(target, dst='', extract=False, into=False, verbose=False):

	cwd = get_cwd() + '/'

	# if TRUE will set dst to targets_parent_dir later
	if dst == '':
		use_parent = True
	else:
		use_parent = False

	# Add trailing / to all dirctorys, for the fun of it.
	# WARNING: This includes EXTRACTING files! (example.tar.gz/)
	if not target.endswith('/'):
		target += '/'

	if not dst.endswith('/'):
		dst += '/'

	# From the target, get the target dirctory name & it's parents path.
	if extract:
		target_file = target[:-1].rpartition('/')[2] # Removes the path & trailing "/" when EXTRACTING (PATH/example.tar.gz/ > example.tar.gz)
		target_dir = target_file.rpartition('.')[0].rpartition('.')[0] # Removes anything after the first "." (example.tar.gz > example.tar > example)
		targets_parent_dir = target[:-1].rpartition('/')[0] + '/' # (PATH/example.tar.gz/ > PATH/example.tar.gz > PATH > PATH/)
	else:
		target_dir = target[:-1].rpartition('/')[2]
		targets_parent_dir = target[:-1].rpartition('/')[0] + '/'

	if use_parent:
		dst = targets_parent_dir

	cd(dst)

	if not extract:
		# ARCHIVEING
		if verbose:
			print 'Archiving: "' + target + '" to "' + dst + target_dir + '.tar.gz"'
		tar = tarfile.open(dst + target_dir + '.tar.gz', 'w:gz')
		tar.add(target_dir)
	else:
		# EXTRACTING
		tar = tarfile.open(target[:-1])
		if not into:
			if verbose:
				print 'Extracting: "' + target[:-1] + '" to "' + dst + '"'
			tar.extractall()
		else:
			if verbose:
				print 'Extracting: "' + target[:-1] + '" into "' + dst + '"'
			for member in tar.getmembers():
				if not member.name == target_dir:
					member.name = './' + str(member.name).partition('/')[2]
					tar.extract(member)
	tar.close()
	cd(cwd)
