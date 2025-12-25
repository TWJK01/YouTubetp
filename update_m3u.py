import re
import requests

def get_video_id(url):
    # 支援 watch?v=, .be/, /live/, /embed/ 等多種 YouTube 網址格式
    pattern = r"(?:v=|live\/|embed\/|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def convert():
    # 如果原始檔案在 GitHub 上，也可以改成從網址讀取
    input_file = "live_list.txt" 
    output_file = "playlist.m3u"
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("錯誤：找不到 live_list.txt")
        return

    m3u_content = "#EXTM3U\n"
    current_group = "未分類"

    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 偵測大題分類 (例如：風景,#genre#)
        if ",#genre#" in line:
            current_group = line.split(",")[0]
            continue
            
        # 處理頻道資料 (標題,網址)
        if "," in line:
            parts = line.split(",", 1)
            title = parts[0].strip()
            url = parts[1].strip()
            
            video_id = get_video_id(url)
            if video_id:
                # 抓取最高畫質縮圖
                logo = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                
                # 組合 M3U 格式
                m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="{title}" tvg-logo="{logo}" group-title="{current_group}",{title}\n'
                m3u_content += f"{url}\n"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("轉換完成，playlist.m3u 已更新。")

if __name__ == "__main__":
    convert()
