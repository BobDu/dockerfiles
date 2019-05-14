import argparse
from shutil import copyfile

from shared import safe_mkdir


VERSIONS = ['0.9']
LANGS = ['py27', 'py36']
ARCHS = ['cpu', 'gpu']

TEMPLATE = """FROM tinymind/base:{version}
LABEL author="TinyMind" website="www.tinymind.com" email="hello@tinymind.com"

RUN conda install -y theano

COPY theanorc-{arch} /root/.theanorc
"""

BUILD_COMMAND = """docker build . -t theano{i} -f Dockerfile.theano{i}
docker tag theano{i} tinymind/theano:{i}
docker push tinymind/theano:{i}
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
    with open('/tmp/tmbuild/Dockerfile.theano{}'.format(ver), 'w+') as f:
        f.write(TEMPLATE.format(version='{}-{}'.format(l, a), arch=a))
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
