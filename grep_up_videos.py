#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
@author: ysw
@Time:2022/9/2 17:57
@Function:
"""
import json
import os
import re
import subprocess
from urllib.parse import urlencode
import requests
from tqdm import tqdm

# 这里使用会话，尽量节省后面头部参数值传来传去的麻烦
rs = requests.Session()
rs.headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
}


def get_title_and_bvid(mid, pn):
    query_parameter = {
        "mid": mid,
        "pn": pn,
        "ps": 25,
        "index": 1,
        "jsonp": "jsonp",
    }
    s = rs.get(url="https://api.bilibili.com/x/space/arc/search?" + urlencode(query_parameter))
    video_list = s.json()['data']['list']['vlist']  # 实际有用的信息在vlist里面
    prefix = "https://www.bilibili.com/video/"
    ret_info = {}
    for video in video_list:
        ret_info[video['title']] = prefix + video['bvid']
    return ret_info


def get_audio_video(ret_info):
    video_info = []
    for title, url in ret_info.items():
        rs.headers['referer'] = url
        try:
            text = rs.get(url=url).text
            json_data = re.findall('<script>window.__playinfo__=(.*?)</script>', text)[0]
            json_data = json.loads(json_data)
            # 音频地址
            audio_url = json_data['data']['dash']['audio'][0]['backupUrl'][0]
            # 视频地址
            video_url = json_data['data']['dash']['video'][0]['backupUrl'][0]
            video_info.append([title, audio_url, video_url])
        except Exception as e:
            # traceback.print_exc()
            print(f"标题为 {title} 的视频无法正确提取，已跳过该视频")
    return video_info


def download(video_info, path_prefix):
    print("下载音频和视频")
    for title, audio_url, video_url in tqdm(video_info):
        audio_req = rs.get(url=audio_url)
        audio_data = audio_req.content
        audio_path = os.path.join(path_prefix, f"{title}_audio.mp3")
        with open(audio_path, mode='wb') as f:
            f.write(audio_data)
        video_req = rs.get(url=video_url)
        video_data = video_req.content
        video_path = os.path.join(path_prefix, f"{title}_video.mp4")
        with open(video_path, mode='wb') as f:
            f.write(video_data)
        store_path = os.path.join(path_prefix, f"{title}.mp4")
        cmd = f'ffmpeg -i {audio_path} -i {os.path.join(video_path)} -c:v copy -c:a copy {store_path}'

        subprocess.call(cmd, shell=True)
        # 删除源文件
        os.remove(audio_path)
        os.remove(video_path)


if __name__ == '__main__':
    # up主的mid，打开up主的主页，最后面那串数字就是，比如陈翔六点半的主页地址https://space.bilibili.com/19286458，则mid就是19286458
    mid = 19286458
    pn = 1  # 第几页，一般一个up的主页的第一页只能放25个视频，后面也是如此，这个参数用于设置爬取第几页的视频
    path_prefix = 'G:/temp2'  # 存储文件夹，下载下来的视频存放在哪里，建议写绝对路径

    # 第一步，获取各个视频的bvid
    ret_info = get_title_and_bvid(mid, pn)
    # 第二步，拿bvid去获取各个视频的音频和视频的地址
    video_info = get_audio_video(ret_info)
    # 第三步，访问音频和视频地址并进行存储，使用ffmpeg将音频和视频组合起来
    download(video_info, path_prefix)
    print('done')
