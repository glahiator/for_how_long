from youtube_handler import YoutubeHandler
import datetime


def prepare_link(link: str) -> str:
    res = ""
    if "youtu.be/" in link:
        res = link.split('/')[-1]
    elif "youtube" in link:
        pass
    return res


def get_durations(video_url: str) -> None:
    yt = YoutubeHandler()
    video_id = prepare_link(video_url)
    data = yt.get_all_videos_duration(video_id)

    dur = str(datetime.timedelta(seconds=data['duration']))
    print(f"For {data['title']} channel with {data['counts']} videos summ diration = {dur}")


def main() -> None:
    get_durations("https://youtu.be/Kji4PvHwYso")


if __name__ == "__main__":
    main()
