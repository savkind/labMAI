import subprocess

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import requests
from config import token
import zipfile
import os
import shlex
from subprocess import *

bot = Bot(token=token)
dp = Dispatcher(bot)

def processing_zip(ref):
    r = requests.get(ref, allow_redirects=True)
    open("object.zip", "wb").write(r.content)
    z = zipfile.ZipFile('object.zip', 'r')
    path = z.filelist[0].filename.rpartition('/')[0]
    z.extractall()
    z.close()
    compile_file(path)

def compile_file(path):
    curdir = os.getcwd() + '\\' + path
    os.chdir(curdir)
    full_dir = os.listdir(curdir)
    cFileList = ""
    for file in full_dir:
        if (file.find('.c') != -1):
            print("файл найден", file)
            cFileList += file + " "
    os.system(f"gcc {cFileList} -o prog")





@dp.message_handler()
async def echo_message(msg: types.Message):
    text = "Вы отправили ссылку на GitHub - " + msg.text
    await bot.send_message(msg.from_user.id, text)
    processing_zip(msg.text)



async def sent_hello(dp):
    await bot.send_message(chat_id=967676469,text="Бот запущен")


if __name__ == '__main__':
    executor.start_polling(dp,on_startup=sent_hello)