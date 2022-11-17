from pathlib import Path
import json


class YoutubeCache:
    def __init__(self):
        self.cache = {}
        self.__load_cache()

    def check_in_cache(self, channel_id: str) -> bool:
        return channel_id in self.cache.keys()

    def get_from_cache(self, channel_id: str) -> dict:
        return self.cache[channel_id]

    def insert_in_cache(self, channel_id: str, title: str, video_counts: int, duration: float) -> dict:
        self.cache[channel_id] = {"title": title, "counts": video_counts, "duration": duration}
        self.__save_cache()
        return self.cache[channel_id]

    def __load_cache(self) -> None:
        cache_file = 'youtube_cache.json'
        cf = Path(cache_file)
        if cf.exists():
            with open(cache_file, 'r', encoding='utf-8', newline='') as f:
                self.cache = json.load(f)
                print(f"Load cache data from disk")

    def __save_cache(self) -> None:
        cache_file = 'youtube_cache.json'
        with open(cache_file, "w", encoding='utf-8', newline='') as fp:
            json.dump(self.cache, fp, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    pass
