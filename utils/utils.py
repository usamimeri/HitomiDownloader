import re
import requests
import json
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
from requests.exceptions import HTTPError

headers={
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
    'referer':'https://hitomi.la/',
}
class Util:
    def get_gallery_id(url:str):
        '''
        根据主页获取galleryid
        xxx-388036-211xxxx.html >> 211xxxx
        '''
        pattern=r'.*?-(?P<gallery_id>\d+).html.*'
        match=re.match(pattern=pattern,string=url).group('gallery_id')
        return match

    def get_image_infos(gallery_id:str):
        '''
        根据画廊id,请求js网址获得即该作品的所有信息,
        其中files被更改为hash存储所有哈希值
        获取hash_list: images_data['hash']
        '''
        js_url=f'https://ltn.hitomi.la/galleries/{gallery_id}.js' 
        #注意 访问改连接很大概率会被禁ip,谨慎行事
        with requests.get(js_url,headers=headers) as response:
            data=response.text
            match=re.search(pattern=r'.*?({.*})',string=data).group(1) #去除不需要的部分
            images_data=json.loads(match) #转为python格式,是字典
            images_data['hash']=[hash['hash'] for hash in images_data['files']] #获取哈希值列表
            del images_data['files']
        return images_data

    def get_time_info():
        '''获取gg.js即时间戳信息和映射表信息'''
        infos={}
        js_url='https://ltn.hitomi.la/gg.js'
        with requests.get(js_url,headers=headers) as response:
            if response.status_code!=200:
                logging.error(f'获取{js_url}信息时出错')
                raise HTTPError
            time_data=response.text
            timestamp=re.search(pattern=r'b:\s+\'(\d+)/\'',string=time_data).group(1)
            mapping=re.findall(pattern=r'case (\d+?):',string=time_data)
            infos={
                'mapping':mapping, #映射表
                'timestamp':timestamp, #时间戳
            }
            return infos
    def get_subdomains(hash_list:list):
        '''
        根据哈希列表，返回一个对应的subdomain列表,即对应的十六进制数
        规则：xxx9e1 >>> 9e 1 换位>>> 19e
        '''
        subdomains=[str(int(hash[-1]+hash[-3:-1],16)) for hash in hash_list]
        return subdomains
    
    def get_mapping_result(subdomains,mapping):
        '''根据subdomain列表和映射表mapping
        获取各个对应的是aa还是bb
        subdomains=['123','456','1892']
        mapping=['2544','3652','2014']
        get_mapping_result(subdomains,mapping)
        '''
        return ['b' if subdomain in mapping else 'a' for subdomain in subdomains ]


    def get_image_urls(mapping_result:list,timestamp:str,subdomains:list,hash_list:list):
        '''
        根据：
        1. 属于a还是b
        2. 时间戳
        3. subdomain
        4. 哈希值
        组合图片的url,返回url列表
        '''
        urls=[]
        for i in zip(mapping_result,subdomains,hash_list):
            url=f'https://{i[0]}a.hitomi.la/webp/{timestamp}/{i[1]}/{i[2]}.webp'
            urls.append(url)
        return urls
    