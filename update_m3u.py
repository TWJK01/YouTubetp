import re
import requests
import os
from datetime import datetime

def get_video_id(url):
    """提取 YouTube 影片 ID"""
    patterns = [
        r"(?:v=|live\/|embed\/|youtu\.be\/|shorts\/|\/v\/|e\/|u\/\w+\/|embed\/|v=)([a-zA-Z0-9_-]{11})",
        r"watch\?v=([a-zA-Z0-9_-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def convert():
    # 您的原始文字檔網址
    source_url = "https://github.com/TWJK01/YouTube/raw/refs/heads/main/live_list.txt"
    output_file = "playlist.m3u"
    
    print(f"--- 開始執行轉換 ---")
    print(f"正在抓取來源: {source_url}")
    
    try:
        r = requests.get(source_url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        lines = r.text.splitlines()
        print(f"抓取成功，檔案總行數: {len(lines)}")
    except Exception as e:
        print(f"抓取發生錯誤: {e}")
        return

    # 寫入 M3U 開頭與最後更新時間戳記
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    m3u_content = f"#EXTM3U\n# Last Update: {now}\n"
    
    current_group = "其他"
    count = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 1. 處理分類行 (例如：台灣,#genre#)
        if ",#genre#" in line:
            current_group = line.split(",")[0].strip()
            print(f"設定分類為: {current_group}")
            continue
            
        # 2. 處理頻道行 (例如：【標題】描述,網址)
        if "," in line and "http" in line:
            #
