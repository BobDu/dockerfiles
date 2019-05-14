import argparse
from shutil import copyfile

from shared import safe_mkdir


VERSIONS = ['0.12', '1.0', '1.1', '1.2', '1.3']
LANGS = ['py27', 'py36']
ARCHS = ['cpu', 'gpu']

VMAP = {
    '0.12': '0.12.1',
    '1.0': '1.0.0.post4',
    '1.1': '1.1.0.post0',
    '1.2': '1.2.1.post1',
    '1.3': '1.3.1'
}

TEMPLATE = """FROM tinymind/base:{version}
LABEL author="TinyMind" website="www.tinymind.com" email="hello@tinymind.com"

RUN pip install {mxnet_pkgname}=={mxnet_version} && \
    rm -rf ~/.cache/pip
"""

BUILD_COMMAND = """docker build . -t mxnet{i} -f Dockerfile.mxnet{i}
docker tag mxnet{i} tinymind/mxnet:{i}
docker push tinymind/mxnet:{i}
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
    version = '{}-{}'.format(l, a)
    if a == 'gpu':
        if v in ('1.4', '1.5'):
            version += '-cuda10'
            mxnet_pkgname = 'mxnet-cu100'
        else:
            version += '-cuda9'
            mxnet_pkgname = 'mxnet-cu90'
    else:
        mxnet_pkgname = 'mxnet'
    with open('/tmp/tmbuild/Dockerfile.mxnet{}'.format(ver), 'w+') as f:
        f.write(TEMPLATE.format(
            version=version,
            mxnet_pkgname=mxnet_pkgname,
            mxnet_version=VMAP[v],
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
