import setuptools
import osutil

setuptools.setup(
	name=osutil.__name__,
	version=osutil.__version__,
	py_modules=['osutil'],
	url='https://github.com/PencilShavings/python-osutil',
	license='MIT',
	author=osutil.__author__,
	author_email='eb.pencilshavings@protonmail.com',
	description=osutil.__doc__,
	long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Bug Tracker": "https://github.com/PencilShavings/python-osutil/issues",
    },
	classifiers=[
		'Development Status :: 3 - Alpha',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3'
	]
)
