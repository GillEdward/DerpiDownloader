import json
import urllib.request
import os
import shutil
import time

def ReverseSearch(filename):
    url = 'https://trixiebooru.org/api/v1/json/search/reverse?'
    print(url)

    headers = {'User-Agent':'Mozilla/5.0 3578.98 Safari/537.36'}
    url = urllib.request.Request(url, headers = headers)    # 浏览器伪装
    
    data = json.dumps({'url' : 'file:///' + path + filename})
    data = bytes(data, 'utf8')
    req = urllib.request.Request(url = url, headers = headers, data = data)
    resp = urllib.request.urlopen(req).read()

    '''
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
                        '''

    return False    # 正常退出

def reorganize():
    i = 0
    for filename in os.listdir(path):
        os.rename(path + filename, path + str(i) + filename[-4:])
        i += 1

if not os.path.exists('./API-KEY.txt'):
    keyFile = open('./API-KEY.txt', 'w')
    key = input("未查询到保存过的API-KEY\n你可以在Account里找到你的API-KEY\n\thttps://trixiebooru.org/registrations/edit \n\tor \n\thttps://derpibooru.org/registrations/edit\nAPI-KEY:")
    keyFile.write(key)

keyFile = open('./API-KEY.txt', 'r')
key = keyFile.readline()

path = 'E:/Derpibooru/DerpiDownloader/ReverseImage/'

#reorganize()
for filename in os.listdir(path):
    ReverseSearch(filename)