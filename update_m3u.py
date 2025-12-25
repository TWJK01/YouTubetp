import re
import os

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

    new_m3u = "#EXTM3U\n"
    current_info = ""
    current_group = "未分類"
    current_name = ""
    count = 0

    print(f"開始掃描 {input_file}，總行數: {len(lines)}")

    for line in lines:
        line = line.strip()
        if not line: continue

        # 處理分類行 (相容 M3U 格式與您之前提到的 #genre# 格式)
        if ",#genre#" in line:
            current_group = line.split(",")[0]
            print(f"發現分類標籤: {current_group}")
            continue

        # 處理 M3U 的資訊行
        if line.startswith("#EXTINF:"):
            current_info = line
            # 嘗試從原本的 M3U 裡提取 group-title
            group_match = re.search(r'group-title="([^"]+)"', line)
            if group_match:
                current_group = group_match.group(1)
            
            # 提取頻道名稱 (逗號後面的文字)
            if "," in line:
                current_name = line.split(",")[-1].strip()
            continue

        # 處理網址行 (只要是 http 開頭就視為網址)
        if line.startswith("http"):
            video_id = get_video_id(line)
            if video_id:
                logo = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                name = current_name if current_name else "未知頻道"
                
                new_m3u += f'#EXTINF:-1 tvg-id="" tvg-name="{name}" tvg-logo="{logo}" group-title="{current_group}",{name}\n'
                new_m3u += f"{line}\n"
                count += 1
                # 歸零暫存
                current_name = ""
            else:
                # 如果不是 YouTube，就保留原始網址但給個預設 logo 或不給
                new_m3u += f'#EXTINF:-1 tvg-id="" tvg-name="{current_name}" group-title="{current_group}",{current_name}\n'
                new_m3u += f"{line}\n"
                count += 1

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(new_m3u)
    
    print(f"--- 轉換完成 ---")
    print(f"成功處理頻道總數: {count}")
    print(f"結果已寫入: {output_file}")

if __name__ == "__main__":
    convert()
