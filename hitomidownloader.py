from utils.utils import Util
import requests
import os
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
downloader.by_url('')