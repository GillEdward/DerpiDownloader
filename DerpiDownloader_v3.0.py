import json
import urllib.request
import os
import time

def DownloadPage(page):
    print('\nReading page' + str(page))

    url = 'https://trixiebooru.org/api/v1/json/search/images?page=' + str(page)
    url += '&q=' + q
    url += '&key=' + key
    #print(url)

    headers = {'User-Agent':'Mozilla/5.0 3578.98 Safari/537.36'}
    url = urllib.request.Request(url, headers = headers)    # 浏览器伪装
    
    try:
        data = urllib.request.urlopen(url, timeout = 10)  # 访问网页
        endTime = time.time()
    except Exception as e:
        print('Errer Position: Getting json')
        print(e)
    for image in data:
        image.decode(encoding = 'utf-8', errors = 'strict') # 二进制解码
        image = json.loads(image)   # 读取json

        if len(image['images']) == 0:   # 空页面
            return True

        for i in image['images']: # 下载
            fileType = i['mime_type'][i['mime_type'].find('/') + 1:]    # 获取文件类型
            if fileType == 'svg+xml':   # 若为svg+xml 则转换为 svg
                fileType = 'svg'
            filePath = str(i['id']) + '.' + fileType

            if os.path.exists(filePath):
                print(filePath + ' already exists')
            else:
                url = i['representations']['full'] # 读取地址
                url.replace('view', 'download')
        
                headers = {'User-Agent':'Mozilla/5.0 3578.98 Safari/537.36'}
                url = urllib.request.Request(url, headers = headers)    # 浏览器伪装
        
                print('Downloading ' + filePath)
                try:
                    data = urllib.request.urlopen(url, timeout = 10).read()  # 访问网页
                except Exception as e:
                    print('Errer Position: Getting img')
                    print(e)

                file = open(filePath, 'wb')
                try:
                    file.write(data)
                except Exception as e:
                    print(e)

    return False    # 正常退出

#key = input("Input your API-KEY here, don't tell others about your KEY\nCheck your Account for the KEY at\n\thttps://trixiebooru.org/registrations/edit or \n\thttps://derpibooru.org/registrations/edit")
key = input("你可以在账户里找到你的API-KEY\n\thttps://trixiebooru.org/registrations/edit \n\tor \n\thttps://derpibooru.org/registrations/edit\nAPI-KEY:")

q = input('搜索栏: ')
q = q.replace(' ', '+')
q = q.replace(':', '%3A')
q = q.replace(',', '%2C')

root = 'imageDownload'
filePath = root + '/' + q

if not os.path.exists(root):
    os.mkdir(root)
if not os.path.exists(filePath):
    os.mkdir(filePath)
os.chdir(filePath)

print('a.自动下载所有')
print('b.下载指定页')
option = input('选择: ')

startTime = time.time()
endTime = time.time()
if option == 'A' or option == 'a':
    page = 1
    lastResult = []
    while True:
        startTime = time.time()
        if startTime - endTime < 5: # 强制5s时间间隔, 防止过于频繁访问
            time.sleep(5 - (startTime - endTime))

        if DownloadPage(page):    # 如果为空页面则退出
            print('Empty Page, Cycle Ended')
            break
        endTime = time.time()

        page += 1
        if(page > 100): # 防止操作不当导致的死循环
            print('Max Page Limit Reached, U can change it in the script, but be aware that too many requests may be BANNED by the site!')
            break
else:
    start = input('开始页: ')
    end = input('结束页: ')
    
    for i in range(int(start), int(end) + 1):
        startTime = time.time()
        if startTime - endTime < 5: # 强制时间间隔, 防止过于频繁访问
            time.sleep(5 - (startTime - endTime))

        if DownloadPage(i):    # 如果为空页面则退出
            print('Empty Page, Cycle Ended')
            break
        endTime = time.time()

input('Press any key to exit')