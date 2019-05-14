import argparse
from shutil import copyfile

from shared import safe_mkdir


VERSIONS = ['0.1', '0.2', '0.3', '0.4', '1.0']
LANGS = ['py27', 'py36']
ARCHS = ['cpu', 'gpu']

VMAP = {
    '0.1': '0.1.12',
    '0.2': '0.2.0',
    '0.3': '0.3.1',
    '0.4': '0.4.1',
    '1.0': '1.0.0'
}

TEMPLATE = """FROM tinymind/base:{version}
LABEL author="TinyMind" website="www.tinymind.com" email="hello@tinymind.com"

RUN pip install https://download.pytorch.org/whl/{arch}/torch-{ptversion}-cp36-cp36m-linux_x86_64.whl && \
    rm -rf ~/.cache/pip
"""

LEGACY_TEMPLATE = """FROM tinymind/base:{version}
LABEL author="TinyMind" website="www.tinymind.com" email="hello@tinymind.com"

RUN conda install -y -c soumith pytorch={ptversion} torchvision {gpuonly}
"""

BUILD_COMMAND = """docker build . -t pytorch{i} -f Dockerfile.pytorch{i}
docker tag pytorch{i} tinymind/pytorch:{i}
docker push tinymind/pytorch:{i}
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
    with open('/tmp/tmbuild/Dockerfile.pytorch{}'.format(ver), 'w+') as f:
        if v not in ('0.1', '0.2'):
            version = '{}-{}'.format(l, a)
            if a == 'gpu':
                if v in ('0.3', '0.4'):
                    version += '-cuda9'
                    a = 'cu90'
                if v in ('1.0', ):
                    version += '-cuda10'
                    a = 'cu100'
            f.write(TEMPLATE.format(
                version=version,
                ptversion=VMAP[v],
                arch=a
            ))
        else:
            # A old docker file template. Remove it in the future.
            f.write(LEGACY_TEMPLATE.format(
                version='{}-{}'.format(l, a),
                ptversion=VMAP[v],
                gpuonly='cuda80' if a == 'gpu' else '',
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
