# HitomiDownloader
下载hitomi.la上的资源
# 当前功能
1. 根据主页信息例如`https://hitomi.la/doujinshi/%E6%90%BE%E7%B2%BE%E3%83%AA%E3%83%88%E3%83%AB-%E3%83%95%E3%83%A9%E3%83%B3%E3%81%A1%E3%82%83%E3%82%93-%E6%97%A5%E6%9C%AC%E8%AA%9E-2564330.html#1`
下载所有图片的jpg

# 计划目标
1. 多线程下载
2. 过滤器
3. 遍历所有页下载指定要求的作品
4. 避免反爬机制导致中断
5. 断点续传
# 思路

注意以下必须要注意referer 不然会报错！
1. 用户输入画廊链接
2. 提取链接的galleryid
3. 请求js地址，返回数据https://ltn.hitomi.la/galleries/画廊的id.js
3. 请求gg.js,https://ltn.hitomi.la/gg.js 返回映射表，时间戳
4. 解析返回数据，格式化，返回info并存储本地cache
    > 需要注意这步关键是获取哈希值
6. 根据哈希值获取subdomain即十六进制数部分
7. 根据返回映射表判断链接
8. 拼接映射后的信息,时间戳,子域名,哈希值
9. 以上 获取了所有图片的下载链接

