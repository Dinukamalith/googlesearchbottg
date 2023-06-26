from telegram.ext import Updater, CommandHandler
import requests
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome to the Google Search bot! Send me your search query."
    )

def search(update, context):
    query = update.message.text
    encoded_query = quote_plus(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='yuRUbf')
        if len(results) > 0:
            first_result = results[0]
            title = first_result.find('h3', class_='LC20lb').text
            link = first_result.find('a')['href']
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"{title}\n{link}")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="No results found.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, something went wrong with the search.")

def main():
    updater = Updater(token="6032498675:AAHpZPvPU4YjlXes_G2kKTEGw0XheduiZBM", use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    search_handler = CommandHandler('search', search)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(search_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
