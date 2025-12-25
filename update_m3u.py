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
    
    print("--- 開始執行轉換 ---")
    
    try:
        r = requests.get(source_url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        lines = r.text.splitlines()
        print(f"抓取成功，檔案總行數: {len(lines)}")
    except Exception as e:
        print(f"抓取發生錯誤: {e}")
        return

    # 寫入 M3U 開頭
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    m3u_content = f"#EXTM3U\n# Last Update: {update_time}\n"
    
    current_group = "其他"
    count = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 1. 處理分類行 (例如：台灣,#genre#)
        if ",#genre#" in line:
            current_group = line.split(",")[0].strip()
            continue
            
        # 2. 處理頻道行 (例如：標題,網址)
        if "," in line and "http" in line:
            parts = line.rsplit(",", 1)
            if len(parts) == 2:
                title = parts[0].strip()
                url = parts[1].strip()
                video_id = get_video_id(url)
                
                # 組裝 M3U 資訊
                if video_id:
                    logo = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                    m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{current_group}",{title}\n'
                else:
                    m3u_content += f'#EXTINF:-1 group-title="{current_group}",{title}\n'
                
                m3u_content += f"{url}\n"
                count += 1

    # 存檔
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"轉換完成！成功處理 {count} 個頻道。")

if __name__ == "__main__":
    convert()
