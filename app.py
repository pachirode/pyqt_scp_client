import glob
import os.path
import shutil
import sys
import time

import yaml
import paramiko
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QDialog, QMessageBox, QGridLayout, QPushButton, QFileDialog

from deepdiff import DeepDiff

from consts import CONFIG_FILE, LANGUAGE, CMDS
from ssh import Ui_SSH
from sshconfig import Ui_SSHConfig


class SSHConfig(QDialog):
    def __init__(self, parent, data, name):
        super(SSHConfig, self).__init__(parent)

        self.name = name
        self.ui = Ui_SSHConfig()
        self.ui.setupUi(self)
        self.ui.Remote_ip_edit.setText(data.get("ip"))
        self.ui.Remote_dir_edit.setText(data.get("remote_dir"))
        self.ui.local_dir_edit.setText(data.get("local_dir"))

        self.ui.openDirButton.clicked.connect(self.open_dir)

    def open_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.ui.local_dir_edit.setText(directory)

    def upload(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.ui.local_dir_edit.text(), username=self.name, password="123456")
        sftp = ssh.open_sftp()

        if os.path.isfile(self.ui.local_dir_edit.text()):
            filename = os.path.basename(self.ui.local_dir_edit.text())
            remote_file_path = f"{self.ui.Remote_dir_edit.text()}/{filename}".replace("\\", "/")
            sftp.put(self.ui.local_dir_edit.text(), remote_file_path)
        elif os.path.isdir(self.ui.local_dir_edit.text()):
            self._upload_directory(sftp, self.ui.local_dir_edit.text(), self.ui.Remote_dir_edit.text())

        sftp.close()
        ssh.close()

    def _upload_directory(self, sftp, local_dir, remote_dir):
        try:
            sftp.mkdir(remote_dir)
        except:
            pass
        for item in os.listdir(local_dir):
            local_path = os.path.join(local_dir, item)
            remote_path = f"{remote_dir}/{item}".replace("\\", "/")

            if os.path.isfile(local_path):
                sftp.put(local_path, remote_path)
            elif os.path.isdir(local_path):
                self._upload_directory(
                    sftp,
                    local_path,
                    remote_path
                )

    def download(self):
        self._download_with_paramiko()

    def _download_with_paramiko(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.connect(hostname=self.ui.Remote_ip_edit.text(), username=self.name, password="123456")

            sftp = ssh.open_sftp()

            filename = os.path.basename(self.ui.Remote_dir_edit.text())
            local_file_path = os.path.join(self.ui.local_dir_edit.text(), filename)
            sftp.get(self.ui.Remote_dir_edit.text(), local_file_path)

            sftp.close()
            ssh.close()

            print("Download completed successfully")

        except Exception as e:
            print(f"Download failed: {str(e)}")

    def as_dict(self):
        return {
            "ip": self.ui.Remote_ip_edit.text(),
            "remote_dir": self.ui.Remote_dir_edit.text(),
            "local_dir": self.ui.local_dir_edit.text()
        }


class SSH(QWidget):
    def __init__(self, name, data):
        super(SSH, self).__init__()

        self.ui = Ui_SSH()
        self.ui.setupUi(self)

        self.ssh_config = SSHConfig(self, data, name)
        self.ssh_config.setWindowTitle(name)
        self.ssh_config.setModal(True)
        self.ui.name.setText(name)
        self.ssh_config.icon = f"./icons/{name}.svg"

        if not os.path.exists(self.ssh_config.icon):
            self.ssh_config.icon = "./icons/debain.svg"

        self.ui.icon.setPixmap(QPixmap(self.ssh_config.icon))
        self.ui.action_upload.clicked.connect(self.upload)
        self.ui.action_download.clicked.connect(self.download)
        self.ui.action_settings.clicked.connect(self.ssh_config.show)

        self.process = None

    def upload(self):
        self.ssh_config.upload()

    def download(self):
        self.ssh_config.download()


class SSHManager(QWidget):
    def __init__(self):
        super().__init__()
        with open(CONFIG_FILE, "r") as fp:
            self.data = yaml.load(fp, Loader=yaml.FullLoader)

        self.grid = QGridLayout(self)
        self.servers = []

        i = 0
        for i, server in enumerate(self.data["servers"]):
            server = SSH(server, self.data["servers"][server])
            self.servers.append(server)
            self.grid.addWidget(server, i, 0)

        self.close = QPushButton("Close")
        self.grid.addWidget(self.close, i + 1, 1)

        self.setLayout(self.grid)
        self.resize(10, 10)
        self.setWindowTitle(LANGUAGE.Title)
        self.show()

    def closeEvent(self, event):
        data = {"servers": {}}
        for server in self.servers:
            data["servers"][server.ui.name.text()] = server.ssh_config.as_dict()
        changed = DeepDiff(self.data, data, ignore_order=True)

        if changed:
            timestamp = int(time.time())
            shutil.copy(CONFIG_FILE, F"./history/{CONFIG_FILE}-{timestamp}")
            with open(CONFIG_FILE, "w") as fp:
                yaml.dump(data, fp)
            backup_configs = glob.glob(f"{CONFIG_FILE}-*")
            if len(backup_configs) > 10:
                for config in sorted(backup_configs, reverse=True)[10:]:
                    os.remove(config)
        event.accept()


if __name__ == '__main__':

    app = QApplication(sys.argv)

    if not os.path.exists(CONFIG_FILE):
        mb = QMessageBox()
        mb.setText(LANGUAGE.CONFIG_NOT_FOUND)
        mb.setWindowTitle(LANGUAGE.OOPS)
        mb.setStandardButtons(QMessageBox.Close)
        mb.show()
    else:
        sm = SSHManager()
    sys.exit(app.exec_())
