from youtube_handler import YoutubeHandler
import datetime
import aiogram
import logging
import configparser

from aiogram import Bot, Dispatcher, executor, types
import emoji

ok = emoji.emojize(":check_mark:")
warn = emoji.emojize(":red_exclamation_mark:")
info = emoji.emojize(":information:") 

config = configparser.ConfigParser()
config.read('info.ini')
API_TOKEN = config['TELEGRAM']['TOKEN']

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
yt = YoutubeHandler()

# @dp.message_handler(commands=['start', 'help'])
# async def send_welcome(message: types.Message):
#     """
#     This handler will be called when user sends `/start` or `/help` command
#     """
#     await message.reply("Пришли мне видео с youtube, а я посчитаю сколько времени тебе надо потратить, чтоб посмотреть все видео с канала!")

@dp.message_handler()
async def echo(message: types.Message):    
    video_id = prepare_link(message.text)
    if video_id == "":
        await message.answer(f"{warn} {message.text} не является ссылкой на youtube")
        return
    data = yt.get_all_videos_duration(video_id)
    time = datetime.timedelta(seconds=data['duration'])
    dur = str(time)
    if "days" in dur:
        repl = "дней"
        if time.days == 1:
            repl = "день"
        elif time.days == 2 or time.days == 3:
            repl = "дня"        
        dur = dur.replace('days,', repl)
    reply = f"На канале {data['title']} {data['counts']} видео общей длительностью {dur}"
    await message.answer(reply)

def prepare_link(link: str) -> str:
    res = ""
    if "youtu.be/" in link:
        res = link.split('/')[-1]
    elif "youtube" in link:
        pass
    return res

def main() -> None:
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
