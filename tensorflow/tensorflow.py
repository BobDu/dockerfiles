import os
import argparse
from shutil import copyfile


VERSIONS = ['1.4', '1.5', '1.6', '1.7', '1.8', '1.9', '1.10', '1.11', '1.12', '1.13', '1.14']
LANGS = ['py36']
ARCHS = ['cpu', 'gpu']

BASE = 'https://github.com/mind/wheels/releases/download/'
TAIL = '-linux_x86_64.whl'

WHEELS = {
    '1.4-py36-cpu': 'tf1.4.1-cpu/tensorflow-1.4.1-cp36-cp36m',
    '1.4-py36-gpu': 'tf1.4.1-gpu-cuda91/tensorflow-1.4.1-cp36-cp36m',

    '1.5-py36-cpu': 'tf1.5-cpu/tensorflow-1.5.0-cp36-cp36m',
    '1.5-py36-gpu': 'tf1.5-gpu-cuda91-nomkl/tensorflow-1.5.1-cp36-cp36m',

    '1.6-py36-cpu': 'tf1.6-cpu/tensorflow-1.6.0-cp36-cp36m',
    '1.6-py36-gpu': 'tf1.6-gpu-cuda91-nomkl/tensorflow-1.6.1-cp36-cp36m',

    '1.7-py36-cpu': 'tf1.7-cpu/tensorflow-1.7.0-cp36-cp36m',
    '1.7-py36-gpu': 'tf1.7-gpu-cuda91-nomkl/tensorflow-1.7.0-cp36-cp36m',

    '1.8-py36-cpu': 'tf1.8-cpu/tensorflow-1.8.0-cp36-cp36m',
    '1.8-py36-gpu': 'tf1.8-gpu-cuda91-nomkl/tensorflow-1.8.0-cp36-cp36m',

    '1.9-py36-cpu': 'tf1.9-cpu/tensorflow-1.9.0-cp36-cp36m',
    '1.9-py36-gpu': 'tf1.9-GPU-nomkl/tensorflow-1.9.0-cp36-cp36m',

    '1.10-py36-cpu': 'tf1.10-cpu/tensorflow-1.10.1-cp36-cp36m',
    '1.10-py36-gpu': 'tf1.10-gpu-cuda10-tensorrt/tensorflow-1.10.1-cp36-cp36m',

    '1.11-py36-cpu': 'tf1.11-cpu-mkl/tensorflow-1.11.0-cp36-cp36m',
    '1.11-py36-gpu': 'tf1.11-gpu-cuda10-tensorrt/tensorflow-1.11.0-cp36-cp36m',

    '1.12-py36-cpu': 'tf1.12-cpu-mkl/tensorflow-1.12.0-cp36-cp36m',
    '1.12-py36-gpu': 'tf1.12-gpu-cuda10-tensorrt/tensorflow-1.12.0-cp36-cp36m',

    '1.13-py36-cpu': 'tf1.13-cpu-mkl/tensorflow-1.13.1-cp36-cp36m',
    '1.13-py36-gpu': 'tf1.13-gpu-cuda10-tensorrt/tensorflow-1.13.1-cp36-cp36m',

    '1.14-py36-cpu': 'tf1.14-cpu-mkl/tensorflow-1.14.0-cp36-cp36m',

}

TEMPLATE = """FROM tinymind/base:{version}
LABEL author="TinyMind" website="www.tinymind.com" email="hello@tinymind.com"

RUN pip --no-cache-dir install {wheel}

# TensorBoard
EXPOSE 6006
"""

base_path = os.path.dirname(__file__)

def create_files(vs=VERSIONS, langs=LANGS, archs=ARCHS):
    for v in vs:
        for l in langs:
            for a in archs:
                create_file(v, l, a)


def create_file(v, l, a):
    ver = '{}-{}-{}'.format(v, l, a)
    path = os.path.join(base_path, 'Dockerfile.{}'.format(ver))
    with open(path, 'w+') as f:
        version = '{}-{}'.format(l, a)
        if a == 'gpu':
            if v in ('1.10', '1.11', '1.12', '1.13'):
                version += '-cuda10'
            else:
                version += '-cuda91'
        f.write(TEMPLATE.format(
            version=version,
            wheel=BASE + WHEELS['{}-{}-{}'.format(v, l, a)] + TAIL,
        ))
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
