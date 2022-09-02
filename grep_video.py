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


def get_video(bvid, path_prefix):
    try:
        url = "https://www.bilibili.com/video/" + bvid
        rs.headers['referer'] = url
        text = rs.get(url=url).text
        json_data = re.findall('<script>window.__playinfo__=(.*?)</script>', text)[0]
        json_data = json.loads(json_data)
        # 音频地址
        audio_url = json_data['data']['dash']['audio'][0]['backupUrl'][0]
        # 视频地址
        video_url = json_data['data']['dash']['video'][0]['backupUrl'][0]
        audio_req = rs.get(url=audio_url)
        audio_data = audio_req.content
        audio_path = os.path.join(path_prefix, f"temp_audio.mp3")
        with open(audio_path, mode='wb') as f:
            f.write(audio_data)
        video_req = rs.get(url=video_url)
        video_data = video_req.content
        video_path = os.path.join(path_prefix, f"temp_video.mp4")
        with open(video_path, mode='wb') as f:
            f.write(video_data)
        store_path = os.path.join(path_prefix, f"video.mp4")
        cmd = f'ffmpeg -i {audio_path} -i {os.path.join(video_path)} -c:v copy -c:a copy {store_path}'
        subprocess.call(cmd, shell=True)
        # 删除源文件
        os.remove(audio_path)
        os.remove(video_path)
    except Exception as e:
        print(f"bvid:{bvid}视频下载失败，已经跳过")


if __name__ == '__main__':
    path_prefix = 'G:/temp2'  # 存储文件夹，下载下来的视频存放在哪里，建议写绝对路径
    bvid = "BV1CG41187nW"
    get_video(bvid, path_prefix)
    print('done')
