from googleapiclient.discovery import build
import configparser
import json

from googleapiclient.errors import HttpError


def get_api_key() -> str:
    config = configparser.ConfigParser()
    config.read('info.ini')
    return config['API']['KEY']

def get_chanel_id(video_id):
    API_KEY = get_api_key()
    with build('youtube', 'v3', developerKey=API_KEY) as youtube:
        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        try:
            response = request.execute()
        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
        channel_id = response['items'][0]["snippet"]["channelId"]
        print(channel_id)
        return channel_id
        # print(json.dumps(response, sort_keys=True, indent=4, ensure_ascii=False))

def get_playlist_id(user_id):
    API_KEY = get_api_key()
    with build('youtube', 'v3', developerKey=API_KEY) as youtube:
        request = youtube.channels().list(
            part="contentDetails",
            id=user_id
        )
        try:
            response = request.execute()
        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
        upload_id = response['items'][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        print(upload_id)
        return upload_id
        # print(json.dumps(response, sort_keys=True, indent=4, ensure_ascii=False))

def get_all_videos_items(playlist_id):
    API_KEY = get_api_key()
    with build('youtube', 'v3', developerKey=API_KEY) as youtube:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults = 50
        )
        videos = []
        all_videos = 0
        try:
            response = request.execute()
            for it in response['items']:
                videos.append(it["contentDetails"]["videoId"])
            all_videos = response["pageInfo"]["totalResults"]
            while len(videos) < all_videos:
                request = youtube.playlistItems().list_next( previous_request=request, previous_response=response)
                response = request.execute()
                for it in response['items']:
                    videos.append(it["contentDetails"]["videoId"])

        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

        return all_videos, videos
        # upload_id = response['items'][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        # print(upload_id)
        # return upload_id
        # print(json.dumps(response, sort_keys=True, indent=4, ensure_ascii=False))

def calculate_durations():
    videos = []
    with open('data.json') as f:
        videos = json.load(f)
    print(f"Load from file {len(videos)} items")
    API_KEY = get_api_key()

    durations = []
    with build('youtube', 'v3', developerKey=API_KEY) as youtube:
        for vid in videos:
            request = youtube.videos().list(
                part="contentDetails",
                id=vid
            )
            try:
                response = request.execute()
                duration = response['items'][0]['contentDetails']['duration']
                # print(response)
                print( f"for {vid} duration {duration} ms" )
                durations.append(duration)

            except HttpError as e:
                print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
        return durations


def calc_all_duration():
    durations = []
    with open('duration.json') as f:
        durations = json.load(f)
    print(f"Load from file {len(durations)} items")
    all_time = {
        "H": 0,
        "M": 0,
        "S": 0
    }
    for dur in durations:
        num = ""
        time = {
            "H" : 0,
            "M" : 0,
            "S" : 0
        }
        for el in dur:
            if el == "P" or el == "T":
                continue
            if el.isdigit():
                num += el
                continue
            time[el] = int(num) if num else 0
            all_time[el] += int(num) if num else 0
            num = ""

        print(dur, time["H"], time["M"], time["S"])
    print("ALL TIME")
    print( all_time["H"], all_time["M"], all_time["S"])



# Ссылка гна видео -> найти UserID
# UserID -> PlaylistID (uploads)
# PlaylistUpload -> Все видео
# Подсчитать duration каждого видео


def main() -> None:
    # id = get_chanel_id("ggYcRwyemR0")
    # pl_id = get_playlist_id( id )
    # all_videos, videos =  get_all_videos_items(pl_id)
    # print(f"All videos count {all_videos}")
    # print(f"VideosId list len {len(videos)}")
    # with open('data1.json', 'w', encoding='utf-8') as f:
    #     json.dump(videos, f, ensure_ascii=False, indent=4)

    # durations = calculate_durations()
    # print(f"Duration list len {len(durations)}")
    # with open('duration.json', 'w', encoding='utf-8') as f:
    #     json.dump(durations, f, ensure_ascii=False, indent=4)

    calc_all_duration()


if __name__ == "__main__":
    main()
