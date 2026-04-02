import os
import requests
from dotenv import load_dotenv


from openai import OpenAI

load_dotenv()  # load environment variables from .env file
client = OpenAI()  # create an OpenAI client instance
response = client.responses.create(
    model="gpt-5-nano", input="Write a one sentence bedtime story about a unicorn.")
print(response.output_text)




#load_dotenv()  # load environment variables from .env file
#API_KEY = os.getenv('OPENWEATHER_API_KEY')  # get the API key from environment variable

#url = (f'https://api.openweathermap.org/data/2.5/weather'
      # f'?q=Boston&appid={API_KEY}&units=imperial')
#print(url)
#data = requests.get(url).json()
#print(f"Boston: {data['main']['temp']}°F")

