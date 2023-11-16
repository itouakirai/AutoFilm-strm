# AutoFilm-strm
**加速strm文件生成**
## 注意
只魔改了autofilm.py文件，只测试了单生成strm，其余未测，
如果想更快或更慢，请修改文中两处（max_workers=5）中的数值，默认为5，参考自己配置修改
## win/常见liunx使用教程
详情见[Akimio的博客](https://blog.akimio.top/posts/1031/#使用教程)
## arch/manjaro系统使用教程
查看py版本确保是3
python --version
创建虚拟环境，因为虚拟环境在根目录下所以需要sudo命令，可自行修改也可按实例来
sudo python -m venv /path/to/your/venv
切换到虚拟环境
sudo source /path/to/your/venv/bin/activate
先升级一下
sudo pip install --upgrade pip
安装webdav3
pip install webdavclient3
然后就可以正常使用脚本了，下次使用前只要切换到虚拟环境就行，请自行补全下面的脚本的参数
sudo python3 ./autofilm.py --webdav_url http://192.168.31.162:5244/dav/gdrive/团队盘/最新电影/ --username admin --password root
    
## 已知问题
貌似windows端遇见#号开头的文件夹会返回文件错误，自行去alist隐藏文件夹。

## Star History
<a href="https://github.com/Akimio521/AutoFilm/stargazers">
    <img width="500" alt="Star History Chart" src="https://api.star-history.com/svg?repos=Akimio521/AutoFilm&type=Date">
</a> 

## 请我喝杯咖啡吧
**如果你认为这个项目有帮到你，欢迎请我喝杯咖啡**
![欢迎请我喝咖啡](https://img.akimio.top/reward/coffee.png)
