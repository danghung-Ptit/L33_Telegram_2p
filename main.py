import schedule
from time import sleep
from telegram import Bot
import requests
import yaml
import asyncio

    
with open("/app/config.yml", "r") as ymlfile:
    try:
        cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)
    except yaml.YAMLError as e:
        print("Lỗi khi mở file config.yml:", e)
        cfg = None


if cfg:
    try:
        TELEGRAM_BOT_TOKEN_Infinity2pW3_Bot = cfg['telethon']['TELEGRAM_BOT_TOKEN_Infinity2pW3_Bot']
        TELEGRAM_CHAT_ID_Javis_2p_w3_Online = cfg['telethon']['TELEGRAM_CHAT_ID_Javis_2p_w3_Online']
        TELEGRAM_CHAT_ID_Javis_2p_w3 = cfg['telethon']['TELEGRAM_CHAT_ID_Javis_2p_w3']
        TELEGRAM_CHAT_ID_Javis_2p_w3_Online_vip = cfg['telethon']['TELEGRAM_CHAT_ID_Javis_2p_w3_Online_vip']
    except KeyError as e:
        print("Không tìm thấy key trong file config.yml:", e)
        TELEGRAM_BOT_TOKEN_Infinity2pW3_Bot = None
        TELEGRAM_CHAT_ID_Javis_2p_w3_Online = None
        TELEGRAM_CHAT_ID_Javis_2p_w3 = None
        TELEGRAM_CHAT_ID_Javis_2p_w3_Online_vip = None
else:
    TELEGRAM_BOT_TOKEN_Infinity2pW3_Bot = None
    TELEGRAM_CHAT_ID_Javis_2p_w3_Online = None
    TELEGRAM_CHAT_ID_Javis_2p_w3 = None
    TELEGRAM_CHAT_ID_Javis_2p_w3_Online_vip = None
    



def get_data():
    url = 'http://123.30.234.209:9000/predict_MB2p'
    data = {
        'username': 'sT8t5JJM',
        'password': 'u2K%qW'
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Lỗi yêu cầu HTTP:", e)
        return None
    except requests.exceptions.JSONDecodeError as e:
        print("Lỗi phân tích phản hồi JSON:", e)
        return None
    except Exception as e:
        print("Lỗi không xác định:", e)
        return None
    
    
    
async def send_notification(notification_message, chat_id):
    if not TELEGRAM_BOT_TOKEN_Infinity2pW3_Bot:
        print("Không tìm thấy khóa API Telegram trong file config.yml.")
        return
    
    telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN_Infinity2pW3_Bot)
    try:
        await telegram_bot.send_message(chat_id=chat_id, text=notification_message, parse_mode="Markdown")
    except Exception as e:
        print("Lỗi khi gửi tin nhắn Telegram:", e)


def send_messenger_notification(option, issue, prediction, time, wrong_predictions):
    message = f"MB2\\_{str(issue)[-3:]} {time.split()[1][:5]} | {prediction} - {wrong_predictions}"
    return message


count_big_small_wrong_predictions = 0
count_even_odd_wrong_predictions = 0
wrongs = 3

async def main():
    global count_big_small_wrong_predictions, count_even_odd_wrong_predictions
    await asyncio.sleep(8)
    response = get_data()
    
    if response is None:
        message = f"Lỗi yêu cầu HTTP"
        await send_notification(message, TELEGRAM_CHAT_ID_Javis_2p_w3_Online)
    else:
        big_small_wrong_predictions = response['predict']['big_small']['wrong_predictions']
        even_odd_wrong_predictions = response['predict']['even_odd']['wrong_predictions']
        issue = response['issue']
        big_small_prediction = response['predict']['big_small']['prediction']
        even_odd_prediction = response['predict']['even_odd']['prediction']
        time = response['time']

        point_BS = int(response['point']['big_small'])
        point_EO = int(response['point']['even_odd'])

        if point_BS in [1, 2]:
            if point_BS == 2:
                big_small_prediction_vip1 = big_small_prediction
            elif big_small_prediction == "Small":
                big_small_prediction_vip1 = "Big"
            elif big_small_prediction == "Big":
                big_small_prediction_vip1 = "Small"

            messagevip1_BS = f"MB2\\_{str(issue)[-3:]} {time.split()[1][:5]} | {point_BS} | {big_small_prediction_vip1} | {big_small_prediction}"
            await send_notification(messagevip1_BS, TELEGRAM_CHAT_ID_Javis_2p_w3_Online_vip)

        if point_EO in [1, 2]:
            if point_EO == 2:
                even_odd_prediction_vip1 = even_odd_prediction
            elif even_odd_prediction == "Even":
                even_odd_prediction_vip1 = "Odd"
            elif even_odd_prediction == "Odd":
                even_odd_prediction_vip1 = "Even"


            messagevip1_EO = f"MB2\\_{str(issue)[-3:]} {time.split()[1][:5]} | {point_EO} | {even_odd_prediction_vip1} | {even_odd_prediction}"
            await send_notification(messagevip1_EO, TELEGRAM_CHAT_ID_Javis_2p_w3_Online_vip)

        message = f"MB2\\_{str(issue)[-3:]} {time.split()[1][:5]} | {big_small_prediction}-{big_small_wrong_predictions} | {even_odd_prediction}-{even_odd_wrong_predictions}"
    
        await send_notification(message, TELEGRAM_CHAT_ID_Javis_2p_w3_Online)
    
        if big_small_wrong_predictions >= wrongs:
            count_big_small_wrong_predictions = big_small_wrong_predictions
            notification_message = send_messenger_notification("bigSmall", issue, big_small_prediction, time, big_small_wrong_predictions)
            await send_notification(notification_message, TELEGRAM_CHAT_ID_Javis_2p_w3)
        elif big_small_wrong_predictions == 0 and count_big_small_wrong_predictions >= wrongs:
            notification_message = f"MB2\\_{str(int(issue) - 1)[-3:]} BS | *WIN - {count_big_small_wrong_predictions - wrongs}*"
            count_big_small_wrong_predictions = 0
            await send_notification(notification_message, TELEGRAM_CHAT_ID_Javis_2p_w3)
    
        if even_odd_wrong_predictions >= wrongs:
            count_even_odd_wrong_predictions = even_odd_wrong_predictions
            notification_message = send_messenger_notification("evenOdd", issue, even_odd_prediction, time, even_odd_wrong_predictions)
            await send_notification(notification_message, TELEGRAM_CHAT_ID_Javis_2p_w3)
        elif even_odd_wrong_predictions == 0 and count_even_odd_wrong_predictions >= wrongs:
            notification_message = f"MB2\\_{str(int(issue) - 1)[-3:]} EO | *WIN - {count_even_odd_wrong_predictions - wrongs}*"
            count_even_odd_wrong_predictions = 0
            await send_notification(notification_message, TELEGRAM_CHAT_ID_Javis_2p_w3)
        
def run_main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

schedule.every().hour.at(":00").do(run_main)
schedule.every().hour.at(":02").do(run_main)
schedule.every().hour.at(":04").do(run_main)
schedule.every().hour.at(":06").do(run_main)
schedule.every().hour.at(":08").do(run_main)
schedule.every().hour.at(":10").do(run_main)
schedule.every().hour.at(":12").do(run_main)
schedule.every().hour.at(":14").do(run_main)
schedule.every().hour.at(":16").do(run_main)
schedule.every().hour.at(":18").do(run_main)
schedule.every().hour.at(":20").do(run_main)
schedule.every().hour.at(":22").do(run_main)
schedule.every().hour.at(":24").do(run_main)
schedule.every().hour.at(":26").do(run_main)
schedule.every().hour.at(":28").do(run_main)
schedule.every().hour.at(":30").do(run_main)
schedule.every().hour.at(":32").do(run_main)
schedule.every().hour.at(":34").do(run_main)
schedule.every().hour.at(":36").do(run_main)
schedule.every().hour.at(":38").do(run_main)
schedule.every().hour.at(":40").do(run_main)
schedule.every().hour.at(":42").do(run_main)
schedule.every().hour.at(":44").do(run_main)
schedule.every().hour.at(":46").do(run_main)
schedule.every().hour.at(":48").do(run_main)
schedule.every().hour.at(":50").do(run_main)
schedule.every().hour.at(":52").do(run_main)
schedule.every().hour.at(":54").do(run_main)
schedule.every().hour.at(":56").do(run_main)
schedule.every().hour.at(":58").do(run_main)


while True:
    schedule.run_pending()
    sleep(1)

    