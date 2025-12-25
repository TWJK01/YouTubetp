import re
import requests

def get_video_id(url):
    # 支援 YouTube 各種網址格式 (watch, live, short, youtu.be)
    pattern = r"(?:v=|live\/|embed\/|youtu\.be\/|shorts\/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def convert():
    input_file = "https://github.com/TWJK01/YouTube/raw/refs/heads/main/live_list.txt"
    output_file = "playlist.m3u"
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("錯誤：找不到 live_list.txt，請確認檔案已上傳至倉庫。")
        return

    m3u_content = "#EXTM3U\n"
    current_group = "未分類"

    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 辨識大題分類：例如「風景,#genre#」
        if ",#genre#" in line:
            current_group = line.split(",")[0].strip()
            continue
            
        # 處理頻道資料：【標題】名稱,網址
        if "," in line:
            try:
                parts = line.split(",", 1)
                title = parts[0].strip()
                url = parts[1].strip()
                
                video_id = get_video_id(url)
                if video_id:
                    # 使用 YouTube 官方縮圖 API
                    logo = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                    
                    # 組合為 IPTV 標準格式
                    m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="{title}" tvg-logo="{logo}" group-title="{current_group}",{title}\n'
                    m3u_content += f"{url}\n"
            except Exception as e:
                print(f"跳過錯誤行: {line} -> {e}")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("M3U 檔案已成功生成！")

if __name__ == "__main__":
    convert()
