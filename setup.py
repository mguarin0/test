from setuptools import setup
from setuptools import Extension
from setuptools.command.build_ext import build_ext
import pybind11
import os
import sys
import subprocess

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir="."):
        super().__init__(name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

class CMakeBuild(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)
    
    def build_cmake(self, ext):
        build_dir = os.path.abspath(self.build_temp)
        os.makedirs(build_dir, exist_ok=True)

        cfg = "Debug" if self.debug else "Release"
        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={os.path.abspath(self.get_ext_fullpath(ext.name))}",
            f"-DCMAKE_BUILD_TYPE={cfg}",
        ]

        build_args = ["--config", cfg]
        subprocess.check_call(["cmake", ext.sourcedir] + cmake_args, cwd=build_dir)
        subprocess.check_call(["cmake", "--build", "."] + build_args, cwd=build_dir)

setup(
    name="vector_add",
    version="0.1.0",
    ext_modules=[CMakeExtension("vector_add")],
    cmdclass={"build_ext": CMakeBuild},
    zip_safe=False,
)
