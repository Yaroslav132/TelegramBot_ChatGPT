import settings
import csv
import openai
import telebot
import re

openai.api_key= settings.OPENAI_API_KEY
bot = telebot.TeleBot(settings.BOT_API_KEY)
  


@bot.message_handler(commands=['help']) 
def help_command(message): 
  bot.send_message(message.chat.id, 
"""Для написания эссе с помощью OpenAI API вам нужно выбрать подходящую модель, начальный текст и параметры генерации. Вот некоторые рекомендации:

Вы можете использовать функцию '/temp' [ваша цифра от 0 до 1] для изменения стиля вашего текста. 

Например, если вы хотите написать более творческое и оригинальное эссе, вы можете увеличить значение temperature с помощью (например, до 0.7 или 0.8). 

Если вы хотите написать более формальное и академическое эссе, вы можете уменьшить значение temperature (например, до 0.3 или 0.4).
""")

temp = 0.7
# Define a command handler to change the temperature
@bot.message_handler(commands=['temp'])
def change_temp(message):
  try:
    # Get the new temperature value from the message text
    new_temp = message.text.split()[1]
    if 0 <= float(new_temp) <= 1:
      global temp
      temp = float(new_temp)
      bot.send_message(message.chat.id, f"Temperature changed to {temp}")
    else:
      # Send an error message to the user
      bot.send_message(message.chat.id, "Invalid temperature value. Please enter a number between 0 and 1.")
  except:
    bot.send_message(message.chat.id, "Something went wrong. Please make sure you enter a valid command and a number between 0 and 1.")
    

@bot.message_handler(func=lambda _:True)
def handle_message(message):
  response = openai.Completion.create(
  model="text-davinci-003",
  prompt=message.text, 
  temperature=temp,       #степень случайности текста
  max_tokens=1000,        #максимум токенов
  top_p=1,                #вероятность выбора следующего слова (0 - только самое вероятное слово)
  frequency_penalty=0.0,  #штраф за повторяющиеся слова
  presence_penalty=0.6,   #штраф за повторяющиеся слова по всему тексту
  stop=[" Human:", " AI:"]#список слов для конца генерации
)
  # bot.send_message(chat_id=message.from_user.id,text ="temp ="+str(temp))
  bot.send_message(chat_id=message.from_user.id,text=response['choices'][0]['text'])


  with open("private/messages.csv", "a") as file:
    Response = re.sub(r"\n+", "", response['choices'][0]['text'])
    writer = csv.writer(file)
    writer.writerow([message.text, Response])
    print(message.from_user.first_name + ': ' + message.text + '\n')
    print('TeleBotAI: '+Response+'\n')
    file.close()

bot.polling()


