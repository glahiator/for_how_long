import json, datetime, os
from pathlib import Path
from datetime import timedelta

class YoutubeCache():
    def __init__(self):
        self.cache = {}
        self.__load_cache()

    def check_in_cache(self, channel_id : str) -> str :        
        return channel_id in self.cache.keys()

    def get_from_cache(self, channel_id : str) -> tuple:
        return self.cache[channel_id]
    
    def insert_in_cache(self, channel_id : str, video_counts : int, duration : float ) ->None:
        self.cache[channel_id] = { "counts" : video_counts, "duration" : duration}
        self.__save_cache()

    def __load_cache(self):
        cache_file = 'youtube_cache.json'
        cf = Path(cache_file)
        if cf.exists():
            with open(cache_file, 'r', encoding='utf-8', newline='') as f:
                self.cache = json.load(f)
                print(f"Load cache data from disk")

    def __save_cache(self):
        cache_file = 'youtube_cache.json'
        with open(cache_file, "w", encoding='utf-8', newline='') as fp:
            json.dump(self.cache, fp, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    pass
