import os
import telebot
import schedule
import threading
import time
from config import BOT_TOKEN, DB_PATH
from database import Database
from bot_handlers import BotHandlers

bot = telebot.TeleBot(BOT_TOKEN)
db = Database(DB_PATH)

bot_handlers = BotHandlers(bot, db)
bot_handlers.register_handlers()

def schedule_daily_update():
    schedule.every().day.at("00:00").do(daily_update)

def daily_update():
    current_date = time.strftime("%Y-%m-%d")
    leaders = db.execute_query('SELECT username, points FROM users_points ORDER BY points DESC LIMIT 10')
    leaders_text = "\n".join([f"{i+1}. @{leader[0]}: {leader[1]} яблок" for i, leader in enumerate(leaders)])
    db.execute_update('REPLACE INTO leaderboard (date, leaders) VALUES (?, ?)', (current_date, leaders_text))
    print(f"Leaderboard updated for {current_date}")

def run_scheduler():
    print("Scheduler started...")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()
    bot.polling(none_stop=True)




