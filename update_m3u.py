import re
import os

def get_video_id(url):
    # 提取 YouTube ID (支援 watch?v=, live/, shorts/, youtu.be/)
    pattern = r"(?:v=|live\/|embed\/|youtu\.be\/|shorts\/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def convert():
    input_file = "https://github.com/TWJK01/YouTube/raw/refs/heads/main/live_list.txt"
    output_file = "playlist.m3u"
    
    if not os.path.exists(input_file):
        print("錯誤：找不到 live_list.txt")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 使用正則表達式解析 M3U 的每一組頻道
    # 匹配 #EXTINF 和緊接著的下一行 URL
    pattern = re.compile(r'(#EXTINF:[^\n]+group-title="([^"]+)"[^,]+,([^\n]+))\n(http[^\n]+)')
    matches = pattern.findall(content)

    new_m3u = "#EXTM3U\n"
    count = 0

    for original_info, group, name, url in matches:
        video_id = get_video_id(url.strip())
        if video_id:
            # 統一生成 YouTube 高清縮圖網址
            logo = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            # 重新組合成標準格式
            new_m3u += f'#EXTINF:-1 tvg-id="" tvg-name="{name.strip()}" tvg-logo="{logo}" group-title="{group.strip()}",{name.strip()}\n'
            new_m3u += f"{url.strip()}\n"
            count += 1

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(new_m3u)
    
    print(f"轉換完成！已處理 {count} 個頻道，並更新縮圖網址。")

if __name__ == "__main__":
    convert()
