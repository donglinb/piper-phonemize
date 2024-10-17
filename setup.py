import os
import shutil
import platform
from pathlib import Path

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

_DIR = Path(__file__).parent
_ESPEAK_DIR = _DIR / "espeak-ng"
_ONNXRUNTIME_DIR = _DIR / "onnxruntime"

__version__ = "1.2.0"

ext_modules = [
    Pybind11Extension(
        "piper_phonemize.lib.piper_phonemize_cpp",
        [
            "src/python.cpp",
            "src/phonemize.cpp",
            "src/phoneme_ids.cpp",
            "src/tashkeel.cpp",
        ],
        define_macros=[("VERSION_INFO", __version__)],
        include_dirs=[str(_ESPEAK_DIR / "include"), str(_ONNXRUNTIME_DIR / "include")],
        library_dirs=[str(_ESPEAK_DIR / "lib"), str(_ONNXRUNTIME_DIR / "lib")],
        libraries=["espeak-ng", "onnxruntime"],
        runtime_library_dirs=['$ORIGIN']
    ),
]

package_base_dir = _DIR / 'python' / 'piper_phonemize'
if os.path.exists(package_base_dir):
    shutil.rmtree(package_base_dir)
os.makedirs(package_base_dir, exist_ok=True)

shutil.copyfile(_DIR / 'piper_phonemize' / '__init__.py', package_base_dir / '__init__.py')
shutil.copyfile(_ESPEAK_DIR / 'share' / 'libtashkeel_model.ort', package_base_dir / 'libtashkeel_model.ort')
shutil.copytree(_ESPEAK_DIR / 'share' / 'espeak-ng-data', package_base_dir / 'espeak-ng-data', True, dirs_exist_ok=True)

package_lib_dir = package_base_dir / 'lib'
shutil.copytree(_ESPEAK_DIR / 'lib', package_lib_dir, True, lambda x, y: ['pkgconfig'], dirs_exist_ok=True)
shutil.copytree(_ONNXRUNTIME_DIR / 'lib', package_lib_dir, True, dirs_exist_ok=True)

setup(
    name="piper_phonemize",
    version=__version__,
    author="Michael Hansen",
    author_email="mike@rhasspy.org",
    url="https://github.com/rhasspy/piper-phonemize",
    description="Phonemization libary used by Piper text to speech system",
    long_description="",
    packages=["piper_phonemize"],
    package_dir={
        "piper_phonemize": "python/piper_phonemize",
    },
    package_data={
        "piper_phonemize": [str(p) for p in package_base_dir.parent.rglob('*')],
    },
    include_package_data=False,
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.7",
)
