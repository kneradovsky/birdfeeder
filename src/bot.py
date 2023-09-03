import logging
from multiprocessing import Queue
from threading import Thread
from mzmq import ZmqReceiver
import asyncio

from telegram import ForceReply, Update,Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters




# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARN
)
logger = logging.getLogger(__name__)



BOT_TOKEN="6184473978:AAFMkjQWkDy8vaKhpGZwtddb_p4YCg_YMeg"
group_chat_id=-709234685

feeders = {
    "1" : {"name":"Кормушка 1","weight":10,"isEmpty":False},
    "2" : {"name":"Кормушка 2","weight":1,"isEmpty":True},
    "3" : {"name":"Кормушка 3","weight":2,"isEmpty":False},
    "4" : {"name":"Кормушка 4","weight":4,"isEmpty":False},
}

async def start(update: Update, context:ContextTypes.DEFAULT_TYPE) -> None :
    user = update.effective_user
    await update.message.reply_text("Я бот отслеживания наполненности кормушек в Таежном сквере. Если в кормушке кончается корм, то я обязательно тебе об этом скажу")

async def info(update: Update,context:ContextTypes.DEFAULT_TYPE) -> None :
    await update.message.reply_text("В сквере Таёжный можно встретить следующих птиц: воробей, синица, щегол, чиж, зеленушка, сойка, поползень, клест, дятел, дрозд, снегирь, свиристель."+
        "\n\nВ кормушку <b>можно</b> положить: овес, подсолнечник, просо, пшеница. \n<b>Нельзя</b> класть в кормушку: хлеб, колбасные изделия, мясные изделия.",parse_mode="HTML")


def format_feeder_item1(feeder) -> str :
    s = f'В <b>{feeder["name"]}</b> {feeder["weight"]} г. корма.'
    if(feeder["isEmpty"]) : s+=" Она пустая"
    return s


async def list_feed(update:Update,context:ContextTypes.DEFAULT_TYPE) -> None: 
    #print(feeders.values())
    msg = "\n".join([format_feeder_item1(v) for v in feeders.values()])
    await update.message.reply_html(msg)

async def list_empty(update:Update,context:ContextTypes.DEFAULT_TYPE) -> None:
    msg = "\n".join([f'<b>{v["name"]}</b> пустая' for v in feeders.values() if v["isEmpty"]])
    print(update.message.chat.id)
    await update.message.reply_html(msg)


app = Application.builder().token(BOT_TOKEN).build()

def send_message(groupid,msg):
    asyncio.run(Bot(BOT_TOKEN).send_message(groupid,msg,parse_mode="HTML"))
    print("Done send")

def worker(groupid):
    mq = ZmqReceiver()
    print("app="+str(app))
    while True:
        try :
            msg = mq.receive()
            mq.send("ok")
            print(msg)
            parts = msg.split(";")
            feed = feeders[parts[1]]
            if feed is None : 
                print("Invalid feeder number"+parts[1])
                continue
            match parts[0]:
                case "empty":
                    feed["isEmpty"]=True
                    feed["weight"]=0
                    send_message(groupid,f'<b>{feed["name"]}</b> пустая')
                case "refill":
                    feed["isEmpty"]=False
                    feed["weight"]=20
                    send_message(groupid,f'<b>{feed["name"]}</b> снова полная. <b>Спасибо!</b>')
                case "weight":
                    feed["weight"]=parts[2]
                    send_message(groupid,f'В <b>{feed["name"]}</b>  <i>{feed["weight"]}</i> г. корма. <b>Спасибо!</b>')
                case _:
                    print(f'mesage from api: {msg}')            
        except: 
            break

worker_thread = Thread(target=worker,args=(group_chat_id,), daemon=True)


def start_bot() -> Application :
    app.add_handlers(
        [
            CommandHandler("start",start),
            CommandHandler("info",info),
            CommandHandler("list",list_feed),
            CommandHandler("empty",list_empty),
        ]
    )
    worker_thread.start()
    app.run_polling()
    return app