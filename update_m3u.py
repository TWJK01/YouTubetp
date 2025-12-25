import re
import requests
import os
from datetime import datetime

def get_video_id(url):
    # 支援 YouTube 各種網址格式 (watch, live, short, youtu.be)
    pattern = r"(?:v=|live\/|embed\/|youtu\.be\/|shorts\/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def convert():
    # 您指定的原始清單網址
    url_source = "https://github.com/TWJK01/YouTube/raw/refs/heads/main/live_list.txt"
    output_file = "playlist.m3u"
    
    print(f"正在從網址抓取資料: {url_source}")
    
    try:
        response = requests.get(url_source)
        response.raise_for_status()
        # 確保使用 UTF-8 編碼
        response.encoding = 'utf-8'
        lines = response.text.splitlines()
    except Exception as e:
        print(f"抓取失敗: {e}")
        return

    # 加入更新時間，確保每次產生的檔案內容都不同，Git 才能偵測到更新
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    m3u_content = f"#EXTM3U\n# Last Update: {update_time}\n"
    
    current_group = "未分類"
    current_name = ""
    count = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 1. 辨識分類行 (相容「風景,#genre#」格式)
        if ",#genre#" in line:
            current_group = line.split(",")[0].strip()
            continue
            
        # 2. 辨識 M3U 資訊行 (提取群組和名稱)
        if line.startswith("#EXTINF:"):
            group_match = re.search(r'group-title="([^"]+)"', line)
            if group_match:
                current_group = group_match.group(1)
            if "," in line:
                current_name = line.split(",")[-1].strip()
            continue
            
        # 3. 辨識網址行並生成縮圖
        if line.startswith("http"):
            video_id = get_video_id(line)
            name = current_name if current_name else "未知頻道"
            
            if video_id:
                logo = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="{name}" tvg-logo="{logo}" group-title="{current_group}",{name}\n'
            else:
                # 非 YouTube 網址則不加縮圖
                m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="{name}" group-title="{current_group}",{name}\n'
            
            m3u_content += f"{line}\n"
            count += 1
            current_name = "" # 清空暫存名稱

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"轉換完成！共處理 {count} 個頻道。")

if __name__ == "__main__":
    convert()
