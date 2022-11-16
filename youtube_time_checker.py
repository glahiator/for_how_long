from youtube_handler import YoutubeHandler
from youtube_cache import YoutubeCache
from datetime import timedelta

def prepare_link( link : str) -> str:
    res = ""
    if "youtu.be/" in link:
        res = link.split('/')[-1]
    return res


def get_durations( video_url : str ) -> None:
    yt = YoutubeHandler()
    # получить из ссылки на видео video_id
    video_id =  prepare_link(video_url)
    # из video_id найти chanel_id
    channel_id = yt.get_chanel_id(video_id)
    # проверить наличие канала в кэше
    yt_cache = YoutubeCache()
    if yt_cache.check_in_cache(channel_id):
        print( yt_cache.get_from_cache(channel_id) )
        return
    # у channel_id найти playlistId для uploads
    uploads_id = yt.get_uploads_id(channel_id)
    # получить все video_id в плейлисте uploads
    videos = yt.get_all_videos_ids(uploads_id)
    # получить длительность каждого видео в формате PT{}H{}M{}S   
    time_counter = timedelta(hours=0, minutes=0, seconds=0)
    for id, vid in enumerate(videos, start=1):
        duration = yt.get_video_duration(vid)
        num = ""
        curr_time = {  "H": 0, "M": 0, "S": 0 }
        if "P0D" in duration:
            continue
        for el in duration:
            if el == "P" or el == "T":
                continue
            if el.isdigit():
                num += el
                continue            
            curr_time[el] += int(num) if num else 0
            num = ""
        time_counter += timedelta(hours=curr_time["H"], minutes=curr_time["M"], seconds=curr_time["S"])
        print(f"{id} / {len(videos)}")
    
    yt_cache.insert_in_cache(channel_id, len(videos), time_counter.total_seconds())
    print(time_counter)
    

    
def main() -> None:
    get_durations("https://youtu.be/e_atyw0IDqg")

if __name__ == "__main__":
    main()
