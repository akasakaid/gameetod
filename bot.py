import os
import json
import uuid
import time
import asyncio
import aiofiles
import argparse
import httpx as hatetepe
from datetime import datetime
from colorama import Fore, Style, init
from urllib.parse import parse_qs
from fake_useragent import UserAgent
from base64 import urlsafe_b64decode

init(autoreset=True)
hitam = Fore.LIGHTBLACK_EX
hijau = Fore.LIGHTGREEN_EX
putih = Fore.LIGHTWHITE_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX
merah = Fore.LIGHTRED_EX
reset = Style.RESET_ALL
ungu = Fore.LIGHTMAGENTA_EX
line = putih + "~" * 50


class Config:
    def __init__(
        self,
        countdown,
        interval,
        use_ticket_to_spin,
        max_use_ticket_to_spin,
    ):
        self.countdown = countdown
        self.interval = interval
        self.use_ticket_to_spin = use_ticket_to_spin
        self.max_use_ticket_to_spin = max_use_ticket_to_spin


class GameeTod:
    def __init__(self, query: str, config: Config):
        marin = lambda data: {key: value[0] for key, value in parse_qs(data).items()}
        parser = marin(query)
        user = parser.get("user")
        if user is None:
            self.log(
                f"{merah}There is no user data in your query, \
                    make sure your query is correct!"
            )
            return
        luser = json.loads(user)
        self.id = str(luser.get("id"))
        first_name = luser.get("first_name")
        self.log(f"{hijau}login as {putih}{first_name}")
        self.uuid_file = "gamee_uuid.json"
        self.ua_file = "gamee_useragent.json"
        self.token_file = "gamee_tokens.json"
        self.gamee_url = "https://api.gamee.com/"
        self.query = query
        self.config = config

    @staticmethod
    def log(msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{hitam}[{now}]{reset} {msg}{reset}")

    def is_expired(self, token):
        if token is None:
            return True
        header, payload, sign = token.split(".")
        deload = urlsafe_b64decode(payload + "==")
        jeload = json.loads(deload)
        exp = int(jeload.get("exp", 0))
        now = int(time.time())
        if (now + 300) > exp:
            return True
        return False

    def cv(self, data):
        return data / 1000000

    async def http(self, url, data=None):
        while True:
            try:
                if not os.path.exists("http.log"):
                    await aiofiles.open("http.log", "a")
                logsize = os.path.getsize("http.log")
                if ((logsize / 1024) / 1024) > 1:
                    async with aiofiles.open("http.log", "w") as hw:
                        await hw.write("")
                if data is None:
                    res = await self.ses.get(url)
                elif data == "":
                    res = await self.ses.post(url)
                else:
                    res = await self.ses.post(url, data=data)
                async with aiofiles.open("http.log", "a", encoding="utf-8") as hw:
                    await hw.write(f"{res.text}\n")
                if "<title>" in res.text:
                    self.log(f"{kuning}failed get response json !")
                    await self.countdown(5)
                    continue
                return res
            except (hatetepe.TimeoutException, hatetepe.NetworkError):
                self.log(f"{merah}connection error / connection timeout !")

    async def check_ip(self):
        res = await self.http("https://ipinfo.io/json")
        ip = res.json().get("ip")
        city = res.json().get("city")
        region = res.json().get("region")
        country = res.json().get("country")
        GameeTod.log(f"{hijau}proxy ip : {putih}{ip}")
        GameeTod.log(f"{hijau}city : {putih}{city} | {hijau}country : {putih}{country}")

    async def login(self, tg_data):
        data = {
            "jsonrpc": "2.0",
            "id": "user.authentication.loginUsingTelegram",
            "method": "user.authentication.loginUsingTelegram",
            "params": {"initData": tg_data},
        }
        while True:
            res = await self.http(self.gamee_url, json.dumps(data))
            result = res.json().get("result")
            if result is None:
                self.log(f"{merah}something wrong, check http.log ")
                return False
            self.log(f"{hijau}login {putih}success !")
            access_token = result.get("tokens").get("authenticate")
            return access_token

    async def spin(self):
        daily_get_price = {
            "jsonrpc": "2.0",
            "id": "dailyReward.getPrizes",
            "method": "dailyReward.getPrizes",
            "params": {},
        }
        daily_reward_claim_prize = {
            "jsonrpc": "2.0",
            "id": "dailyReward.claimPrize",
            "method": "dailyReward.claimPrize",
            "params": {},
        }
        buy_spin_using_ticket = {
            "jsonrpc": "2.0",
            "id": "dailyReward.buySpinUsingTickets",
            "method": "dailyReward.buySpinUsingTickets",
            "params": {},
        }

        res = await self.http(
            self.gamee_url,
            json.dumps(daily_get_price),
        )
        result = res.json().get("result")
        if result is None:
            self.log(f"{merah}result is None")
            return False
        daily_reward = result.get("dailyReward")
        daily_spin = daily_reward.get("spinsCountAvailable")
        spin_using_ticket_price = daily_reward.get("dailyRewardBonusSpinsPriceTickets")
        tickets = res.json()["user"]["tickets"]["count"]
        self.log(f"{hijau}available ticket : {putih}{tickets}")
        self.log(f"{hijau}available free spin : {putih}{daily_spin}")
        self.log(
            f"{hijau}price to spin : {putih}{spin_using_ticket_price} {hijau}ticket"
        )
        if daily_spin > 0:
            for i in range(daily_spin):
                res = await self.http(
                    self.gamee_url,
                    json.dumps(daily_reward_claim_prize),
                )
                reward_type = res.json()["result"]["reward"]["type"]
                key = "usdCents" if reward_type == "money" else reward_type
                reward = res.json()["result"]["reward"][key]
                self.log(f"{hijau}reward spin : {putih}{reward} {reward_type}")
        if self.config.use_ticket_to_spin is False:
            return
        self.log(f"{biru}start spin using ticket !")
        while True:
            if tickets < spin_using_ticket_price:
                self.log(f"{kuning}not enough tickets for spin !")
                return
            if spin_using_ticket_price > self.config.max_use_ticket_to_spin:
                self.log(f"{kuning}max using ticket to spin reacted !")
                return
            res = await self.http(
                self.gamee_url,
                json.dumps(buy_spin_using_ticket),
            )
            res = await self.http(
                self.gamee_url,
                json.dumps(daily_reward_claim_prize),
            )
            reward_type = res.json()["result"]["reward"]["type"]
            key = "usdCents" if reward_type == "money" else reward_type
            reward = res.json()["result"]["reward"][key]
            self.log(f"{hijau}reward spin : {putih}{reward} {reward_type}")
            res = await self.http(
                self.gamee_url,
                json.dumps(daily_get_price),
            )
            result = res.json().get("result")
            daily_reward = result.get("dailyReward")
            daily_spin = daily_reward.get("spinsCountAvailable")
            spin_using_ticket_price = daily_reward.get(
                "dailyRewardBonusSpinsPriceTickets"
            )
            tickets = res.json()["user"]["tickets"]["count"]
            self.log(f"{hijau}available ticket : {putih}{tickets}")
            self.log(
                f"{hijau}price to spin : {putih}{spin_using_ticket_price} {hijau}ticket"
            )

    async def claim_mining(self):
        data = {
            "jsonrpc": "2.0",
            "id": "user.getActivities",
            "method": "user.getActivities",
            "params": {"filter": "all", "pagination": {"offset": 0, "limit": 100}},
        }
        res = await self.http(
            self.gamee_url,
            json.dumps(data),
        )
        result = res.json().get("result")
        if result is None:
            self.log(f"{merah}something wrong, check http.log !")
            return False
        activities = result.get("activities")
        for activity in activities:
            activity_id = activity.get("id")
            activity_type = activity.get("type")
            is_claim = activity.get("isClaimed")
            if is_claim:
                continue
            self.log(f"{hijau}activity type {putih}{activity_type}")
            rewards = activity.get("rewards")
            virtual_token = rewards.get("virtualTokens")
            for token in virtual_token:
                name = token["currency"]["ticker"]
                amount = self.cv(token["amountMicroToken"])
                data = {
                    "jsonrpc": "2.0",
                    "id": "user.claimActivity",
                    "method": "user.claimActivity",
                    "params": {"activityId": activity_id},
                }
                res = await self.http(
                    self.gamee_url,
                    json.dumps(data),
                )
                if res.status_code != 200:
                    self.log(f"{merah}claim mining reward failure !")
                    continue
                self.log(f"{putih}claim mining reward {hijau}successfully !")
                self.log(f"{hijau}reward {putih}{amount} {hijau} {name}")

    async def mining(self):
        event_id = 26
        data = {
            "jsonrpc": "2.0",
            "id": "miningEvent.get",
            "method": "miningEvent.get",
            "params": {
                "miningEventId": event_id,
            },
        }
        data_start_mining = {
            "jsonrpc": "2.0",
            "id": "miningEvent.startSession",
            "method": "miningEvent.startSession",
            "params": {"miningEventId": event_id},
        }
        data_claim_mining = {
            "jsonrpc": "2.0",
            "id": "miningEvent.claim",
            "method": "miningEvent.claim",
            "params": {
                "miningEventId": event_id,
            },
        }
        res = await self.http(
            self.gamee_url,
            json.dumps(data),
        )
        assets = res.json()["user"]["assets"]
        for asset in assets:
            cur = asset["currency"]["ticker"]
            amount = asset["amountMicroToken"] / 1000000
            self.log(f"{putih}balance : {hijau}{amount} {putih}{cur}")
        mining = res.json()["result"]["miningEvent"]["miningUser"]
        if mining is None:
            self.log(f"{kuning}mining not started !")
            while True:
                res = await self.http(
                    self.gamee_url,
                    json.dumps(data_start_mining),
                )
                if "error" in res.json().keys():
                    time.sleep(2)
                    continue

                if "miningEvent" in res.json()["result"]:
                    self.log(f"{hijau}mining start successfully !")
                    return

        end = mining["miningSessionEnded"]
        earn = self.cv(mining["currentSessionMicroToken"])
        mine = self.cv(mining["currentSessionMicroTokenMined"])
        total_mine = self.cv(mining["cumulativeMicroTokenMined"])
        self.log(f"{putih}total mining : {hijau}{total_mine}")
        self.log(f"{putih}max mining : {hijau}{earn}")
        self.log(f"{putih}current mining : {hijau}{mine}")
        if end:
            self.log(f"{kuning}mining has end !")
            while True:
                res = await self.http(
                    self.gamee_url,
                    json.dumps(data_start_mining),
                )
                result = res.json().get("result")
                error = res.json().get("error")
                if error is not None:
                    msg = error.get("message").lower()
                    if msg == "mining session in progress.":
                        self.log(f"{kuning}mining in progress")
                        return
                    time.sleep(2)
                    continue

                if result.get("miningEvent") is not None:
                    self.log(f"{hijau}mining start successfully !")
                    return

        self.log(f"{kuning}mining is not over !")
        return

    async def start(self, proxy=None):
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en,id-ID;q=0.9,id;q=0.8,en-US;q=0.7",
            "client-language": "en",
            "content-type": "text/plain;charset=UTF-8",
            "Host": "api.gamee.com",
            "Origin": "https://prizes.gamee.com",
            "Referer": "https://prizes.gamee.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "X-Requested-With": "org.telegram.messenger",
        }
        if proxy is None:
            self.ses = hatetepe.AsyncClient()
        else:
            self.ses = hatetepe.AsyncClient(proxy=proxy)
            await self.check_ip()
        self.ses.headers.update(headers)
        if not os.path.exists(self.ua_file):
            async with aiofiles.open(self.ua_file, "w") as w:
                await w.write(json.dumps({}))
        if not os.path.exists(self.token_file):
            async with aiofiles.open(self.token_file, "w") as w:
                await w.write(json.dumps({}))
        if not os.path.exists(self.uuid_file):
            async with aiofiles.open(self.uuid_file, "w") as w:
                await w.write(json.dumps({}))
        async with aiofiles.open(self.ua_file) as uar:
            uas = json.loads(await uar.read())
        async with aiofiles.open(self.uuid_file) as uuidr:
            uuids = json.loads(await uuidr.read())
        async with aiofiles.open(self.token_file) as tokenr:
            tokens = json.loads(await tokenr.read())
        ua = uas.get(self.id)
        if ua is None:
            ua = UserAgent(os=["android", "ios"]).random
            uas[self.id] = ua
            async with aiofiles.open(self.ua_file, "w") as uaw:
                await uaw.write(json.dumps(uas, indent=4))
        uuuid = uuids.get(self.id)
        if uuuid is None:
            uuuid = uuid.uuid4().__str__()
            uuids[self.id] = uuuid
            async with aiofiles.open(self.uuid_file, "w") as uw:
                await uw.write(json.dumps(uuids))
        self.ses.headers["x-install-uuid"] = uuuid
        self.ses.headers["User-Agent"] = ua
        token = tokens.get(self.id)
        if token is None or self.is_expired(token):
            self.log(f"{kuning}token is none or expired !")
            token = await self.login(self.query)
            tokens[self.id] = token
            async with aiofiles.open(self.token_file, "w") as tw:
                await tw.write(json.dumps(tokens, indent=4))
        self.ses.headers["authorization"] = f"Bearer {token}"
        await self.claim_mining()
        await self.spin()
        await self.mining()
        await self.countdown(self.config.interval)

    @staticmethod
    async def countdown(i):
        for i in range(i, 0, -1):
            menit, detik = divmod(i, 60)
            jam, menit = divmod(menit, 60)
            detik = str(detik).zfill(2)
            menit = str(menit).zfill(2)
            jam = str(jam).zfill(2)
            print(f"waiting {jam}:{menit}:{detik} ", flush=True, end="\r")
            await asyncio.sleep(1)


async def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(
        f"""
{ungu}┏┓┳┓┏┓  ┏┓    •         {putih}Auto Script for {kuning}Gamee {putih}/ WAT
{ungu}┗┓┃┃┗┓  ┃┃┏┓┏┓┓┏┓┏╋     {hijau}Author : {putih}AkasakaID
{ungu}┗┛┻┛┗┛  ┣┛┛ ┗┛┃┗ ┗┗     {hijau}Note : {putih}Don't forget to breathe
{ungu}              ┛         {reset}

          """
    )
    arg = argparse.ArgumentParser()
    arg.add_argument("-D", "--data", default="data.txt")
    arg.add_argument("-C", "--config", default="config.json")
    arg.add_argument("-P", "--proxy", default="proxies.txt")
    args = arg.parse_args()
    if not os.path.exists(args.data):
        print(f"{merah}file {putih}{args.data}{merah} is not found !")
        exit()
    if not os.path.exists(args.config):
        print(f"{merah}file {putih}{args.config}{merah} is not found !")
        exit()
    if not os.path.exists(args.proxy):
        print(f"{merah}file {putih}{args.proxy}{merah} is not found !")
        exit()
    async with aiofiles.open(args.data) as dr:
        dread = await dr.read()
        datas = [i for i in dread.splitlines() if len(i) > 10]
    async with aiofiles.open(args.config) as cr:
        cf = await cr.read()
        load = json.loads(cf)
        config = Config(
            load.get("countdown", 300),
            load.get("interval", 3),
            load.get("use_ticket_to_spin", False),
            load.get("max_use_ticket_to_spin", 50),
        )
    use_proxy = False
    async with aiofiles.open(args.proxy) as pr:
        pr = await pr.read()
        proxies = [i for i in pr.splitlines() if len(i) > 0]
        if len(proxies) > 0:
            use_proxy = True
    GameeTod.log(f"{hijau}total account : {putih}{len(datas)}")
    if len(datas) <= 0:
        GameeTod.log(f"{merah}0 Account detected, please input your data first !")
        exit()
    GameeTod.log(f"{hijau}use proxy : {putih}{use_proxy}")
    print(line)
    while True:
        for no, data in enumerate(datas):
            GameeTod.log(f"{hijau}account number : {putih}{no + 1}")
            if use_proxy:
                proxy = proxies[no % len(proxies)]
            else:
                proxy = None
            await GameeTod(data, config).start(proxy)
            print(line)
        await GameeTod.countdown(config.countdown)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        exit()
