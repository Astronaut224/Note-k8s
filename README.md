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
sudo curl -L "https://github.com/docker/compose/releases/download/2.3.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
# 国内镜像地址
curl -L https://get.daocloud.io/docker/compose/releases/download/1.29.1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose

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
sudo yum install -y zlib-devel perl-ExtUtils-MakeMaker
wget https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.18.0.tar.gz
tar -zxvf git-2.18.0.tar.gz
cd git-2.18.0
./configure --prefix=/usr/local/bin
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



