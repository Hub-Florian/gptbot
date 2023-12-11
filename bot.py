import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import Firefox
import socket

import json
import time


bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is ready")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.content[0] != "$":
        return
    all_messages = []
    
    firefox_options = FirefoxOptions()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(options=firefox_options)

    driver.get("https://chat.openai.com/")
    with open("cookies.json", "r") as f:
        data = json.load(f)
    for cookie in data:
        driver.add_cookie(cookie)
    driver.get("https://chat.openai.com/")
    old_nbr_message = len(driver.find_elements(By.XPATH, "//*[@data-message-id]"))
    sentence = message.content[1:] + "réponds en max 50 mots"
    input_elem = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
    input_elem.send_keys(sentence)
    send_button = driver.find_element(By.XPATH, "//*[@data-testid='send-button']")
    send_button.click()
    time.sleep(5)
    message_elements = driver.find_elements(By.XPATH, "//*[@data-message-id]")
    for index, messagegpt in enumerate(message_elements):
        valeur_attribut = messagegpt.get_attribute('data-message-id')
        if valeur_attribut in all_messages:
            continue
        if index % 2 == 0:
            continue
        await message.channel.send(messagegpt.text)
        all_messages.append(valeur_attribut)

if __name__ == "__main__":
    with open("token.json", "r") as f:
        data = json.load(f)
    bot.run(data["token"])
