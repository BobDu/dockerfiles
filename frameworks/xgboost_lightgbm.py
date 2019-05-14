import argparse
from shutil import copyfile

from shared import safe_mkdir


VERSIONS = ['0.8_2.0.11']
LANGS = ['py27', 'py36']
ARCHS = ['cpu']
LANGS_OPERATION = {'py27': 'python', 'py36': 'python3'}
FRAMEWORKS_VERSIONS = {
    '0.8_2.0.11': {'xgboost_version': 'v0.80', 'lightgbm_version': 'v2.0.11'},
}

TEMPLATE = """FROM tinymind/base:{version}
LABEL author="TinyMind" website="www.tinymind.com" email="hello@tinymind.com"

# Build XGBoost from source
RUN git clone --recursive https://github.com/dmlc/xgboost && \\
    cd xgboost && \\
    git checkout {xgboost_version} && \\
    make -j4 && \\
    cd python-package && \\
    {python} setup.py install

# Build LightGBM from source
RUN git clone --recursive https://github.com/Microsoft/LightGBM && \\
    cd LightGBM && \\
    git checkout {lightgbm_version} && \\
    mkdir build && \\
    cd build && \\
    cmake .. && \\
    make -j4 && \\
    cd .. && cd python-package && \\
    {python} setup.py install
"""

BUILD_COMMAND = """docker build . -t xgboost_lightgbm{i} -f Dockerfile.xgboost_lightgbm{i}
docker tag xgboost_lightgbm{i} tinymind/xgboost_lightgbm:{i}
docker push tinymind/xgboost_lightgbm:{i}
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
    with open('/tmp/tmbuild/Dockerfile.xgboost_lightgbm{}'.format(ver), 'w+') as f:
        xgboost_lightgbm_version = FRAMEWORKS_VERSIONS['{}'.format(v)]
        f.write(TEMPLATE.format(
            version='{}-{}'.format(l, a),
            python=LANGS_OPERATION[l],
            xgboost_version=xgboost_lightgbm_version['xgboost_version'],
            lightgbm_version=xgboost_lightgbm_version['lightgbm_version'],
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
