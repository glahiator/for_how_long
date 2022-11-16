from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import configparser

class YoutubeHandler():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('info.ini')
        self.__api_key = config['API']['KEY']
        self.youtube = build('youtube', 'v3', developerKey=self.__api_key)

    def get_chanel_id(self, vid_url : str) -> str:
        request = self.youtube.videos().list(
            part="snippet",
            id=vid_url )
        try:
            response = request.execute()
        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
        channel_id = response['items'][0]["snippet"]["channelId"]        
        return channel_id
    
    def get_uploads_id(self, user_id : str) -> str:
        request = self.youtube.channels().list(
            part="contentDetails",
            id=user_id )
        try:
            response = request.execute()
        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
        uploads_id = response['items'][0]["contentDetails"]["relatedPlaylists"]["uploads"]        
        return uploads_id
    
    def get_all_videos_ids(self, playlist_id : str) -> list:
        request = self.youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults = 50 )
        videos = []
        all_videos = 0
        try:
            response = request.execute()
            for it in response['items']:
                videos.append(it["contentDetails"]["videoId"])
            all_videos = response["pageInfo"]["totalResults"]
            while len(videos) < all_videos:
                request = self.youtube.playlistItems().list_next( previous_request=request, 
                                                                  previous_response=response)
                response = request.execute()
                for it in response['items']:
                    videos.append(it["contentDetails"]["videoId"])

        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
        if len(videos) != all_videos:
            print(f"Error! Not equal sizes: {len(videos)} != {all_videos}")
        return videos

    def get_video_duration(self, video_id : str) -> str:
        request = self.youtube.videos().list(
                part="contentDetails",
                id=video_id )
        try:
            response = request.execute()
            duration = response['items'][0]['contentDetails']['duration']            
        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
        return duration

if __name__ == "__main__":
    pass