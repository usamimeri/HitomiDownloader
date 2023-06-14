# HitomiDownloader
下载hitomi.la上的资源

## 思路
注意以下必须要注意referer 不然会报错！
1. 用户输入画廊链接
2. 提取链接的galleryid
3. 请求js地址，返回数据https://ltn.hitomi.la/galleries/画廊的id.js
3. 请求gg.js,https://ltn.hitomi.la/gg.js 返回映射表，时间戳
4. 解析返回数据，格式化，返回info并存储本地cache
    > 需要注意这步关键是获取哈希值
6. 根据哈希值获取subdomain即十六进制数部分
7. 根据返回映射表判断链接
8. 以上 获取了所有图片的下载链接
9. 下载为jpg格式 可以多线程，只需要传入url
