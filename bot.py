import os
import subprocess
import telebot

TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Отправь мне файл .epub, и я верну его бионическую версию.")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if not message.document.file_name.endswith('.epub'):
        bot.reply_to(message, "Жду файл формата EPUB!")
        return

    msg = bot.reply_to(message, "Скачиваю и обрабатываю...")
    
    try:
        # Скачиваем книгу из Telegram
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        input_path = message.document.file_name
        
        with open(input_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # Запускаем консольный скрипт конвертера
        subprocess.run(['python', 'converter/brec.py', input_path], check=True)
        
        output_path = f"bionic_{input_path}"
        
        # Отправляем результат обратно
        if os.path.exists(output_path):
            with open(output_path, 'rb') as doc:
                bot.send_document(message.chat.id, doc)
            os.remove(output_path)
        else:
            bot.edit_message_text("Ошибка: файл не сконвертировался.", chat_id=message.chat.id, message_id=msg.message_id)
            
        os.remove(input_path)
        
    except Exception as e:
        bot.edit_message_text(f"Ошибка: {str(e)}", chat_id=message.chat.id, message_id=msg.message_id)

bot.polling(none_stop=True)
