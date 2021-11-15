#!/usr/bin/env python

import os
import glob
from setuptools import find_packages, setup

import torch
from torch.utils.cpp_extension import CUDA_HOME, CppExtension, CUDAExtension

ROOT = os.path.abspath(os.path.dirname(__file__))

def get_extensions():
    global ROOT
    path_ext = os.path.join(ROOT, 'torch_toys', 'csrc')
    path_main_cpp = os.path.join(path_ext, 'ext.cpp')
    lst_path_cpp = glob.glob(os.path.join(path_ext, '**', '*.cpp'))
    lst_path_cu = glob.glob(os.path.join(path_ext, '**', '*.cu'))

    sources = [path_main_cpp] + lst_path_cpp + lst_path_cu

    cuda_enabled = len(lst_path_cu) > 0
    extension = CppExtension if not cuda_enabled else CUDAExtension

    extra_compile_args = {"cxx": [
        '-O3',
        '-fopenmp',
    ]}
    define_macros = []

    if cuda_enabled:
        assert torch.cuda.is_available()
        assert CUDA_HOME is not None

        extra_compile_args["nvcc"] = [
            "-O3",
            "-DCUDA_HAS_FP16=1",
            "-D__CUDA_NO_HALF_OPERATORS__",
            "-D__CUDA_NO_HALF_CONVERSIONS__",
            "-D__CUDA_NO_HALF2_OPERATORS__",
        ]

    ext_modules = [
        extension(
            "torch_toys._C",
            sources,
            include_dirs=[path_ext],
            define_macros=define_macros,
            extra_compile_args=extra_compile_args,
        )
    ]

    return ext_modules


setup(
    name="torch_toys",
    url="https://github.com/twjang/torch_toys",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "torch>=1.7"
        "tqdm",
    ],
    ext_modules=get_extensions(),
    cmdclass={"build_ext": torch.utils.cpp_extension.BuildExtension},
)
