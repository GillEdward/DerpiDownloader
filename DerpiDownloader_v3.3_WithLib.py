import json
import urllib.request
import os
import shutil
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
            if fileType == 'jpeg':
                fileType = 'jpg'
            if fileType == 'svg+xml':   # 若为svg+xml 则转换为 svg
                fileType = 'svg'
            filePath = str(i['id']) + '.' + fileType

            try:
                shutil.copy(os.path.join(target, fileId[fileName.index(filePath)] + '.info', filePath), filePath)
                print(filePath + ' exists in liberary')
            except ValueError:
                if os.path.exists(filePath):
                    print(filePath + ' already exists')                
                else:
                    url = i['representations']['full'] # 读取地址
                    url.replace('view', 'download')
            
                    headers = {'User-Agent':'Mozilla/5.0 3578.98 Safari/537.36'}
                    url = urllib.request.Request(url, headers = headers)    # 浏览器伪装
            
                    print('Downloading ' + filePath)
                    while True:
                        try:
                            data = urllib.request.urlopen(url, timeout = 10).read()  # 访问网页
                            break
                        except Exception as e:
                            print('Errer Position: Getting img')
                            print(e)
        
                    file = open(filePath, 'wb')
                    try:
                        file.write(data)
                    except Exception as e:
                        print(e)

    return False    # 正常退出

if not os.path.exists('./API-KEY.txt'):
    keyFile = open('./API-KEY.txt', 'w')
    key = input("未查询到保存过的API-KEY\n你可以在Account里找到你的API-KEY\n\thttps://trixiebooru.org/registrations/edit \n\tor \n\thttps://derpibooru.org/registrations/edit\nAPI-KEY:")
    keyFile.write(key)

keyFile = open('./API-KEY.txt', 'r')
key = keyFile.readline()

print('(若需要特定排序模式可以直接复制网址栏 q= 后面的所有内容并粘贴)')

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

start = 1
end = 100
if option == 'B' or option == 'b':
    start = int(input('开始页: '))
    end = int(input('结束页: '))
    
# Eagle Lib 图库导入
target = r'E:\Derpibooru.library\images'
fileId = []
fileName = []

print('\nLoading Liberary...')
for root, dirs, files in os.walk(target):
    for name in files:
        if name[-4:] == 'json':
            data = open(os.path.join(root, name), 'r', encoding = 'utf-8').readline()
            data = json.loads(data)   # 读取json
            fileId.append(data['id'])
            fileName.append(data['name'] + '.' + data['ext'])
print('...Complete')

for i in range(start, end + 1):
    startTime = time.time()
    if startTime - endTime < 5: # 强制时间间隔, 防止过于频繁访问
        time.sleep(5 - (startTime - endTime))

    if DownloadPage(i):    # 如果为空页面则退出
        print('Empty Page, Cycle Ended')
        break
    endTime = time.time()

input('Press any key to exit')