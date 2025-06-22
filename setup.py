from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import os
import subprocess

class CMakeExtension(Extension):
    def __init__(self, name):
        super().__init__(name, sources=[])

class CMakeBuild(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)

    def build_cmake(self, ext):
        build_temp = os.path.abspath(self.build_temp)
        os.makedirs(build_temp, exist_ok=True)
        ext_dir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

        subprocess.check_call([
            "cmake",
            "-S", "cpp",
            "-B", build_temp,
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={ext_dir}",
            "-DCMAKE_BUILD_TYPE=Release",
        ])
        subprocess.check_call(["cmake", "--build", build_temp])

setup(
    name="vector_add",
    version="0.1.0",
    packages=["vector_add"],
    package_dir={"": "src"},
    ext_modules=[CMakeExtension("vector_add._vector_add")],  # creates vector_add/_vector_add.so
    cmdclass={"build_ext": CMakeBuild},
    zip_safe=False,
)
