import argparse
from shutil import copyfile

from shared import safe_mkdir


VERSIONS = ['2.0', '2.1', '2.2']
LANGS = ['py36']
ARCHS = ['cpu', 'gpu']


TEMPLATE = """FROM tinymind/tensorflow:1.12-{lang}-{arch}
LABEL author="TinyMind" website="www.tinymind.com" email="hello@tinymind.com"

RUN pip install keras=={version}.*
"""

BUILD_COMMAND = """docker build . -t keras{i} -f Dockerfile.keras{i}
docker tag keras{i} tinymind/keras:{i}
docker push tinymind/keras:{i}
"""


def create_files(vs=VERSIONS, langs=LANGS, archs=ARCHS, base=True, nb=True):
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
    with open('/tmp/tmbuild/Dockerfile.keras{}'.format(ver), 'w+') as f:
        f.write(TEMPLATE.format(version=v, lang=l, arch=a))
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
