import argparse
from shutil import copyfile

from shared import safe_mkdir


VERSIONS = ['0.8']
LANGS = ['py27', 'py36']
ARCHS = ['cpu', 'gpu']

CPU_TEMPLATE = """FROM tinymind/base:{version}
LABEL author="TinyMind" website="www.tinymind.com" email="hello@tinymind.com"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        cmake \
        libgoogle-glog-dev \
        libprotobuf-dev \
        python-pip \
        protobuf-compiler \
        && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir future hypothesis numpy protobuf six

RUN git clone --branch v0.8.1 --recursive https://github.com/caffe2/caffe2.git
RUN cd caffe2 && mkdir build && cd build \
    && cmake .. \
    -DUSE_CUDA=OFF \
    -DUSE_NNPACK=OFF \
    -DUSE_ROCKSDB=OFF \
    && make -j"$(nproc)" install \
    && ldconfig \
    && make clean \
    && cd .. \
    && rm -rf build

ENV PYTHONPATH /usr/local
"""

GPU_TEMPLATE = """FROM tinymind/base:{version}
LABEL author="TinyMind" website="www.tinymind.com" email="hello@tinymind.com"


"""

BUILD_COMMAND = """docker build . -t caffe2{i} -f Dockerfile.caffe2{i}
docker tag caffe2{i} tinymind/caffe2:{i}
docker push tinymind/caffe2:{i}
"""


def create_files(vs=VERSIONS, langs=LANGS, archs=ARCHS):
    safe_mkdir('/tmp/tmbuild')
    copyfile('fix-permissions.sh', '/tmp/tmbuild/fix-permissions.sh')
    commands = []
    for v in vs:
        for l in langs:
            for a in archs:
                commands.append(BUILD_COMMAND.format(i=create_file(v, l, a)))
    with open('/tmp/tmbuild/build.sh', 'w+') as f:
        for command in commands:
            f.write(command + '\n')


def create_file(v, l, a, base, nb):
    ver = '{}-{}-{}'.format(v, l, a)
    with open('/tmp/tmbuild/Dockerfile.caffe2{}'.format(ver), 'w+') as f:
        TPL = GPU_TEMPLATE if a == 'gpu' else CPU_TEMPLATE
        f.write(TPL.format(version='{}-{}'.format(l, a)))
    return ver


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--versions', nargs='+', type=str)
    parser.add_argument('--langs', nargs='+', type=str)
    parser.add_argument('--archs', nargs='+', type=str)
    FLAGS, unparsed = parser.parse_known_args()
    create_files(
        vs=FLAGS.versions or VERSIONS,
        langs=FLAGS.langs or LANGS,
        archs=FLAGS.archs or ARCHS,
    )
