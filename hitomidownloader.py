import requests
import os
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
import re
from requests.exceptions import HTTPError
import json

headers={
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
    'referer':'https://hitomi.la/',
}
class Util:
    def get_gallery_id(url:str):
        logging.info('正在获取画廊id')
        '''
        根据主页获取galleryid
        xxx-388036-211xxxx.html >> 211xxxx
        '''
        pattern=r'.*?-(?P<gallery_id>\d+).html.*'
        try:
            match=re.match(pattern=pattern,string=url).group('gallery_id')
        except:
            raise Exception('获取画廊id失败,请检查正则表达式或输入url的正确性')
        else:
            logging.info(f'正在获取画廊id{match}')
            return match

    def get_image_infos(gallery_id:str):
        '''
        根据画廊id,请求js网址获得即该作品的所有信息,
        其中files被更改为hash存储所有哈希值
        获取hash_list: images_data['hash']
        '''
        logging.info('正在获取图片详情信息')
        js_url=f'https://ltn.hitomi.la/galleries/{gallery_id}.js' 
        #注意 访问改连接很大概率会被禁ip,谨慎行事
        with requests.get(js_url,headers=headers) as response:
            try:
                data=response.text
                match=re.search(pattern=r'.*?({.*})',string=data).group(1) #去除不需要的部分
                images_data=json.loads(match) #转为python格式,是字典
                images_data['hash']=[hash['hash'] for hash in images_data['files']] #获取哈希值列表
                del images_data['files']
            except:
                raise Exception('获取图片详情失败，请检查是否被封禁ip')
            else:
                logging.info('正在获取图片详情信息')
                return images_data

    def get_time_info():
        '''获取gg.js即时间戳信息和映射表信息'''
        logging.info('正在获取时间戳和映射表信息')
        infos={}
        js_url='https://ltn.hitomi.la/gg.js'
        with requests.get(js_url,headers=headers) as response:
            if response.status_code!=200:
                logging.error(f'获取{js_url}信息时出错')
                raise HTTPError
            time_data=response.text
            try:
                timestamp=re.search(pattern=r'b:\s+\'(\d+)/\'',string=time_data).group(1)
                mapping=re.findall(pattern=r'case (\d+?):',string=time_data)
            except:
                raise Exception('获取时间戳和映射表失败，请检查正则表达式！')
            infos={
                'mapping':mapping, #映射表
                'timestamp':timestamp, #时间戳
            }
            logging.info('成功获取时间戳和映射表信息')
            return infos
    def get_subdomains(hash_list:list):
        '''
        根据哈希列表，返回一个对应的subdomain列表,即对应的十六进制数
        规则：xxx9e1 >>> 9e 1 换位>>> 19e
        '''
        logging.info('正在获取子域名信息')
        subdomains=[str(int(hash[-1]+hash[-3:-1],16)) for hash in hash_list]
        return subdomains
    
    def get_mapping_result(subdomains,mapping):
        '''根据subdomain列表和映射表mapping
        获取各个对应的是aa还是bb
        subdomains=['123','456','1892']
        mapping=['2544','3652','2014']
        get_mapping_result(subdomains,mapping)
        '''
        logging.info('正在进行域名信息映射')
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
    
    def get_image_urls_by_url(url):
        '''根据主页url获得所有图片的url和图片详情'''
        logging.info(f'正在根据主页信息{url}尝试获取所有图片的url和详情')
        try:
            gallery_id=Util.get_gallery_id(url)
            images_info=Util.get_image_infos(gallery_id)
            hash_list=images_info['hash']
            time_info=Util.get_time_info()
            mapping=time_info['mapping']
            timestamp=time_info['timestamp']
            subdomains=Util.get_subdomains(hash_list)
            mapping_result=Util.get_mapping_result(subdomains,mapping)
            urls=Util.get_image_urls(mapping_result,timestamp,subdomains,hash_list) #图片的url列表
        except:
            raise Exception('根据主页url获取信息时出错')
        logging.info('成功获得所有图片的url和详情')
        return urls,images_info

class HitomiDownloader:
    def __init__(self) -> None:
        self.header={
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
    'referer':'https://hitomi.la/',    
}
        self.image_infos=None
        self.image_urls=None

    def by_url(self,url:str):
        '''根据画廊页面url下载'''
        self.image_urls,self.image_infos=Util.get_image_urls_by_url(url)
        #获取所有图片的url和详情
        for i in self.image_urls:
            self.save_image(i)

        

    def save_image(self,url):
        '''根据图片链接下载图片'''
        response = requests.get(url, headers=self.header)
        logging.info(f'正在下载图片:{url}')

        japanese_title=self.image_infos['japanese_title']
        if japanese_title:
            DIR_NAME=japanese_title
        else:
            DIR_NAME=self.image_infos['title'] #标题
        FILE_NAME=str(self.image_urls.index(url)+1)+'.jpg' #比如url在第一个就命名为0
        try:
            response = requests.get(url, headers=self.header)
            if response.status_code == requests.codes.OK:
                if not os.path.exists(DIR_NAME):
                    os.mkdir(DIR_NAME)
                with open(os.path.join(DIR_NAME, FILE_NAME), 'wb') as f:  # 注意要是写入模式
                    try:
                        f.write(response.content)
                    except Exception as e:
                        print(f'保存图片发生错误,url:{url}', e)
                    else:
                        logging.info(f'成功下载url为{url}的图片')

            else:
                logging.error(f'不正确的状态码{response.status_code}')
                
        except requests.RequestException:
            logging.error(f'下载图片{url}时发生错误', exc_info=True)

downloader=HitomiDownloader()
downloader.by_url('https://hitomi.la/doujinshi/%E6%90%BE%E7%B2%BE%E3%83%AA%E3%83%88%E3%83%AB-%E3%83%95%E3%83%A9%E3%83%B3%E3%81%A1%E3%82%83%E3%82%93-%E6%97%A5%E6%9C%AC%E8%AA%9E-2564330.html#1')