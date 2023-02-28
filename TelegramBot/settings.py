import os
import dotenv

dotenv.load_dotenv('.env')

#BOT_API_KEY = os.environ['BOT_API_KEY']
#OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
#print(os.environ['BOT_API_KEY'])

# with open('.env','r') as file:
#     line = file.readline()
#     os.environ[line[:line.find("=")]]=line[line.find("=")+1:]

# print(os.environ['OPENAI_API_KEY'])
# print(os.environ['BOT_API_KEY'])
BOT_API_KEY = os.environ['BOT_API_KEY']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']