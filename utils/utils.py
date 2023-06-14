import re
import requests
import json

headers={
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
    'referer':'https://hitomi.la/',
}

def get_gallery_id(url:str):
    '''
    根据主页获取galleryid
    xxx-388036-211xxxx.html >> 211xxxx
    '''
    pattern=r'.*?-(?P<gallery_id>\d+).html.*'
    match=re.match(pattern=pattern,string=url).group('gallery_id')
    return match

def get_image_infos(gallery_id):
    '''
    根据画廊id,请求js网址获得即该作品的所有信息,
    其中files被更改为hash存储所有哈希值
    '''
    infos={}
    js_url=f'https://ltn.hitomi.la/galleries/{gallery_id}.js' 
    with requests.get(js_url,headers=headers) as response:
        data=response.text
        match=re.match(pattern=r'.*?({.*})',string=data).group(1) #去除不需要的部分
        images_data=json.loads(match) #转为python格式,是字典
        images_data['hash']=[hash['hash'] for hash in images_data['files']] #获取哈希值列表
    return images_data

