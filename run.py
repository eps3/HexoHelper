# -*- encoding=UTF-8 -*-

from ftplib import FTP
import os, sys
import paramiko
import subprocess

#你的ftp用户名
name = 'ftproot'
#你的ftp密码
pwd = 'ftppass'

#你的服务器地址
server = '192.168.0.1'
#你的root密码
sshpwd = 'sshrootpass'


#ftp路径
ftppath = ' /home/ftp/blog '
#博客目标路径
blogpath=' /usr/local/nginx/html/blog '
#nginx根路径
nginxpath=' /usr/local/nginx/html/ '
#本地hexo路径下的public文件夹路径
srcDir = r"D:\CodePlace\sheep3\sheep3\public"



_XFER_FILE = 'FILE'
_XFER_DIR = 'DIR'


class Xfer(object):
    def __init__(self):
        self.ftp = None

    def __del__(self):
        pass

    def setFtpParams(self, ip, uname, pwd, port=21, timeout=60):
        self.ip = ip
        self.uname = uname
        self.pwd = pwd
        self.port = port
        self.timeout = timeout
        self.count=0

    def initEnv(self):
        if self.ftp is None:
            self.ftp = FTP()
            print '### connect ftp server: %s ...' % self.ip
            self.ftp.connect(self.ip, self.port, self.timeout)
            self.ftp.login(self.uname, self.pwd)
            print self.ftp.getwelcome()

    def clearEnv(self):
        if self.ftp:
            self.ftp.close()
            print '### disconnect ftp server: %s!' % self.ip
            self.ftp = None

    def uploadDir(self, localdir='./', remotedir='./'):
        if not os.path.isdir(localdir):
            return
        self.ftp.cwd(remotedir)

        for file in os.listdir(localdir):
            self.count = self.count + 1
            if self.count == 1:
                try:
                    self.ftp.mkd('blog')
                    self.ftp.cwd(remotedir + 'blog')
                except:
                    sys.stderr.write('the dir is exists %s' % localdir)

            src = os.path.join(localdir, file)
            if os.path.isfile(src):
                self.uploadFile(src, file)
            elif os.path.isdir(src):
                try:
                    self.ftp.mkd(file)
                except:
                    sys.stderr.write('the dir is exists %s' % file)
                self.uploadDir(src, file)
        self.ftp.cwd('..')

    def uploadFile(self, localpath, remotepath='./'):
        if not os.path.isfile(localpath):
            return
        print '+++ upload %s to %s:%s' % (localpath, self.ip, remotepath)
        self.ftp.storbinary('STOR ' + remotepath, open(localpath, 'rb'))

    def __filetype(self, src):
        if os.path.isfile(src):
            index = src.rfind('\\')
            if index == -1:
                index = src.rfind('/')
            return _XFER_FILE, src[index + 1:]
        elif os.path.isdir(src):
            return _XFER_DIR, ''

    def upload(self, src):
        filetype, filename = self.__filetype(src)

        self.initEnv()
        if filetype == _XFER_DIR:
            self.srcDir = src
            self.uploadDir(self.srcDir)
        elif filetype == _XFER_FILE:
            self.uploadFile(src, filename)
        self.clearEnv()


def ssh2(ip, username, passwd, cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, username, passwd, timeout=5)
        for m in cmd:
            stdin, stdout, stderr = ssh.exec_command(m)
            out = stdout.readlines()
            # 屏幕输出
            for o in out:
                print o,
        print '%s\tOK\n' % (ip)
        ssh.close()
    except:
        print '%s\tError\n' % (ip)

def hexo(cmd='dir'):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print line.decode("gbk")
    retval = p.wait()

if __name__ == '__main__':
    #清除并生成html静态文件
    hexo('hexo clean')
    hexo('hexo d')
    #删除ftp下已有的文件
    ssh2(server, 'root', sshpwd, ['rm -rf '+ftppath])
    #连接FTP并上传文件
    xfer = Xfer()
    xfer.setFtpParams(server, name, pwd)
    xfer.upload(srcDir)
    #1.删除原文件
	#2.移动新文件
    ssh2(server,'root', sshpwd,['rm -rf '+blogpath, 'mv '+ftppath+nginxpath])
