from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_cache import YoutubeCache
from datetime import timedelta
import configparser


class YoutubeHandler:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('info.ini')
        self.__api_key = config['API']['KEY']
        self.youtube = build('youtube', 'v3', developerKey=self.__api_key)
        self.cache = YoutubeCache()

    def get_chanel_id(self, vid_url: str) :
        channel_id = ""
        channel_title = ""
        request = self.youtube.videos().list(
            part="snippet",
            id=vid_url)
        try:
            response = request.execute()
            channel_id = response['items'][0]["snippet"]["channelId"]
            channel_title = response['items'][0]["snippet"]["channelTitle"]
        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
        return channel_id, channel_title

    def get_uploads_id(self, user_id: str) :
        uploads_id = ""
        video_count = 0
        request = self.youtube.channels().list(
            part=["contentDetails", "statistics"],
            id=user_id)
        try:
            response = request.execute()
            uploads_id = response['items'][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            video_count = response['items'][0]["statistics"]["videoCount"]
        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
        return uploads_id, video_count

    def get_all_videos_ids(self, playlist_id: str) :
        request = self.youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50)
        videos = []
        all_videos = 0
        try:
            response = request.execute()
            for it in response['items']:
                videos.append(it["contentDetails"]["videoId"])
            all_videos = response["pageInfo"]["totalResults"]
            while len(videos) < all_videos:
                request = self.youtube.playlistItems().list_next(previous_request=request,
                                                                 previous_response=response)
                response = request.execute()
                for it in response['items']:
                    videos.append(it["contentDetails"]["videoId"])

        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
        if len(videos) != all_videos:
            print(f"Error! Not equal sizes: {len(videos)} != {all_videos}")
        return videos

    def get_video_duration(self, video_id: str):
        duration = ""
        request = self.youtube.videos().list(
            part="contentDetails",
            id=video_id)
        try:
            response = request.execute()
            duration = response['items'][0]['contentDetails']['duration']
        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
        return duration

    def get_all_videos_duration(self, video_id: str) :
        channel_id, channel_title = self.get_chanel_id(video_id)
        if channel_id == "":
            return {"title": 0, "counts" : 0, "duration" : 0.0}
        uploads_id, video_count = self.get_uploads_id(channel_id)
        if self.cache.check_in_cache(channel_id):
            curr_cache = self.cache.get_from_cache(channel_id)
            if curr_cache['counts'] == video_count:
                return curr_cache
        videos = self.get_all_videos_ids(uploads_id)
        time_counter = timedelta(hours=0, minutes=0, seconds=0)
        for _id, vid in enumerate(videos, start=1):
            duration = self.get_video_duration(vid)
            num = ""
            curr_time = {"H": 0, "M": 0, "S": 0}
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
            print(f"{_id} / {len(videos)}")
            time_counter += timedelta(hours=curr_time["H"], minutes=curr_time["M"], seconds=curr_time["S"])

        return self.cache.insert_in_cache(channel_id,
                                          channel_title,
                                          video_count,
                                          time_counter.total_seconds())


if __name__ == "__main__":
    pass
