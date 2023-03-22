import settings
import csv
import openai
import telebot
import re

openai.api_key= settings.OPENAI_API_KEY
bot = telebot.TeleBot(settings.BOT_API_KEY)
  
# Using /shutdown command
@bot.message_handler(commands=['shutdown'])
def shutdown(message):
  OWNER_ID =922649944
  if message.from_user.id == OWNER_ID: # only allow owner to use this command
    exit()


models = {
    'gpt3.5': 'gpt-3.5-turbo',
    'dav3': 'text-davinci-003'
}

current_model = 'gpt3.5'

@bot.message_handler(commands=['model','Model'])
def change_model(message):
  try:
    global current_model
    new_model = message.text.split()[1]
    if new_model in models:
        current_model = new_model
        bot.send_message(message.chat.id, f"Model switched to {current_model}")
    else:
        bot.send_message(message.chat.id, "Invalid model name. Please enter a valid model name.")
  except:
    bot.send_message(message.chat.id, "Something went wrong. Please make sure you enter a valid command and a number dav3 or gpt3.5")

temp = 0.7
@bot.message_handler(commands=['temp'])
def change_temp(message):
  try:
    new_temp = message.text.split()[1]
    if 0 <= float(new_temp) <= 1:
      global temp
      temp = float(new_temp)
      bot.send_message(message.chat.id, f"Temperature changed to {temp}")
    else:
      bot.send_message(message.chat.id, "Invalid temperature value. Please enter a number between 0 and 1.")
  except:
    bot.send_message(message.chat.id, "Something went wrong. Please make sure you enter a valid command and a number between 0 and 1.")


@bot.message_handler(commands=['help'])
def help(message):
  bot.send_message(message.chat.id, f"""
  У данного бота есть две модели. На данный момент используется {current_model} модель. 
  
  dav3 более слабая языковая модель. Также она не запоминает диалог. gpt3.5 же является моделью, используемой на данный момент в ChatGPT. Также данная модель запоминает диалог, что делает ее незаменимым помошником.
  
  Чтобы поменять модель, введите /model и после нее gpt3.5 или dav3
  
  Для dev3 имеется настройка температуры (/temp) от 0 до 1. Чем больше температура, тем менее формальный текст выдает модель. При высоком значении могут быть фактические ошибки!""")

  
    


messages = [{"role": "system", "content": "Ты - лучший ассистент."},]#Пиши в стиле поцана с района, используя слова-парразиты и ненормативную лексику (можно задать тон разговора для бота)
@bot.message_handler(func=lambda _:True)
def handle_message(message):
  if current_model == 'gpt3.5':
    message_dict = {"role": "user", "content": message.text }
    messages.append(message_dict)
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo", 
      messages=messages
    )
    reply = response.choices[0].message.content #response['choices'][0]['text']
    bot.send_message(chat_id=message.from_user.id,text=reply)
    messages.append({"role": "assistant", "content": reply})
  elif current_model == 'dav3':
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
    reply = response['choices'][0]['text']
    bot.send_message(chat_id=message.from_user.id,text=reply)


  # Код для записи диалогов в файл. Может выдать ошибку при попытке записать спецсимволы или имодзи, поэтому отключил
  # with open("private/messages.csv", "a") as file:
  #   Response = re.sub(r"\n+", "", reply)
  #   writer = csv.writer(file)
  #   writer.writerow([message.text, Response])
  #   print(message.from_user.first_name + ': ' + message.text + '\n')
  #   print('TeleBotAI: '+Response+'\n')
  #   file.close()



bot.polling()


