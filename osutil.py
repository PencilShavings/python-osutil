# osutil v0.3

# Tested on the following,
# All Arch are 64-bit unless otherwise noted,
# Python & Cygwin Arch are the same as OS:

# CentOS 7.2
# CentOS 6.7 (32-bit)
# Raspbian 8 (ARM)
# MacOS 10.10
# Cygwin/Windows 7, 10
# Winodws 7

import tarfile
import os
import shutil
import platform

verbose = True

def get_kernel():
	kernel_name = platform.system()
	kernel_version_full = platform.release()
	kernel_version = None

	if kernel_name == 'Linux':
		kernel_version = kernel_version_full.partition('-')[0]

	if kernel_name == 'Darwin':
		kernel_version = kernel_version_full

	if kernel_name == 'CYGWIN_NT-10.0' or kernel_name == 'CYGWIN_NT-6.1':
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

	if kernel == 'Linux':
		os_type = platform.linux_distribution()[0]
		if os_type == 'CentOS Linux':
			os_type = 'CentOS'
		elif (os_type == 'debian') and (file_exists('/usr/bin/raspi-config')):
			os_type = 'Raspbian'

		os_version = platform.linux_distribution()[1]

	if kernel == 'Darwin':
		os_type = 'MacOS'
		os_version = platform.mac_ver()[0]

	if kernel == 'Cygwin-NT':
		os_type = 'Windows'

		# 5.0 = W2000, 5.1 = XP 6.0 = Vista

		if platform.system() == 'CYGWIN_NT-10.0':
			os_version = '10'
		elif platform.system() == 'CYGWIN_NT-6.1':
			os_version = '7'
		else:
			os_version = 'N/A'

	if kernel == 'Windows-NT':
		os_type = 'Windows'
		os_version = platform.release()

	info = [os_type, os_version]

	return info

def get_os_generic():
	kernel = get_kernel()[0]

	if kernel == 'Linux':
		return 'Linux'
	elif kernel == 'Darwin':
		return 'MacOS'
	elif kernel == 'Cygwin-NT':
		return 'Cygwin'
	elif kernel == 'Windows-NT':
		return 'Windows'
	else:
		return 'N/A'

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

def mkdir(target):
	if verbose:
		print 'Creating: ' + target

	#os.mkdir(target)
	os.makedirs(target)

def rm(target):
	if verbose:
		print 'Removing: "' + target + '"'

	if is_dir(target):
		shutil.rmtree(target)

	if is_file(target):
		os.remove(target)

def mv(src, dst):
	if verbose:
		print 'Moving: "' + src + '" to: "' + dst + '"'

	shutil.move(src, dst)

def cp(src, dst):
	if verbose:
		print 'Copying: "' + src + '" to: "' + dst + '"'

	if is_dir(src):
		shutil.copytree(src, dst)

	if is_file(src):
		shutil.copy(src, dst)

def cd(dst):
	os.chdir(dst)


def ls(target):
	dirs = ls_dirs(target)
	files = ls_files(target)

	return dirs + files

def ls_dirs(target):
	if target == '':
		target = get_cwd()

	dirs = os.walk(target).next()[1]
	dirs.sort()

	return dirs

def ls_files(target):
	if target == '':
		target = get_cwd()

	files = os.walk(target).next()[2]
	files.sort()

	return files

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

def targz(target):

	cwd = get_cwd()

	if target.endswith('/'):
		name = target[:-1].rpartition('/')[2]
		parent = target[:-1].rpartition('/')[0] + '/'
	else:
		name = target.rpartition('/')[2]
		parent = target.rpartition('/')[0] + '/'

	if parent == '/':
		parent = get_cwd() + '/'

	cd(parent)

	if verbose:
		print 'Archiving: "' + target + '" as: "' + name + '.tar.gz"'

	tar = tarfile.open(name + '.tar.gz', 'w:gz')

	tar.add(name)
	tar.close()

	cd(cwd)

def targz_v2(src, dst, name):

	# Check if the dst exists (always a dir)
	if dst == '':
		dst = get_cwd()

	# Check if a name is specifiyed, otherwise get it from the end of the src
	if name == '':
		if src.endswith('/'):
			name = src[:-1].rpartition('/')[2]
		else:
			name = src.rpartition('/')[2]

	# Check if dst has / in string
	if dst.endswith('/'):
		dst = dst + name
	else:
		dst = dst + '/' + name

	# OVER WRITES PREVIOUS FILE. UN-COMMENT TO NOT OVER WRITE EXISTING FILE
	# Check if the dst dir/file exits (can be a dir or file)
	# if does_this_exist(dst):
	# 	__msg_dst_already_exits(dst)

	if verbose:
		print 'Archiving: "' + src + '" to: "' + dst + '.tar.gz"'

	tar = tarfile.open(dst + '.tar.gz', 'w:gz')

	tar.add(src)
	tar.close()

def untar(src, dst):

	cwd = get_cwd()

	if dst == '':
		dst = cwd

	cd(dst)
	tar = tarfile.open(src)
	tar.extractall()
	tar.close()
	cd(cwd)


