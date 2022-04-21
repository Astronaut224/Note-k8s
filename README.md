# 项目介绍

采用python语言开发，基于Django框架设计的web笔记，将笔记项目容器化部署，用k8s搭建高可用集群进行管理。



# 部署步骤

## 项目容器化部署

1. 在服务器上关闭防火墙、selinux，在服务器上先创建用户：

```bash
useradd wyh
echo admin | passwd --stdin wyh
# 给用户加sudo权限
vim /etc/sudoers
# 在用户下创建文件
su - wyh
mkdir src
mkdir app
```



2. 安装docker和docker-compose

```bash
#官方脚本自动安装
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
# 国内镜像
curl -sSL https://get.daocloud.io/docker | sh

# 或者手动安装
# 首先安装必要依赖
sudo yum install -y yum-utils \
  device-mapper-persistent-data \
  lvm2
 
# 添加仓库源sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
 
# 最后安装docker
sudo yum install docker-ce docker-ce-cli containerd.io

# 启动docker
$ sudo systemctl start docker

# 设置Docker源加速
curl -sSL https://get.daocloud.io/daotools/set_mirror.sh | sh -s http://f1361db2.m.daocloud.io

# 把系统当前用户加入docker组
sudo usermod -aG docker ${USER}

=================================================

# 安装docker-compose
yum -y install epel-release
yum install python-pip
cd /usr/local/bin

wget https://github.com/docker/compose/releases/download/v2.4.1/docker-compose-linux-x86_64
mv docker-compose-linux-x86_64 docker-compose

# 给docker compose 目录授权
sudo chmod +x /usr/local/bin/docker-compose

# 查看一下version，显示有版本号那就说明安装成功了
docker-compose version
```



3. 安装git，拉取项目代码

```bash
cd /home/wyh/src
sudo yum install -y wget
sudo yum install -y gcc-c++
sudo yum install curl-devel -y
sudo yum install -y zlib-devel perl-ExtUtils-MakeMaker
wget https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.18.0.tar.gz
tar -zxvf git-2.18.0.tar.gz
cd git-2.18.0
./configure --prefix=/usr/local
make
sudo make install
git --version

# 拉项目代码
cd /home/wyh/app
git config --global user.name "Your Name"
git config --global user.email "email@example.com"
git clone https://github.com/Astronaut224/Note-k8s.git
```



4. 部署项目到容器中

```bash
cd Note-k8s
# 构建容器
docker-compose -f production.yml build
# 启动容器
docker-compose -f production.yml up
```



5. 访问项目创建笔记需要用户，添加用户命令

```bash
docker exec -it note-k8s python manage.py createsuperuser
```



## 迁移到k8s

通过kompose转换production.yml文件，先安装kompose

```bash

curl -L https://github.com/kubernetes/kompose/releases/download/v1.26.0/kompose-linux-amd64 -o kompose

chmod +x kompose

sudo mv ./kompose /usr/local/bin/kompose

kompose version

kompose convert -f docker-compose.yml 

```

安装好了执行yaml文件，如果报了错可能是kubernetes-master与本机没有绑定。

```bash
error:The connection to the server localhost:8080 was refused - did you specify the right host or port

具体根据情况，此处记录linux设置该环境变量
方式一：编辑文件设置
	   vim /etc/profile
	   在底部增加新的环境变量 export KUBECONFIG=/etc/kubernetes/admin.conf
方式二:直接追加文件内容
	echo "export KUBECONFIG=/etc/kubernetes/admin.conf" >> /etc/profile
	source /etc/profile

```

此外kompose转换了有几个pvc文件，但是没有pv文件，所以要自己创建对应的pv文件。

```bash
vim xxx-persistentvolume.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: esdata
  labels:
    type: local
spec:
  storageClassName: esdata
  capacity:
    storage: 100Mi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"
```

将得到的yaml文件根据自己的需求可以修改一些参数，然后最后执行Yaml文件即可：
```bash
kubectl apply -f xxx.yaml
```