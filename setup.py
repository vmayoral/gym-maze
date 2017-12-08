from setuptools import setup, find_packages

setup(name='gym_maze',
      version='0.0.1',
      packages=find_packages(),
      package_data={'gym_maze': ['gym_maze/envs/waco.txt']},
      include_package_data=True,
      install_requires=['gym']  # And any other dependencies foo needs
)
