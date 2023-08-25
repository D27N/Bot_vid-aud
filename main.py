import moviepy.editor as mpe
from teletoken import token
import telebot
import os


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        name = message.from_user.first_name
        bot.send_message(message.chat.id, f'Hello, {name}\nIn order to get audio, just send me videofile and wait a minute\n‼️But keep in mind, video size can be not more, that 20MB‼️')

    @bot.message_handler(content_types=['video'])
    def in_audio(message):
        file_name = message.video.file_name
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f'C:\\Proga\\from_video_in_audio\\{file_name}', 'wb') as video_file:
            video_file.write(downloaded_file)
        video = mpe.VideoFileClip(file_name)
        my_audio = video.audio
        my_audio.write_audiofile('new_audio.mp3')
        with open(r'C:\Proga\from_video_in_audio\new_audio.mp3', 'rb') as audio:
            bot.send_audio(message.chat.id, audio, title=f'Audiofile for {message.from_user.first_name}.mp3', reply_to_message_id=message.id)
        video.close()
        os.remove(r'C:\Proga\from_video_in_audio\new_audio.mp3')
        os.remove(f'C:\\Proga\\from_video_in_audio\\{file_name}')
    bot.infinity_polling()

if __name__ == '__main__':
    telegram_bot(token)
