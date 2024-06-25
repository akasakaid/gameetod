import os
import sys
import json
import uuid
import time
import argparse
import requests
from colorama import *
from datetime import datetime
from urllib.parse import unquote, quote,parse_qs
from base64 import b64decode

init(autoreset=True)

merah = Fore.LIGHTRED_EX
putih = Fore.LIGHTWHITE_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL
hitam = Fore.LIGHTBLACK_EX


class Gamee:
    def __init__(self):
        self.peer = "gamee"
        self.url_api_gamee = "https://api.service.gameeapp.com/"
        self.ref = "ref_629438076"
        self.DEFAULT_COUNTDOWN = 2 * (60 * 60)
        self.DEFAULT_INTERVAL = 10
        self.line = putih + "~" * 50

    def http(self, url, headers: dict, data=None):
        while True:
            try:
                if data is None:
                    headers["content-length"] = "0"
                    res = requests.get(url, headers=headers)
                    open("http.log", "a", encoding="utf-8").write(
                        res.text + "\n"
                    )
                    if "<html>" in res.text:
                        time.sleep(1)
                        self.log(f"{kuning}failed get json response !")
                        continue
                    return res

                res = requests.post(url, headers=headers, data=data)
                open("http.log", "a", encoding="utf-8").write(res.text + "\n")
                if "<html>" in res.text:
                    time.sleep(1)
                    self.log(f"{kuning}failed get json response !")
                    continue
                return res
            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
            ):
                self.log(f"{merah}connection error !")

    def log(self, message):
        now = now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{hitam}[{now}] {message}")

    def countdown(self, t):
        while t:
            menit, detik = divmod(t, 60)
            jam, menit = divmod(menit, 60)
            jam = str(jam).zfill(2)
            menit = str(menit).zfill(2)
            detik = str(detik).zfill(2)
            print(f"waiting until {jam}:{menit}:{detik} ", flush=True, end="\r")
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")

    def cv(self, data):
        return data / 1000000
    
    def load_config(self,config_file="config.json"):
        try:
            config = json.loads(open(config_file,"r").read())
            self.DEFAULT_COUNTDOWN = config['countdown']
            self.DEFAULT_INTERVAL = config['interval']
            self.USE_TICKET_TO_SPIN = config['use_ticket_to_spin']
            self.MAX_USE_TICKET = config['max_use_ticket_to_spin']
        except json.decoder.JSONDecodeError:
            self.log(f'{merah}failed to get you config, please check {config_file}')
            sys.exit()

    def gamee_login(self, tg_data, uuid):
        data = {
            "jsonrpc": "2.0",
            "id": "user.authentication.loginUsingTelegram",
            "method": "user.authentication.loginUsingTelegram",
            "params": {"initData": tg_data},
        }
        headers = {
            "Host": "api.service.gameeapp.com",
            "Origin": "https://prizes.gamee.com",
            "Referer": "https://prizes.gamee.com/",
            "content-type": "text/plain;charset=UTF-8",
            "content-length": str(len(json.dumps(data))),
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi 4A / 5A Build/QQ3A.200805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.185 Mobile Safari/537.36",
            "x-install-uuid": uuid,
            "X-Requested-With": "org.telegram.messenger",
        }
        while True:
            res = self.http(self.url_api_gamee, headers, json.dumps(data))
            if "result" not in res.json().keys():
                continue

            access_token = res.json()["result"]["tokens"]["authenticate"]
            tokens = json.loads(open("tokens.json", "r").read())
            tokens[uuid] = access_token
            open("tokens.json", "w").write(json.dumps(tokens, indent=4))
            return access_token

    def gamee_spin(self, access_token, uuid):
        headers = {
            "authorization": f"Bearer {access_token}",
            "Host": "api.service.gameeapp.com",
            "Origin": "https://prizes.gamee.com",
            "Referer": "https://prizes.gamee.com/",
            "content-type": "text/plain;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi 4A / 5A Build/QQ3A.200805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.185 Mobile Safari/537.36",
            "x-install-uuid": uuid,
            "X-Requested-With": "org.telegram.messenger",
        }
        daily_get_price = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": "dailyReward.getPrizes",
                "method": "dailyReward.getPrizes",
                "params": {},
            }
        )
        daily_reward_claim_prize = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": "dailyReward.claimPrize",
                "method": "dailyReward.claimPrize",
                "params": {},
            }
        )
        buy_spin_using_ticket = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": "dailyReward.buySpinUsingTickets",
                "method": "dailyReward.buySpinUsingTickets",
                "params": {},
            }
        )
        try:
            res = self.http(self.url_api_gamee, headers, daily_get_price)
            daily_spin = res.json()["result"]["dailyReward"]["spinsCountAvailable"]
            spin_using_ticket_price = res.json()['result']['dailyReward']['dailyRewardBonusSpinsPriceTickets']
            tickets = res.json()['user']['tickets']['count']
            self.log(f'{hijau}available ticket : {putih}{tickets}')
            self.log(f'{hijau}available free spin : {putih}{daily_spin}')
            self.log(f'{hijau}price to spin : {putih}{spin_using_ticket_price} {hijau}ticket')
            if daily_spin > 0:
                for i in range(daily_spin):
                    res = self.http(self.url_api_gamee, headers, daily_reward_claim_prize)
                    reward_type = res.json()["result"]["reward"]["type"]
                    if reward_type == "money":
                        key = "usdCents"
                    else:
                        key = reward_type
                    reward = res.json()["result"]["reward"][key]
                    self.log(f"{hijau}reward spin : {putih}{reward} {reward_type}")

            if self.USE_TICKET_TO_SPIN:
                self.log(f'{biru}start spin using ticket !')
                while True:
                    if tickets < spin_using_ticket_price:
                        self.log(f'{kuning}not enough tickets for spin !')
                        return

                    if spin_using_ticket_price > self.MAX_USE_TICKET:
                        self.log(f'{kuning}max using ticket to spin reacted !')
                        return

                    res = self.http(self.url_api_gamee,headers,buy_spin_using_ticket)
                    res = self.http(self.url_api_gamee,headers,daily_reward_claim_prize)
                    reward_type = res.json()["result"]["reward"]["type"]
                    if reward_type == "money":
                        key = "usdCents"
                    else:
                        key = reward_type
                    reward = res.json()["result"]["reward"][key]
                    self.log(f"{hijau}reward spin : {putih}{reward} {reward_type}")
                    res = self.http(self.url_api_gamee, headers, daily_get_price)
                    daily_spin = res.json()["result"]["dailyReward"]["spinsCountAvailable"]
                    spin_using_ticket_price = res.json()['result']['dailyReward']['dailyRewardBonusSpinsPriceTickets']
                    tickets = res.json()['user']['tickets']['count']
                    self.log(f'{hijau}available ticket : {putih}{tickets}')
                    self.log(f'{hijau}price to spin : {putih}{spin_using_ticket_price} {hijau}ticket')
        except KeyError as e:
            self.log(f'{merah}something error, {e}')
            return False

    def gamee_mining_page(self, access_token, uuid):
        headers = {
            "authorization": f"Bearer {access_token}",
            "Host": "api.service.gameeapp.com",
            "Origin": "https://prizes.gamee.com",
            "Referer": "https://prizes.gamee.com/",
            "content-type": "text/plain;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi 4A / 5A Build/QQ3A.200805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.185 Mobile Safari/537.36",
            "x-install-uuid": uuid,
            "X-Requested-With": "org.telegram.messenger",
        }
        data = {
            "jsonrpc": "2.0",
            "id": "miningEvent.get",
            "method": "miningEvent.get",
            "params": {
                "miningEventId": 7,
            },
        }
        data_start_mining = {
            "jsonrpc": "2.0",
            "id": "miningEvent.startSession",
            "method": "miningEvent.startSession",
            "params": {"miningEventId":11,"code":"watprotocol"},
        }
        res = self.http(self.url_api_gamee, headers, json.dumps(data))
        assets = res.json()["user"]["assets"]
        for asset in assets:
            cur = asset["currency"]["ticker"]
            amount = asset["amountMicroToken"] / 1000000
            self.log(f"{putih}balance : {hijau}{amount} {putih}{cur}")
        mining = res.json()["result"]["miningEvent"]["miningUser"]
        if mining is None:
            self.log(f"{kuning}mining not started !")
            headers["content-length"] = str(len(json.dumps(data_start_mining)))
            while True:
                res = self.http(
                    self.url_api_gamee, headers, json.dumps(data_start_mining)
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
        self.log(f"{putih}max mining : {hijau}{earn}")
        self.log(f"{putih}current mining : {hijau}{mine}")
        if end:
            self.log(f"{kuning}mining has end !")
            headers["content-length"] = str(len(json.dumps(data_start_mining)))
            while True:
                res = self.http(
                    self.url_api_gamee, headers, json.dumps(data_start_mining)
                )
                if "error" in res.json().keys():
                    time.sleep(2)
                    continue

                if "miningEvent" in res.json()["result"]:
                    self.log(f"{hijau}mining start successfully !")
                    return

        self.log(f"{kuning}mining is not over !")
        return

    def data_parsing(self, data):
        return {k: v[0] for k,v in parse_qs(data).items()}

    def token_checker(self, token):
        header, payload, sign = token.split(".")
        depayload = b64decode(payload + "==")
        jeload = json.loads(depayload)
        expired = jeload["exp"]
        now = int(datetime.now().timestamp())
        if now > int(expired):
            return True
        return False

    def main(self):
        banner = f"""
    {hijau}Auto Claim {kuning}WAT Points {hijau}from {biru}Gamee
    
    {putih}By : {hijau}t.me/AkasakaID
    {hijau}Github : {putih}@AkasakaID
    
        """
        arg = argparse.ArgumentParser()
        arg.add_argument('--marinkitagawa',action="store_true")
        arg.add_argument('--data',help="set custom file input data (default: data.txt)",default="data.txt")
        arg.add_argument('--config',help="set custom config (default: config.json)",default="config.json")
        args = arg.parse_args()
        if args.marinkitagawa is False:
            os.system("cls" if os.name == "nt" else "clear")
            
        print(banner)
        
        if not os.path.exists(args.data):
            self.log(f"{merah} {args.data} is not found, input valid path file please !")
            sys.exit()
        
        self.load_config(args.config)
        while True:
            accounts = open(args.data, "r").read().splitlines()
            self.log(f"{hijau}account detected : {putih}{len(accounts)}")
            if len(accounts) <= 0:
                self.log(f"{merah}please add data account in {args.data}")
                sys.exit()

            print(self.line)
            for account in accounts:
                access_token = None
                data_parse = self.data_parsing(account)
                user = json.loads(data_parse["user"])
                userid = user["id"]
                first_name = user['first_name']
                self.log(f'{hijau}login as {putih}{first_name}')
                data = f"query_id={data_parse['query_id']}&user={quote(data_parse['user'])}&auth_date={data_parse['auth_date']}&hash={data_parse['hash']}"
                uids = json.loads(open("uuid.json", "r").read())
                if str(userid) not in uids.keys():
                    uid = uuid.uuid4().__str__()
                    uids[str(userid)] = uid
                    open("uuid.json", "w").write(json.dumps(uids, indent=4))
                else:
                    uid = uids[str(userid)]
                tokens = json.loads(open("tokens.json", "r").read())
                if uid not in tokens.keys():
                    access_token = self.gamee_login(data, uid)
                else:
                    access_token = tokens[uid]
                is_expired = self.token_checker(access_token)
                if is_expired:
                    access_token = self.gamee_login(data, uid)

                res = self.gamee_spin(access_token, uid)
                res = self.gamee_mining_page(access_token, uid)
                print(self.line)
                self.countdown(self.DEFAULT_INTERVAL)

            self.countdown(self.DEFAULT_COUNTDOWN)


if __name__ == "__main__":
    try:
        app = Gamee()
        app.main()
    except KeyboardInterrupt:
        sys.exit()
