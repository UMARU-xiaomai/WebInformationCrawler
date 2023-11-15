from copy import deepcopy
import requests
import json
import msvcrt
from datetime import datetime
from bs4 import BeautifulSoup

'''
Json结构：
{
    'items':
    [
        {
            'url':'[网站链接]',
            'web_name':'[网站名称]'，
            'contents':
            [
                {
                    'title':'[栏目标题]'
                    'path':'[每个文章的标签路径]',
                    'text_path':'[文本相对路径]',
                    'format':'[日期格式]'
                    'date_path':'[日期相对路径]',
                    'latest':'[最新文章的日期]'
                },
                {
                ...
                }
            ]
            
        },
        {
        ...
        }
    ]
}
'''

def send_request(url):
    try:
        print("[MESSAGE] Sending request...")
        response = requests.get(url)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            #print(response.text)
            return response.text
        else:
            print("[ERROR] Request failed:%d",response.status_code)
            msvcrt.getch()
            exit()

    except Exception as ex:
        print("[ERROR] Unexpected error:",ex)
        msvcrt.getch()
        exit()

def search_target(html,path):
    # 使用Beautiful Soup解析HTML内容
    soup = BeautifulSoup(html, 'html.parser')
    target = soup.select(path)
    if target:
        return target
    else:
        print("[ERROR] No matched information.")
        msvcrt.getch()
        exit()

def open_file(path):
    f = open(path,'r',encoding='utf-8')
    data = json.load(f)
    f.close()
    if data :
        return data
    else:
        print("[ERROR] Can't find file'%s'"%(path))
        msvcrt.getch()
        exit()

def save_file(path,data):
    f = open(path,'w',encoding='utf-8')
    json.dump(data,f)
    f.close()

def cmp_date(l_date,c_date,forma='%Y-%m-%d'):
    d_obj1 = datetime.strptime(l_date, forma)
    d_obj2 = datetime.strptime(c_date,forma)

    if d_obj1 <= d_obj2:
        return 1
    else:
        return 0

save_path = r"web_list.json"

data = open_file(save_path)

new = []
for i,item in enumerate(data['items']):
    url = item['url']
    html = send_request(url)
    for j,con in enumerate(item['contents']):
        path = con['path']
        date_path = con['date_path']
        text_path = con['text_path']
        l_date = con['latest']
    
        target = search_target(html,path)

        n_date = target[0].select(date_path)[0].text
        for tar in target:
            date = tar.select(date_path)[0].text
            if cmp_date(l_date,date,con['format']):
                new.append("%s:%s:[%s]%s"%(item['web_name'],con['title'],date,tar.select(text_path)[0].text))

            if not cmp_date(date,n_date,con['format']):
                n_date = deepcopy(date)

        data['items'][i]['contents'][j]['latest'] = n_date


save_file(save_path,data)                
             
print("----------------------------------------------------------------------------------------------------------------------")
for i in new :
    print(i)
print("----------------------------------------------------------------------------------------------------------------------")

print("Press any key to continue...")
msvcrt.getch()
