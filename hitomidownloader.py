from utils.utils import Util

class HitomiDownloader:
    def __init__(self) -> None:
        self.header={
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
    'referer':'https://hitomi.la/',
}
    def by_url(self,url:str):
        '''根据画廊页面url下载'''
        pass
    def get_image_urls(self,url):
        gallery_id=Util.get_gallery_id(url)
        images_info=Util.get_image_infos(gallery_id)
        hash_list=images_info['hash']
        time_info=Util.get_time_info()
        mapping=time_info['mapping']
        timestamp=time_info['timestamp']
        subdomains=Util.get_subdomains(hash_list)
        mapping_result=Util.get_mapping_result(subdomains,mapping)
        urls=Util.get_image_urls(mapping_result,timestamp,subdomains,hash_list) #图片的url列表
        return urls
