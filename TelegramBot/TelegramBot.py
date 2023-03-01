import settings
import csv
import openai
import telebot
import re


openai.api_key= settings.OPENAI_API_KEY
bot = telebot.TeleBot(settings.BOT_API_KEY)


@bot.message_handler(func=lambda _:True)
def handle_message(message):
  response = openai.Completion.create(
  model="text-davinci-003",
  prompt=message.text,
  temperature=0.7,
  max_tokens=1000,
  top_p=1,
  frequency_penalty=0.0,
  presence_penalty=0.6,
  stop=[" Human:", " AI:"]
)
  bot.send_message(chat_id=message.from_user.id,text=response['choices'][0]['text'])


  with open("private/messages.csv", "a") as file:
    Response = re.sub(r"\n+", "", response['choices'][0]['text'])
    writer = csv.writer(file)
    writer.writerow([message.text, Response])
    print(message.from_user.first_name + ': ' + message.text + '\n')
    print('TeleBotAI: '+Response+'\n')
    file.close()

bot.polling()


