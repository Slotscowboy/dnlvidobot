import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import yt_dlp  # Импортируем yt_dlp

# Функция для обработки команды /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Отправь мне ссылку на видео, и я скачаю его для тебя.")

# Функция для скачивания видео по ссылке
async def download_video(update: Update, context):
    # Получаем ссылку из сообщения пользователя
    url = update.message.text

    try:
        # Настройки для yt-dlp
        ydl_opts = {
            'format': 'best',  # Лучшее доступное качество
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Путь для сохранения файла
        }

        # Используем yt-dlp для скачивания видео
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', 'video')
            video_ext = info.get('ext', 'mp4')
            video_path = f"downloads/{video_title}.{video_ext}"

        # Отправляем видео пользователю
        with open(video_path, 'rb') as video_file:
            await update.message.reply_video(video=video_file)

        # Удаляем скачанный файл после отправки
        os.remove(video_path)

        # Отправляем сообщение об успешной загрузке
        await update.message.reply_text("Видео успешно скачано и отправлено!")

    except Exception as e:
        # Если произошла ошибка, отправляем сообщение об ошибке
        await update.message.reply_text(f"Произошла ошибка: {str(e)}")

# Основная функция для запуска бота
def main():
    # Замените 'YOUR_BOT_TOKEN' на ваш токен, полученный от BotFather
    application = Application.builder().token("8015660772:AAFNT4Nw7BUb_LTD2E_SbvqQDCzMa5bUnDU").build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))

    # Регистрируем обработчик текстовых сообщений (ссылок)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    # Создаем папку для скачивания видео, если её нет
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    main()