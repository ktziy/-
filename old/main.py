# -- coding: utf-8 --**
from telegram import ParseMode
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import create_deep_linked_url
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from telegram.ext.updater import Updater
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import re
import os
import json
import asyncio
from telegram.ext import Filters,MessageHandler,CallbackQueryHandler,PreCheckoutQueryHandler,ShippingQueryHandler
from telegram import LabeledPrice, ShippingOption, Update
from telegram import ChatMemberAdministrator
import time
import random
from group import *

#from elasticsearch import Elasticsearch

class main:
    def __init__(self,token,botname,mainkeyboard):
        def aexec(func):
            def wrapper(update: Update, context: CallbackContext):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(func(update, context))
                loop.close()
            return wrapper
        @aexec
        async def play(update: Update, context: CallbackContext):
            query = update.callback_query
            if query.data == 'buy':
                kb=InlineKeyboardMarkup([
    [InlineKeyboardButton("购买价格✅",callback_data='buy'),InlineKeyboardButton("出售价格",callback_data='sell')],
   ]
    )
            elif query.data=='sell':
                kb=InlineKeyboardMarkup([
    [InlineKeyboardButton("购买价格",callback_data='buy'),InlineKeyboardButton("出售价格✅",callback_data='sell')],
   ]
    )
            query.edit_message_text(usdt.gethuilv(type=query.data),parse_mode='HTML',reply_markup=kb)

        @aexec
        async def start(update: Update, context: CallbackContext):
            _= re.findall(r"(?:/start )(.+)", update.message.text)
            print(_)
            update.message.reply_text(
                '''您好 欢迎使用记账机器人 目前支持以下命令（仅限群组内使用）

<b>【1】 全局命令</b>
先将机器人拉入群聊并设置为管理员 并发送<code>初始化</code>
设置操作人：命令"设置操作人"+空格+用户的telegramid（存在则添加 否则删除）

新增账单：命令"新增账单"+账单名称 

<b>【2】 带账单名称的命令</b>
设置汇率：设置汇率 或 设置实时汇率
查看账单："查看账单"
删除账单："删除账单"
清空账单："清空账单"

出入账：±账单金额 
如 账单1+100

<b>【3】 特别说明</b>
1.固定汇率与实时汇率不可同时设置
2.账单币种为usdt
3.发送z0即可查询实时u价



'''
                ,parse_mode='HTML')

        @aexec
        async def echo(update: Update, context: CallbackContext):
            allow=False
            _= re.findall(r'^T[0-9a-zA-Z]{33}$', update.message.text)
            print(_)
            if '+' in update.message.text or '-' in update.message.text or '*' in update.message.text or '/' in update.message.text:
                try:
                    print(eval(update.message.text))
                    allow=True
                except:
                    pass
                try:
                    print(int(update.message.text))
                    allow=True
                except:
                    allow=False
                update.message.reply_text(str(eval(update.message.text)))

            elif update.message.text =='初始化' and not update.message.from_user.id == update.message.chat_id:
                if ChatMemberAdministrator(user=update.message.from_user.id)['status'] == 'administrator':
                    group.new(groupid=update.message.chat_id,adminlist=[str(update.message.from_user.id)])
                    group.newbook(bookname='',groupid=update.message.chat_id)
                    update.message.reply_text("完成！")
                    pass
                else:
                    update.message.reply_text("您不是管理！")
            elif "设置操作人" in update.message.text and not update.message.from_user.id == update.message.chat_id:
                print(update.message.reply_to_message)
                admin=update.message.text[6:].strip()
                if ChatMemberAdministrator(user=update.message.from_user.id)['status'] == 'administrator':
                    group.change(groupid=update.message.chat_id,adminid=str(admin))
                    update.message.reply_text("完成！")
                    pass
                else:
                    update.message.reply_text("您不是管理！")
            elif "新增账单" in update.message.text and not update.message.from_user.id == update.message.chat_id:
                bookname=update.message.text[4:].strip()
                if group.userinadmin(adminid=update.message.from_user.id,groupid=update.message.chat_id):
                    group.newbook(bookname=bookname,groupid=update.message.chat_id)
                    update.message.reply_text("账单新建完成！\n您可以发送 查看{} 获取账单详情 \n或发送账单名称+汇率方式（实时汇率或固定汇率xx）".format(bookname))
            if "+" in update.message.text and not update.message.from_user.id == update.message.chat_id and allow:
                bookname=update.message.text.split('+')[0]
                if group.isbookin(groupid=update.message.chat_id,bookname=bookname):
                    if group.userinadmin(adminid=update.message.from_user.id,groupid=update.message.chat_id):
                        feelv=group.getfeelv(groupid=update.message.chat_id,bookname=bookname)
                        group.write(type='入款',bookname=bookname,groupid=update.message.chat_id,score=float(update.message.text.split('+')[1].strip())*(1-feelv))
                        more=group.more(groupid=update.message.chat_id,bookname=bookname)
                        load=group.load(groupid=update.message.chat_id,bookname=bookname)
                        plist=load['pay_text'].split('\n')
                        lp=''
                        i=0
                        print(plist[0])
                        while len(plist) > 1 and i <3:
                            print(i)
                            lp+='{}\n'.format(plist[0])
                            i+=1
                            plist.remove(plist[0])
                        glist=load['get_text'].split('\n')
                        lg=''
                        i=0
                        while len(glist) > 1 and i <3:
                            print(i)
                            lg+='{}\n'.format(glist[0])
                            i+=1
                            glist.remove(glist[0])
                        huilv=group.gethuilv(groupid=update.message.chat_id,bookname=bookname)
                        update.message.reply_text("<b>账单写入完成！</b>\n\n<b>最近入款</b>\n<code>{}</code>\n<b>最近放款</b>\n<code>{}</code>\n\n<b>累计放款：</b>{}\n<b>累计入账：</b>{}\n<b>当前汇率：</b>{}\n<b>费率：</b>{}"
                                                  .format(lg,lp,more['累计放款'],more['累计入款'],huilv,feelv),
                                                  parse_mode='HTML')
                    else:
                        update.message.reply_text("您不是管理！")
                else:
                    update.message.reply_text("{},此账单不存在".format(bookname))
            elif "-" in update.message.text and not update.message.from_user.id == update.message.chat_id and allow:
                bookname=update.message.text.split('-')[0]
                if group.isbookin(groupid=update.message.chat_id,bookname=bookname):
                    if group.userinadmin(adminid=update.message.from_user.id,groupid=update.message.chat_id):
                        feelv=group.getfeelv(groupid=update.message.chat_id,bookname=bookname)
                        group.write(type='放款',bookname=bookname,groupid=update.message.chat_id,score=float(update.message.text.split('-')[1].strip()))
                        more=group.more(groupid=update.message.chat_id,bookname=bookname)
                        load=group.load(groupid=update.message.chat_id,bookname=bookname)
                        plist=load['pay_text'].split('\n')
                        lp=''
                        i=0
                        print(plist[0])
                        while len(plist) > 1 and i <3:
                            print(i)
                            lp+='{}\n'.format(plist[0])
                            i+=1
                            plist.remove(plist[0])
                        glist=load['get_text'].split('\n')
                        lg=''
                        i=0
                        while len(glist) > 1 and i <3:
                            print(i)
                            lg+='{}\n'.format(glist[0])
                            i+=1
                            glist.remove(glist[0])
                        huilv=group.gethuilv(groupid=update.message.chat_id,bookname=bookname)
                        update.message.reply_text("<b>账单写入完成！</b>\n\n<b>最近入款</b>\n<code>{}</code>\n<b>最近放款</b>\n<code>{}</code>\n\n<b>累计放款：</b>{}\n<b>累计入账：</b>{}\n<b>当前汇率：</b>{}\n<b>费率：</b>{}"
                                                  .format(lg,lp,more['累计放款'],more['累计入款'],huilv,feelv),
                                                  parse_mode='HTML')
                    else:
                        update.message.reply_text("您不是管理！")
                else:
                    update.message.reply_text("{},此账单不存在".format(bookname))
            elif "入款" in update.message.text and not update.message.from_user.id == update.message.chat_id:
                bookname=update.message.text.split('入款')[0]
                if group.isbookin(groupid=update.message.chat_id,bookname=bookname):
                    feelv=group.getfeelv(groupid=update.message.chat_id,bookname=bookname) 
                    if group.userinadmin(adminid=update.message.from_user.id,groupid=update.message.chat_id):
                        group.write(type='入款',bookname=bookname,groupid=update.message.chat_id,score=float(update.message.text.split('入款')[1].strip())*(1-feelv))
                        more=group.more(groupid=update.message.chat_id,bookname=bookname)
                        load=group.load(groupid=update.message.chat_id,bookname=bookname)
                        plist=load['pay_text'].split('\n')
                        lp=''
                        i=0
                        print(plist[0])
                        while len(plist) > 1 and i <3:
                            print(i)
                            lp+='{}\n'.format(plist[0])
                            i+=1
                            plist.remove(plist[0])
                        glist=load['get_text'].split('\n')
                        lg=''
                        i=0
                        while len(glist) > 1 and i <3:
                            print(i)
                            lg+='{}\n'.format(glist[0])
                            i+=1
                            glist.remove(glist[0])
                        huilv=group.gethuilv(groupid=update.message.chat_id,bookname=bookname)
                        update.message.reply_text("<b>账单写入完成！</b>\n\n<b>最近入款</b>\n<code>{}</code>\n<b>最近放款</b>\n<code>{}</code>\n\n<b>累计放款：</b>{}\n<b>累计入账：</b>{}\n<b>当前汇率：</b>{}\n<b>费率：</b>{}"
                                                  .format(lg,lp,more['累计放款'],more['累计入款'],huilv,feelv),
                                                  parse_mode='HTML')
                    else:
                        update.message.reply_text("您不是管理！")
                else:
                    update.message.reply_text("{},此账单不存在".format(bookname))
            elif "下发" in update.message.text and not update.message.from_user.id == update.message.chat_id:
                bookname=update.message.text.split('下发')[0]
                if group.isbookin(groupid=update.message.chat_id,bookname=bookname):
                    if group.userinadmin(adminid=update.message.from_user.id,groupid=update.message.chat_id):
                        feelv=group.getfeelv(groupid=update.message.chat_id,bookname=bookname)
                        huilv=group.gethuilv(groupid=update.message.chat_id,bookname=bookname)
                        group.write(type='放款',bookname=bookname,groupid=update.message.chat_id,score=float(update.message.text.split('下发')[1].strip()))
                        more=group.more(groupid=update.message.chat_id,bookname=bookname)
                        load=group.load(groupid=update.message.chat_id,bookname=bookname)
                        plist=load['pay_text'].split('\n')
                        lp=''
                        i=0
                        print(plist[0])
                        while len(plist) > 1 and i <3:
                            print(i)
                            lp+='{}\n'.format(plist[0])
                            i+=1
                            plist.remove(plist[0])
                        glist=load['get_text'].split('\n')
                        lg=''
                        i=0
                        while len(glist) > 1 and i <3:
                            print(i)
                            lg+='{}\n'.format(glist[0])
                            i+=1
                            glist.remove(glist[0])
                        huilv=group.gethuilv(groupid=update.message.chat_id,bookname=bookname)
                        update.message.reply_text("<b>账单写入完成！</b>\n\n<b>最近入款</b>\n<code>{}</code>\n<b>最近放款</b>\n<code>{}</code>\n\n<b>累计放款：</b>{}\n<b>累计入账：</b>{}\n<b>当前汇率：</b>{}\n<b>费率：</b>{}"
                                                  .format(lg,lp,more['累计放款'],more['累计入款'],huilv,feelv),
                                                  parse_mode='HTML')
                    else:
                        update.message.reply_text("您不是管理！")
                else:
                    update.message.reply_text("{},此账单不存在".format(bookname))
            elif "显示账单" in update.message.text and not update.message.from_user.id == update.message.chat_id:
                bookname=update.message.text[4:].strip()
                if group.isbookin(groupid=update.message.chat_id,bookname=bookname):
                    if group.userinadmin(adminid=update.message.from_user.id,groupid=update.message.chat_id):
                        more=group.more(groupid=update.message.chat_id,bookname=bookname)
                        load=group.load(groupid=update.message.chat_id,bookname=bookname)
                        lp=load['pay_text']
                        lg=load['get_text']
                        update.message.reply_text("账单详情如下！\n所有入款\n{}\n所有放款\n{}\n\n累计放款：{}\n累计入账：{}\n汇率：{}\n费率：{}".format(lg,lp,more['累计放款'],more['累计入款'],more['汇率'],more['费率']))
                    else:
                        update.message.reply_text("您不是管理！")
                else:
                    update.message.reply_text("{},此账单不存在".format(bookname))
            elif "设置汇率" in update.message.text and not update.message.from_user.id == update.message.chat_id and len(update.message.text)==4:
                huilv=float(update.message.text.split('设置汇率')[1])
                bookname=update.message.text.split('设置汇率')[0]
                if group.isbookin(groupid=update.message.chat_id,bookname=bookname):
                    if group.userinadmin(adminid=update.message.from_user.id,groupid=update.message.chat_id):
                        group.sethuilv(groupid=update.message.chat_id,bookname=bookname,huilv=huilv)
                        update.message.reply_text("<b>更改完成 当前汇率:</b><code>{}</code>".format(huilv),parse_mode='HTML')
                    else:
                        update.message.reply_text("您不是管理！")
                else:
                    update.message.reply_text("{},此账单不存在".format(bookname))
            elif "设置实时汇率" == update.message.text and not update.message.from_user.id == update.message.chat_id:
                huilv='timer'
                bookname=update.message.text.split('设置实时汇率')[0]
                if group.isbookin(groupid=update.message.chat_id,bookname=bookname):
                    if group.userinadmin(adminid=update.message.from_user.id,groupid=update.message.chat_id):
                        group.sethuilv(groupid=update.message.chat_id,bookname=bookname,huilv=huilv)
                        update.message.reply_text("更改完成 当前汇率{}".format(group.gethuilv(groupid=update.message.chat_id,bookname=bookname)))
                    else:
                        update.message.reply_text("您不是管理！")
                else:
                    update.message.reply_text("{},此账单不存在".format(bookname))
            elif "设置费率" in update.message.text and not update.message.from_user.id == update.message.chat_id:
                feelv=float(update.message.text.split('设置费率')[1].strip('%'))/100
                bookname=update.message.text.split('设置费率')[0]
                if group.isbookin(groupid=update.message.chat_id,bookname=bookname):
                    if group.userinadmin(adminid=update.message.from_user.id,groupid=update.message.chat_id):
                        group.setfeelv(groupid=update.message.chat_id,bookname=bookname,feelv=feelv)
                        update.message.reply_text("更改完成 当前费率{}".format(feelv))
                    else:
                        update.message.reply_text("您不是管理！")
                else:
                    update.message.reply_text("{},此账单不存在".format(bookname))
            elif len(_) ==1:
                msg=usdt.query(address=_[0])
                update.message.reply_text("USDT余额：{}\nTRX余额：{}\n转出总数：{}\n转入总数：{}".format(msg['usdt余额'],msg['trx余额'],msg['所有转出'],msg['所有转入']))
            elif update.message.text=='实时汇率' or update.message.text=='z0' or update.message.text=='Z0':
                update.message.reply_text(text=usdt.huilv(type='buy'),parse_mode='HTML',reply_markup=InlineKeyboardMarkup([
    [InlineKeyboardButton("购买价格✅",callback_data='buy'),InlineKeyboardButton("出售价格",callback_data='sell')],
   ]
    ))

        token = token
        time.sleep(0.1)
        updater = Updater(token=token,use_context=True,request_kwargs={'proxy_url':'socks5h://127.0.0.1:7890'})
        dispatch = updater.dispatcher

        updater.dispatcher.add_handler(CallbackQueryHandler(play, run_async=True))
        updater.dispatcher.add_handler(CommandHandler('start', start, run_async=True))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, echo, run_async=True))
        updater.start_polling()
        updater.idle()
main(token="6117771122:AAGJGVsqc8eW59IbNvuUPmdPA9a-k_f6Kls",
    botname='cnpornbot',
    mainkeyboard=
    InlineKeyboardMarkup([
    [InlineKeyboardButton("官方频道",url='t.me/ilovedudu'),InlineKeyboardButton("官方群组",url='t.me/sgkdudu')],
   ]
    )
    )    
