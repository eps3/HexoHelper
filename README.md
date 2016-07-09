# HexoHelper
Hexo Auto Update Script



### 1. setting

Edit run.py

```python
#ftp user
name = 'ftproot'
#ftp password
pwd = 'ftppass'

#server ip
server = '192.168.0.1'
#server root user password
sshpwd = 'sshrootpass'


#ftp blog path
ftppath = ' /home/ftp/blog '
#nginx blog path
blogpath=' /usr/local/nginx/html/blog '
#nginx path
nginxpath=' /usr/local/nginx/html/ '
#loacl hexo public path
srcDir = r"D:\CodePlace\sheep3\sheep3\public"
```



### 2. run

```
python run.py
```



### 3. TODO

- 中文支持

