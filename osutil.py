import os
import shutil
import platform
import tarfile


def get_kernel():
	kernel_name = platform.system()
	kernel_version_full = platform.release()
	kernel_version = None

	if kernel_name == 'Linux':
		kernel_version = kernel_version_full.partition('-')[0]

	if kernel_name == 'Darwin':
		kernel_version = kernel_version_full

	if kernel_name == kernel_name.rpartition('-')[0]:
		kernel_name = 'Cygwin-NT'
		kernel_version = kernel_version_full.partition('(')[0]

	if kernel_name == 'Windows':
		kernel_name = 'Windows-NT'
		kernel_version_full = platform.win32_ver()[1]
		kernel_version = platform.win32_ver()[1].rpartition('.')[0]

	info = [kernel_name, kernel_version, kernel_version_full]

	return info

def get_os():
	kernel = get_kernel()[0]
	os_type = None
	os_version = None
	os_generic = None

	if kernel == 'Linux':
		os_type = platform.linux_distribution()[0]
		if os_type == 'CentOS Linux':
			os_type = 'CentOS'
		elif (os_type == 'debian') and (file_exists('/usr/bin/raspi-config')):
			os_type = 'Raspbian'

		os_version = platform.linux_distribution()[1][:3]
		os_generic = 'Linux'

	if kernel == 'Darwin':
		os_type = 'MacOS'
		os_version = platform.mac_ver()[0]
		os_generic = 'Mac'

	if kernel == 'Cygwin-NT':
		os_type = 'Cygwin'

		# 5.0 = W2000, 5.1 = XP, 6.0 = Vista

		if platform.system() == 'CYGWIN_NT-10.0':
			os_version = '10'
		elif platform.system() == 'CYGWIN_NT-6.1':
			os_version = '7'
		else:
			os_version = 'N/A'

		os_generic = os_type

	if kernel == 'Windows-NT':
		os_type = 'Windows'
		os_version = platform.release()
		os_generic = os_type

	info = [os_type, os_version, os_generic]

	return info

def get_arch():
	arch = platform.machine()

	if arch == 'x86_64' or arch == 'AMD64':
		arch1 = '64-bit'
		arch2 = 'x86_64'
		arch3 = 'amd64'
		# arch4 = 'x64'
	elif arch == 'armv7l':
		arch1 = 'arm'
		if arch == 'armv7l':
			arch2 = 'armv7'
		else:
			arch2 = arch
		arch3 = arch
	elif arch == 'i686':
		arch1 = '32-bit'
		arch2 = 'i686'
		arch3 = 'x86'
		# arch4 = 'i386'
	else:
		arch1 = arch
		arch2 = 'N/A'
		arch3 = 'N/A'

	info = [arch1, arch2, arch3]

	return info

def get_hostname():
	return platform.node()

def get_user():
	if get_kernel()[0] == 'Windows-NT':
		return os.getenv('USERNAME')
	else:
		return os.getenv('USER')

def get_homeDir():
	if get_kernel()[0] == 'Windows-NT':
		return os.getenv('HOMEDRIVE') + os.getenv('HOMEPATH')
	else:
		return os.getenv('HOME')

def get_cwd():
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


def ls(target, show='all'):
	dirs = os.walk(target).next()[1]
	files = os.walk(target).next()[2]

	dirs.sort()
	files.sort()

	if show == 'dirs':
		return dirs
	elif show == 'files':
		return files
	else:
		return dirs + files

def ls_files_by_extention(folder, extention):
	if folder == '':
		folder = get_cwd()

	result = []

	path = os.walk(folder).next()[2]

	for files in path:
		if files.endswith(extention):
			result.append(files)

	result.sort()

	return result

def targz(target, dst='', extract=False, verbose=False):

	cwd = get_cwd() + '/'

	# if TRUE will set dst to targets_parent_dir later
	if dst == '':
		use_parent = True
	else:
		use_parent = False

	# Add trailing / to all dirctorys, for the fun of it.
	if not target.endswith('/'):
		target += '/'

	if not dst.endswith('/'):
		dst += '/'

	# From the target, get the target dirctory name & it's parents path.
	target_dir = target[:-1].rpartition('/')[2]
	targets_parent_dir = target[:-1].rpartition('/')[0] + '/'

	if use_parent:
		dst = targets_parent_dir

	if not extract:
		cd(targets_parent_dir)
		print 'Archiving: "' + target + '" to "' + dst + target_dir + '.tar.gz"'
		tar = tarfile.open(dst + target_dir + '.tar.gz', 'w:gz')
		tar.add(target_dir)
	else:
		cd(dst)
		print 'Extracting: "' + targets_parent_dir + target_dir + '" to "' + dst + '"'
		tar = tarfile.open(targets_parent_dir + target_dir)
		tar.extractall()

	tar.close()
	cd(cwd)
