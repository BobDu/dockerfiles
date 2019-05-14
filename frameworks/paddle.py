import argparse
from shutil import copyfile

from shared import safe_mkdir


VERSIONS = ['0.11']
LANGS = ['py27']
ARCHS = ['cpu', 'gpu']

BASE = 'https://github.com/mind/paddle-wheels/releases/download/'
TAIL = '-linux_x86_64.whl'

WHEELS = {
    '0.11-py27-cpu': BASE + '0.11/paddlepaddle-0.11.0-cp27-cp27mu' + TAIL,
    '0.11-py27-gpu': BASE + '0.11/paddlepaddle_gpu-0.11.0-cp27-cp27mu' + TAIL,
}

TEMPLATE = """FROM tinymind/base:{version}
LABEL author="TinyMind" website="www.tinymind.com" email="hello@tinymind.com"

RUN pip --no-cache-dir install {wheel}
"""

BUILD_COMMAND = """docker build . -t paddle{i} -f Dockerfile.paddle{i}
docker tag paddle{i} tinymind/paddle:{i}
docker push tinymind/paddle:{i}
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


def create_file(v, l, a):
    ver = '{}-{}-{}'.format(v, l, a)
    with open('/tmp/tmbuild/Dockerfile.paddle{}'.format(ver), 'w+') as f:
        f.write(TEMPLATE.format(
            version='{}-{}'.format(l, a) + ('-cuda9' if a == 'gpu' else ''),  # noqa
            wheel=WHEELS['{}-{}-{}'.format(v, l, a)],
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
