from webdav3.client import Client
import argparse
import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor

def list_files(webdav_url, username, password, depth=None, path='', count=0):
    options = {
        'webdav_hostname': webdav_url,
        'webdav_login': username,
        'webdav_password': password
    }

    client = Client(options)
    
    try:
        items = client.list()
    except:
        print(f'连接失败，请检查网络设置！')
        exit()

    directory = []
    files = []

    def process_item(item):
        nonlocal directory, files


        if item[-1] == '/':
            if depth is None or depth > 0:
                subdirectory, subfiles, subcount = list_files(webdav_url + item, username, password, depth=None if depth is None else depth - 1, path=path + item)
                directory += [item + subitem for subitem in subdirectory]
                files += [item + subitem for subitem in subfiles]
                count += subcount
                
            else:
                directory.append(item)
        else:
            files.append(item)

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(process_item, items[1:])
    
    if path:
        print(f'当前文件夹路径：{path}')

    return directory, files, count

def download_file(url, local_path, filename, total_count):
    p = 1
    while p < 10:
        try:
            print('正在下载：' + filename)
            r = requests.get(url.replace('/dav', '/d'))
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, 'wb') as f:
                f.write(r.content)
        except:
            print(f'第{p}次下载失败，{p + 1}秒后重试...')
            p += 1
            time.sleep(p)
        else:
            if p > 1:
                print('重新下载成功！')
            print(filename + '下载成功！')
            break
        progress = int((p / 10) * 100)
        print(f'已完成 {progress}%，共 {total_count} 个文件')

def process_file(args, url, download_count, count):
    if url[-1] == '/':
        return

    filename = os.path.basename(url)
    local_path = os.path.join(args.output_path, url.replace(args.webdav_url, '').lstrip('/'))
    file_ext = filename[-3:].upper()

    if file_ext in ['MP4', 'MKV', 'FLV', 'AVI']:
        if not os.path.exists(os.path.join(args.output_path, filename[:-3] + 'strm')):
            print('正在处理：' + filename)
            try:
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                with open(os.path.join(local_path[:-3] + 'strm'), "w", encoding='utf-8') as f:
                    f.write(url.replace('/dav', '/d'))
            except:
                print(filename + '处理失败，文件名包含特殊符号，建议重命名！')
    elif args.subtitle == 'true' and file_ext in ['ASS', 'SRT', 'SSA']:
        if not os.path.exists(local_path):
            download_file(url, local_path, filename, count)
            download_count += 1
    elif args.nfo == 'true' and file_ext == 'NFO':
        if not os.path.exists(local_path):
            download_file(url, local_path, filename, count)
            download_count += 1
    elif args.img == 'true' and file_ext in ['JPG', 'PNG']:
        if not os.path.exists(local_path):
            download_file(url, local_path, filename, count)
            download_count += 1

    progress = int((download_count / count) * 100)
    print(f'已完成 {progress}%，共 {count} 个文件')

def main():
    parser = argparse.ArgumentParser(description='Autofilm script')
    parser.add_argument('--webdav_url', type=str, help='WebDAV服务器地址', required=True)
    parser.add_argument('--username', type=str, help='WebDAV账号', required=True)
    parser.add_argument('--password', type=str, help='WebDAV密码', required=True)
    parser.add_argument('--output_path', type=str, help='输出文件目录', default='./Media/')
    parser.add_argument('--subtitle', type=str, help='是否下载字幕文件', choices=['true', 'false'], default='true')
    parser.add_argument('--nfo', type=str, help='是否下载NFO文件', choices=['true', 'false'], default='false')
    parser.add_argument('--img', type=str, help='是否下载JPG和PNG文件', choices=['true', 'false'], default='false')
    args = parser.parse_args()

    print('启动参数：')
    print(f'Webdav服务器地址：{args.webdav_url}')
    print(f'Webdav登入用户名：{args.username}')
    print(f'Webdav登入密码：{args.password}')
    print(f'文件输出路径：{args.output_path}')
    print(f'是否下载字幕：{args.subtitle}')
    print(f'是否下载电影信息：{args.nfo}')
    print(f'是否下载图片：{args.img}')

    directory, files, count = list_files(args.webdav_url, args.username, args.password, depth=None, path='', count=0)

    urls = [args.webdav_url + item for item in directory + files]

    download_count = 0

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_file, args, url, download_count, count) for url in urls]

    print('处理完毕！')

if __name__ == "__main__":
    main()
