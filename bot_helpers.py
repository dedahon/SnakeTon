import telebot
from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

def is_user_subscribed(user_id, channel_name):
    try:
        member = bot.get_chat_member(channel_name, user_id)
        return member.status in ["member", "administrator"]
    except Exception as e:
        print(f"Error checking subscription: {str(e)}")
    return False

def add_user_to_subscribed_list(user_id, username, db):
    try:
        result = db.execute_query("SELECT tasks_completed FROM users_points WHERE user_id = ?", (user_id,))
        tasks_completed = result[0][0] if result and result[0][0] else ''
        
        if 'canal' not in tasks_completed:
            new_tasks_completed = tasks_completed + ',canal' if tasks_completed else 'canal'
            db.execute_update("UPDATE users_points SET tasks_completed = ?, points = points + 100 WHERE user_id = ?", 
                              (new_tasks_completed, user_id))
        else:
            print(f"User {user_id} has already subscribed and has 'canal' task completed.")
        
        print(f"User {user_id} has been added to the subscribed list and given 100 points.")
    except Exception as e:
        print(f"Error adding user to subscribed list: {str(e)}")


