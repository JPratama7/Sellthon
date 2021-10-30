import os

from telebot import TeleBot
from telebot import types
from dotenv import load_dotenv
from lib import *
# Global Variable
load_dotenv(".env")
TOKEN = os.getenv("API")
bot = TeleBot(TOKEN)

user_dict = {}

class User:
    def __init__(self, teleg_id):
        self.teleg_id = int(teleg_id)
        self.nama = None
        self.alamat = None

@bot.message_handler(commands=['daftar'])
def send_welcome(message):
    chat_id = int(message.chat.id)
    cursor = create_cursor()
    try:
        cursor.execute(f"SELECT tele_id FROM user WHERE tele_id={chat_id}")
        data = cursor.fetchone()
        if data != None:
            bot.reply_to(message,"Anda sudah terdaftar")
        else:
            msg = bot.reply_to(message, """\
        Silahkan jawab pertanyaan sesuai data diri.\nNama:
        """)
            bot.register_next_step_handler(msg, nama)
        cursor.close()
    except Exception as e:
        logfunc("cursor error", e)
        

def nama(message):
    try:
        chat_id = message.chat.id
        nama = message.text
        user = User(chat_id)
        user_dict[chat_id] = user
        user.nama = nama
        msg = bot.reply_to(message, 'Alamat?')
        bot.register_next_step_handler(msg, alamat)
    except Exception as e:
        logfunc('nama',e)
        bot.reply_to(message, 'oooops terjadi error silahkan lapor ke admin')


def alamat(message):
    try:
        chat_id = message.chat.id
        alamat = message.text
        user = user_dict[chat_id]
        user.alamat = alamat
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('ya', 'tidak')
        msg = bot.reply_to(message, f'Nama: {user.nama}\nAlamat : {user.alamat}', reply_markup=markup)
        bot.register_next_step_handler(msg, commit_to_database)
    except Exception as e:
        logfunc('alamat',e)
        bot.reply_to(message, 'oooops terjadi error silahkan lapor ke admin terjadi error silahkan lapor ke admin')


def commit_to_database(message):
    try:
        chat_id = message.chat.id
        keputusan = message.text
        user = user_dict[chat_id]
        cursor = create_cursor()
        if (keputusan == u'ya'):
            insert = "INSERT INTO user (tele_id,nama,alamat) VALUES (%s,%s,%s)"
            val = (user.teleg_id,user.nama,user.alamat)
            try:
                cursor.execute(insert,val)
                bot.send_message(chat_id,"ok data sudah terinput")
            except Exception as e:
                bot.send_message(chat_id,"terjadi error silahkan ulang kembali")
                logfunc('commit database', e)
        else:
            bot.send_message(chat_id, "Silahkan tekan -> /daftar untuk melakukan pendaftaran ulang")
        # remove used object at user_dict
        del user_dict[chat_id]
    except Exception as e:
        logfunc('commit database',e)
        bot.reply_to(message, 'oooops terjadi error silahkan lapor ke admin terjadi error silahkan lapor ke admin')
    cursor.close()

#Handler Perintah list
@bot.message_handler(commands=["list"])
def product_list(message):
    try:
        chat_id = message.chat.id
        cursor = create_cursor()
        cursor.execute("SELECT * FROM barang")
        barang = sql.fetchall()
        for x in barang:
            id_barang,nama,harga,stock,gambar=x
            pesan = f"ID barang : {id_barang}\nNama Barang : {nama}\nHarga Barang : Rp. {harga}\nKetersediaan barang: {stock}"
            bot.send_photo(chat_id=chat_id, photo=gambar,caption=pesan)
    except Exception as e:
        logfunc('list', e)
        bot.send_message(chat_id=chat_id,text='oooops terjadi error silahkan lapor ke admin')
    cursor.close()

#handler  orderlist
@bot.message_handler(commands=["orderlist"])
def orderlist(message):
    tele_id = int(message.chat.id)
    cursor = create_cursor()
    try:
        cursor.execute("SELECT list_order.id_order,user.nama,barang.nama,list_order.total,list_order.jmlh,list_order.created_at FROM list_order INNER JOIN user ON list_order.tele_id = user.tele_id INNER JOIN barang ON list_order.barang = barang.id_barang WHERE list_order.tele_id = %s" % (tele_id))
        data = cursor.fetchall()
        if len(data) != 0:
            full_list = []
            for datauser in data:
                id_order, nama_user,nama_barang,total,jmlah,tanggal = datauser
                pesan = f"ID ORDER = {id_order}\nNama User = {nama_user}\nNama Barang = {nama_barang}\nTotal Pembelian = {total}\nJumlah Pembelian = {jmlah}\nTanggal Pemesanan = {tanggal}\n"
                full_list.append(pesan)
            msg = '\n'.join(data)
            bot.send_message(tele_id,msg)
        else:
            bot.send_message(tele_id,"belum melakukan pesanan")
    except Exception as e:
        bot.send_message(chat_id, 'terjadi error silahkan lakukan perintah kembali')
    cursor.close()

print("bot berlari")
bot.infinity_polling()