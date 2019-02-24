import discord
import requests
import json
import datetime
import asyncio


def Stage_Get():
    url = "https://spla2.yuu26.com/schedule"
    headers = {"User-Agent": "LiSplAtoon-Bot/ver0.1(twitter@kuzukawa_lisa)"}
    response = requests.get(url, headers=headers)
    dic = json.loads(response.text)
    dic = dic['result']

    url = "https://spla2.yuu26.com/coop/schedule"
    headers = {"User-Agent": "LiSplAtoon-Bot/ver0.1(twitter@kuzukawa_lisa)"}
    response = requests.get(url, headers=headers)
    dic_coop = json.loads(response.text)
    dic_coop = dic_coop['result']

    coop_now = dic_coop[0]
    coop_next = dic_coop[1]

    held_time = coop_now["start"]
    held_time = held_time.replace("T", " ")
    held_time = datetime.datetime.strptime(held_time, '%Y-%m-%d %H:%M:%S')
    held_now = datetime.datetime.now()
    held_now = held_now + datetime.timedelta(hours=9)

    if held_now >= held_time:
        held = '開催中'
        held_next = '次回'
    else:
        held = '次回'
        held_next = 'その次'

    coop_now_weapons = coop_now["weapons"]
    coop_next_weapons = coop_next["weapons"]
    coop_now_send = '【' + coop_now["stage"]["name"] + '】\n' + coop_now["start"].replace("T", " ") + 'から　　　\n' + coop_now["end"].replace(
        "T", " ") + 'まで\n' + '▲▽支給ブキ▽▲' + '\n・' + coop_now_weapons[0]["name"] + '\n・' + coop_now_weapons[1]["name"] + '\n・' + coop_now_weapons[2]["name"] + '\n・' + coop_now_weapons[3]["name"] + '\n'
    coop_next_send = '【' + coop_next["stage"]["name"] + '】\n' + coop_next["start"].replace("T", " ") + 'から\n' + coop_next["end"].replace(
        "T", " ") + 'まで\n' + '▲▽支給ブキ▽▲' + '\n・' + coop_next_weapons[0]["name"] + '\n・' + coop_next_weapons[1]["name"] + '\n・' + coop_next_weapons[2]["name"] + '\n・' + coop_next_weapons[3]["name"] + '\n'

    regular = dic["regular"]
    regular_now = regular[0]
    regular_next = regular[1]
    regular_now_send = '【' + regular_now["rule"] + '】\n-' + regular_now["maps"][0] + '\n-' + regular_now["maps"][1] + \
        '\n' + regular_now["start"].replace("T", " ") + 'から　　　\n' + \
        regular_now["end"].replace("T", " ") + 'まで\n'
    regular_next_send = '【' + regular_next["rule"] + '】\n-' + regular_next["maps"][0] + '\n-' + regular_next["maps"][1] + \
        '\n' + regular_next["start"].replace("T", " ") + 'から\n' + \
        regular_next["end"].replace("T", " ") + 'まで\n'

    gachi = dic["gachi"]
    gachi_now = gachi[0]
    gachi_next = gachi[1]
    gachi_now_send = '【' + gachi_now["rule"] + '】\n-' + gachi_now["maps"][0] + '\n-' + gachi_now["maps"][1] + \
        '\n' + gachi_now["start"].replace("T", " ") + 'から　　　\n' + \
        gachi_now["end"].replace("T", " ") + 'まで\n'
    gachi_next_send = '【' + gachi_next["rule"] + '】\n-' + gachi_next["maps"][0] + '\n-' + gachi_next["maps"][1] + \
        '\n' + gachi_next["start"].replace("T", " ") + 'から\n' + \
        gachi_next["end"].replace("T", " ") + 'まで\n'

    league = dic["league"]
    league_now = league[0]
    league_next = league[1]
    league_now_send = '【' + league_now["rule"] + '】\n-' + league_now["maps"][0] + '\n-' + league_now["maps"][1] + \
        '\n' + league_now["start"].replace("T", " ") + 'から　　　\n' + \
        league_now["end"].replace("T", " ") + 'まで\n'
    league_next_send = '【' + league_next["rule"] + '】\n-' + league_next["maps"][0] + '\n-' + league_next["maps"][1] + \
        '\n' + league_next["start"].replace("T", " ") + 'から\n' + \
        league_next["end"].replace("T", " ") + 'まで\n'

    return [held, coop_now_send, held_next, coop_next_send, regular_now_send, regular_next_send, gachi_now_send, gachi_next_send, league_now_send, league_next_send]


client = discord.Client()


@client.event
async def on_ready():
    print('login_OK')
    print('{0.user}'.format(client))
    print(client.user.id)
    print('------------------------')
    next_send = "2019-02-24 21:00:00"
    next_send = datetime.datetime.strptime(next_send, '%Y-%m-%d %H:%M:%S')
    asyncio.ensure_future(send_mes(next_send))


async def send_mes(next_send):
    channel = client.get_channel(548139776641990697)
    while True:
        now = datetime.datetime.now()
        now = now + datetime.timedelta(hours=9)

        if now >= next_send:
            next_send = next_send + datetime.timedelta(hours=2)
            print(next_send)

            while True:
                try:
                    stages = Stage_Get()
                    break
                except:
                    print("StageGet Retry")

            send_now = datetime.datetime.now()
            send_now = send_now + datetime.timedelta(hours=9)
            send_now = str(send_now.hour) + "時のステージ変更です！\n"
            await channel.send(send_now)
            embed = discord.Embed(title="サーモンラン", color=0xffff00)
            embed.add_field(name=stages[0], value=stages[1])
            embed.add_field(name=stages[2], value=stages[3])
            await channel.send(embed=embed)
            embed = discord.Embed(title="レギュラーマッチ", color=0x00ff00)
            embed.add_field(name="現在", value=stages[4])
            embed.add_field(name="次回", value=stages[5])
            await channel.send(embed=embed)
            embed = discord.Embed(title="ガチマッチ", color=0xff8c00)
            embed.add_field(name="現在", value=stages[6])
            embed.add_field(name="次回", value=stages[7])
            await channel.send(embed=embed)
            embed = discord.Embed(title="リーグマッチ", color=0xff00ff)
            embed.add_field(name="現在", value=stages[8])
            embed.add_field(name="次回", value=stages[9])
            await channel.send(embed=embed)

        await asyncio.sleep(10)

client.run('NTQ3Mzg3NzQwNDQyOTg0NDQ4.D02COQ.SRT1fXlvKs-CaXBe6uUNqo0NuDE')
