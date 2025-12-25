import re
import os
from datetime import datetime  # 引入時間模組

def get_video_id(url):
    pattern = r"(?:v=|live\/|embed\/|youtu\.be\/|shorts\/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def convert():
    input_file = "https://github.com/TWJK01/YouTube/raw/refs/heads/main/live_list.txt"
    output_file = "playlist.m3u"
    
    if not os.path.exists(input_file):
        print(f"錯誤：找不到 {input_file}")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 在開頭加入更新時間備註
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_m3u = f"#EXTM3U\n# 更新時間: {update_time}\n"
    
    current_group = "未分類"
    current_name = ""
    count = 0

    for line in lines:
        line = line.strip()
        if not line: continue
        if ",#genre#" in line:
            current_group = line.split(",")[0]
            continue
        if line.startswith("#EXTINF:"):
            group_match = re.search(r'group-title="([^"]+)"', line)
            if group_match: current_group = group_match.group(1)
            if "," in line: current_name = line.split(",")[-1].strip()
            continue
        if line.startswith("http"):
            video_id = get_video_id(line)
            if video_id:
                logo = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                name = current_name if current_name else "未知頻道"
                new_m3u += f'#EXTINF:-1 tvg-id="" tvg-name="{name}" tvg-logo="{logo}" group-title="{current_group}",{name}\n'
                new_m3u += f"{line}\n"
                count += 1
                current_name = ""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(new_m3u)
    print(f"轉換完成，成功處理 {count} 個頻道。")

if __name__ == "__main__":
    convert()
