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
    UPLOAD = ':/icons/upload.png'
    DOWNLOAD = ':/icons/download.png'
    OPEN = ':/icons/file-open.png'
