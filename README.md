# Docker

This folder holds Dockerfiles for our machine learning images. It has the following subfolders:

* `**base**` holds the base images that provide particular versions of Python, common libraries such as numpy, and GPU drivers. They are named as Python version + CPU/GPU, e.g. `tinymind/base:py27-cpu`.
  * Regular base images contain conda-installed Python. The `-pyenv` variant comes with pyenv-installed Python. Unless absolutely necessary, use the regular version. The pyenv version does not contain all dependencies (e.g. `pygpu`, `mkl`). In particular, all framework images are built using the conda base.
  * The reason to have a pyenv version is that conda doesn't play nicely with `setuptools`. [See more details here](https://github.com/ContinuumIO/anaconda-issues/issues/542).
* `**example**` holds example environments for testing purposes.
* `**frameworks**` holds images for specific frameworks.
  * Use the scripts like `tensorflow.py` to generate Dockerfiles. You need to be in the `frameworks` folder when running the scripts.
  * There are two types of framework images - "base" images are for running executions, and "notebook" images inherit from "base" ones and provide additional setup for notebooks.
  * Notebook images assume that the user running the image has `uid=1001, gid=1002`.

## Base Images

To build a new version, do the following:

```sh
cd docker/base
# py36cpu is the name of the image. Image name should be the same as the
# suffix of the Dockerfile.
docker build . -t py36cpu -f Dockerfile.py36cpu
# Tag the image with tinymind/NAME.
docker tag py36cpu tinymind/base:py36-cpu
# Push to Docker Hub (need to log in as tinymind).
docker push tinymind/base:py36-cpu
```

The `base` folder contains a `rebuild-all.sh` script that builds all base images.

## Frameworks

To build a new version, do the following:

```sh
cd docker/frameworks
# By default Dockerfiles for all versions of a framework are generated. You
# can use the flags to selectively generate Dockerfiles.
# --versions: list of framework versions (1.3).
# --langs: list of python versions (py27).
# --archs: list of cpu/gpu.
# --nobase: if specified, don't build "base" images.
# --nonb: if specified, don't build notebook images.
python keras.py --nonb --langs py27 py36

cd /tmp/tmbuild/
sh build.sh
```

## Pre install python package

```
RUN pip --no-cache-dir install --upgrade \
        Pillow \
        h5py \
        jupyter \
        keras_applications \
        keras_preprocessing \
        matplotlib \
        numpy \
        scipy \
        scikit-learn \
        pandas \
        mkl \
        pyyaml \
        Cython \
        opencv-python \
        tinyenv
```