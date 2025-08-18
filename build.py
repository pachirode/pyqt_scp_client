import os
import pathlib
import shutil
import sys
import PyQt5

pyinstaller_path = pathlib.Path(sys.executable).parent / "Scripts" / 'pyinstaller.exe'


class Builder:
    def build(self):
        shutil.rmtree('./dist/', True)
        shutil.rmtree('./build/', True)

        cmd = (
            f'{pyinstaller_path.__str__()} '
            # '-i Logo.ico '
            '--noconfirm '
            '-D '
            '-w '
            # '-F '
            '--clean '
            '--name "ssh_client" '
            '--add-data "F:/code/pyqt_scp_client/icons/;./icons/" '
            'app.py'
        )
        print(cmd)
        os.system(cmd)


if __name__ == '__main__':
    builder = Builder()
    builder.build()
