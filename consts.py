import os.path

CONFIG_FILE = 'config.yaml'


class LANGUAGE:
    Title = 'SSH Files'
    Upload = 'Upload'
    Download = 'Download'
    Open = 'Open'
    CONFIG_NOT_FOUND = 'Config file not found'
    OOPS = 'Oops!'


class HOSTS:
    REMOTE_ADDRESS = 'remote_address'
    REMOTE_PORT = 'remote_port'


class CMDS:
    SSH = "ssh"
    SSH_KILL_NIX = "killall ssh"
    SSH_KILL_WIN = "taskkill /im ssh.exe /t /f"
    SCP = "scp"
    SCP_UPLOAD_TEMPLATE = " -r {} {}@{}:{}"
    SCP_DOWNLOAD_TEMPLATE = " -r {}@{}:{} {}"


class ICONS:
    Prefix = "./"


class History:
    Prefix = "./"


if os.path.exists("./icons"):
    ICONS.Prefix = "./icons/"
elif os.path.exists("./_internal/icons"):
    ICONS.Prefix = "./_internal/icons"
else:
    print("Icons folder not found")

if os.path.exists("./history"):
    History.Prefix = "./history/"
elif os.path.exists("./_internal/history"):
    History.Prefix = "./_internal/history"
else:
    os.mkdir("history")
    History.Prefix = "./history"
