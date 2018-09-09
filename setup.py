from setuptools import setup, find_packages

setup(name='sempy',
      version='0.01',
      description='semux python light wallet',
      url='http://github.com/mdodong/sempy',
      author='mdodong',
      author_email='mdodong.6120@gmail.com',
      license='MIT',
      packages=['sempy', 'sempy\cli'],
      install_requires=[
          'semux',
          'requests',
          'click',
          'bcrypt',
          'pycryptodome'
      ],
      zip_safe=False)
