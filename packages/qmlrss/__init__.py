import pathlib

from pydo import *

this_dir = pathlib.Path(__file__).parent

package = {
    'requires': ['qt'],
    'sysroot_debs': [],
    'root_debs': [],
    'target': this_dir / 'qmlrss.tar.gz',
    'install': ['{chroot} {stage} /bin/systemctl reenable qmlrss.service'],
}

from .. import qt
from ... import jobs

builddir = this_dir / 'build'
stage = this_dir / 'stage'
repo = this_dir / 'qmlrss'

service = this_dir / 'qmlrss.service'

@command(produces=[package['target']], consumes=[service, qt.qmake])
def build():
    call([
        f'rm -rf --one-file-system {stage} {builddir}',

        f'mkdir -p {builddir}',

        f'cd {builddir} && {qt.qmake} {repo}',
        f'make -j{jobs} -C {builddir}',

        f'mkdir -p {stage}/etc/systemd/system',
        f'mkdir -p {stage}/{qt.prefix}/bin',

        f'cp {service} {stage}/etc/systemd/system/',
        f'cp {builddir}/qmlrss {stage}/{qt.prefix}/bin/',

        f'tar -C {stage} -czf {package["target"]} .',
    ], env=qt.env, shell=True)


@command()
def clean():
    call([
        f'rm -rf --one-file-system {stage} {builddir} {package["target"]}',
    ])
