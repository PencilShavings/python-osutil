from distutils.core import setup
import osutil

setup(
	name=osutil.__name__,
	version=osutil.__version__,
	py_modules=['osutil'],
	url='https://github.com/PencilShavings/python-osutil',
	license='MIT',
	author=osutil.__author__,
	author_email='eb.pencilshavings@gmail.com',
	description='A wapper for various shell based functions found in the os & shutil modules.',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Topic :: Software Development',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 2'
	]
)
