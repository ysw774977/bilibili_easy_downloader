# bilibili_easy_downloader
快速下载某个bilibili的视频或大批量下载某个up主的视频



## 1、安装依赖
```shell
pip install -r requirements.txt
```

## 2、使用方法

<details>
  <summary>根据某个视频的Bvid来下载</summary>
  bvid参数的获取方法：
  点击某个视频，在网址中查看，在video后面的一串字符就是bvid<br>
  例如，陈翔六点半的某个视频地址是：https://www.bilibili.com/video/BV1HU4y1B7fn
  则该视频的bvid为BV1HU4y1B7fn
  在grep_video.py文件的main函数中，修改bvid参数，直接运行即可
</details>  

<details>
    <summary>大批量下载某个up主的视频</summary>
    在grep_up_videos.py中修改up主的mid，并修改要爬取第几页视频的参数pn
    mid的获取方法：点开某个up主的主页，在com后面的即为mid<br>
    例如陈翔六点半的主页地址为：https://space.bilibili.com/19286458 ,则mid为19286458
    九三的主页为：https://space.bilibili.com/313580179 ,则mid为313580179
</details>
