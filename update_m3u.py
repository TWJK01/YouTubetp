import re
import os

def get_video_id(url):
    pattern = r"(?:v=|live\/|embed\/|youtu\.be\/|shorts\/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def convert():
    input_file = "https://github.com/TWJK01/YouTube/raw/refs/heads/main/live_list.txt"
    output_file = "playlist.m3u"
    
    # 檢查原始檔案是否存在
    if not os.path.exists(input_file):
        print(f"錯誤：找不到 {input_file}，建立空檔案以防止 Action 報錯。")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    m3u_content = "#EXTM3U\n"
    current_group = "未分類"
    count = 0

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        
        if ",#genre#" in line:
            current_group = line.split(",")[0].strip()
            continue
            
        if "," in line:
            try:
                parts = line.split(",", 1)
                title = parts[0].strip()
                url = parts[1].strip()
                
                video_id = get_video_id(url)
                if video_id:
                    logo = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                    m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="{title}" tvg-logo="{logo}" group-title="{current_group}",{title}\n'
                    m3u_content += f"{url}\n"
                    count += 1
            except Exception as e:
                print(f"跳過行 {line}: {e}")

    # 強制寫入檔案，即使 count 為 0
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"轉換完成！共處理 {count} 個頻道。檔案已寫入 {output_file}")

if __name__ == "__main__":
    convert()
