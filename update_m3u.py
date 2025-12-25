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
        response = requests.get(url_source, timeout=30)
        response.raise_for_status()
        # 強制使用 utf-8-sig 以處理可能存在的 BOM 頭
        content = response.content.decode('utf-8-sig')
        lines = content.splitlines()
        print(f"成功讀取檔案，總行數: {len(lines)}")
    except Exception as e:
        print(f"抓取失敗: {e}")
        return

    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    m3u_content = f"#EXTM3U\n# Last Update: {update_time}\n"
    
    current_group = "未分類"
    current_name = "未知頻道"
    count = 0

    for line in lines:
        # 去除前後空白與不可見字元
        line = line.strip()
        if not line:
            continue
        
        # 1. 辨識分類行 (相容「分類名,#genre#」)
        if ",#genre#" in line:
            current_group = line.split(",")[0].strip()
            print(f"切換分類: {current_group}")
            continue
            
        # 2. 辨識 M3U 資訊行 (提取群組和名稱)
        if line.startswith("#EXTINF:"):
            group_match = re.search(r'group-title="([^"]+)"', line)
            if group_match:
                current_group = group_match.group(1)
            if "," in line:
                current_name = line.split(",")[-1].strip()
            continue
            
        # 3. 改進的網址辨識：只要行內包含 http 且不是註解
        if "http" in line and not line.startswith("#"):
            # 提取真正的網址部分（防止行尾有雜質）
            url_match = re.search(r'(https?://[^\s\s]+)', line)
            if url_match:
                url = url_match.group(1)
                video_id = get_video_id(url)
                
                # 如果這行只有網址，沒有先前的 #EXTINF，給它一個預設名稱
                display_name = current_name
                
                if video_id:
                    logo = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                    m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="{display_name}" tvg-logo="{logo}" group-title="{current_group}",{display_name}\n'
                else:
                    m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="{display_name}" group-title="{current_group}",{display_name}\n'
                
                m3u_content += f"{url}\n"
                count += 1
                # 重置名稱，避免下一個網址誤用上一個名稱
                current_name = "未知頻道"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"轉換完成！成功處理 {count} 個頻道。")

if __name__ == "__main__":
    convert()
