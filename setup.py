import os
import sys
import numpy
import os.path
import pathlib
import sysconfig

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as BuildExt

numpy_include_dir = os.path.split(numpy.__file__)[0] + '/core/include'
CLIB_DIR = os.path.join(sysconfig.get_path('purelib'), 'backpropcore')
print("CLIB_DIR: ", CLIB_DIR)
LIBRARY_DIRS = [CLIB_DIR]


class CMakeExtension(Extension, object):
    extension_type = 'cmake'

    def __init__(self, name):
        super(CMakeExtension, self).__init__(name, sources=[])

class BuildExtension(BuildExt):

    def run(self):
        for ext in self.extensions:
            if hasattr(ext, 'extension_type') and ext.extension_type == 'cmake':
                self.cmake(ext)
        self.cythonize()
        super(BuildExtension, self).run()

    def cythonize(self):
        ext_files = ['backpropcore/model/_model.pyx']
        for path in ext_files:
            from Cython.Build import cythonize
            cythonize(path)

    def cmake(self, ext):
        cwd = pathlib.Path().absolute()
        build_temp = pathlib.Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        build_type = "Debug" if self.debug else "Release"

        cmake_args = [
            "-DCMAKE_BUILD_TYPE=" + build_type,
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + CLIB_DIR,
        ]

        os.chdir(str(build_temp))
        self.spawn(["cmake", str(cwd)] + cmake_args)
        if not self._dry_run:
            self.spawn(["cmake", "--build", "."])
        os.chdir(str(cwd))

extensions = [
    CMakeExtension(name="cbackpropcore"),
    Extension(name="backpropcore.model._model",
              sources=["backpropcore/model/_model.cpp"],
              include_dirs=["./include", numpy_include_dir],
              libarary_dirs=LIBRARY_DIRS,
              runtime_library_dirs=LIBRARY_DIRS,
              libraries=["gomp", "cbackpropcore"],
              extra_compile_args=["-fopenmp", "-std=c++14", "-ggdb", "-O3"]),
]

def _setup():
    cmdclass = {
        'build_ext': BuildExtension,
    }
    metadata = dict(
        name="backpropcore",
        version="0.1",
        packages=["backpropcore/model", "backpropcore/"],
        include_package_data=False,
        ext_modules=extensions,
        cmdclass=cmdclass,
    )
    setup(**metadata)

if __name__ == "__main__":
    _setup()
