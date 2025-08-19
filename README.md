# Pyqt5 scp client

主要用于配置 `Window` 本机传递文件给远程 `Debain` 服务器，选择文件夹进行同步

### 背景

主要为了学习 `K8S` 集群部署，为了方便虚拟机和物理机之间同步代码

### 安装

可以之间下载打包好的文件 [Release](https://github.com/pachirode/pyqt_scp_client/releases)

### 源码安装

```shell
pip install -r requirements.txt # 安装依赖
cp config.example.yml config.ym # 创建配置文件
python app.py

# 打包成单个可执行文件
pip install pyinstaller
pyinstaller --onefile --noconsole app.py
```

### 配置文件
配置文件参考 `config.example.yaml`

```yaml
servers:
  k8s:  # 需要登陆的用户名
    ip: 192.168.29.131 
    local_dir: ./ # 本地目录
    remote_dir: /home/k8s/Templates # 远程服务器路径
```

### TODO
1. 添加配置文件记录开关
2. 添加远程服务器密码配置（支持环境变量）
3. 自定义图标
4. 添加设置界面替代配置文件