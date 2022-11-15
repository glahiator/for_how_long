from googleapiclient.discovery import build
import configparser
import json

def get_api_key() -> str:
    config = configparser.ConfigParser()        
    config.read('info.ini')
    return config['API']['KEY']

def main() -> None:
    API_KEY = get_api_key()
    with build('youtube', 'v3', developerKey= API_KEY) as youtube:

        request = youtube.videos().list(
            part="snippet",
            id='j6p5OUT6798'
        )

        # request = youtube.channels().list(
        #     part = 'statistics',
        #     forUsername = 'schafer5'
        # )
        try:
            response = request.execute()
        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
        # print(response['items'][0]["snippet"]["channelId"])
        print(json.dumps(response, sort_keys=True, indent=4, ensure_ascii=False))



if __name__ == "__main__":
    main()