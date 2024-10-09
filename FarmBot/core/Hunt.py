# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


import json
import time
from dateutil import parser


class Hunt:
    def __init__(self, log, httpRequest, account_name):
        self.log = log
        self.http = httpRequest
        self.account_name = account_name

    def claim_hunt_reward(self, bird_id):
        try:
            response = self.http.post(
                url=f"/api/v1/bird-hunt/complete",
                domain="elb",
                data=json.dumps({"bird_id": bird_id}),
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ {self.account_name} failed to claim hunt reward!</r>"
                )
                return None

            return response

        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to claim hunt reward!</r>")
            return None

    def get_bird_info(self):
        try:
            response = self.http.get(url="/api/v1/bird/is-leader", domain="elb")

            if response is None:
                self.log.error(
                    f"<r>⭕ {self.account_name} failed to get bird info!</r>"
                )
                return None

            return response

        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to get bird info!</r>")
            return None

    def make_bird_happy(self, bird_id):
        try:
            response = self.http.post(
                url=f"/api/v1/bird-happiness",
                domain="elb",
                data=json.dumps({"bird_id": bird_id, "happiness_rate": 10000}),
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ {self.account_name} failed to make bird happy!</r>"
                )
                return None

            return response

        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to make bird happy!</r>")
            return None

    def feed_bird(self, bird_id, worm_id):
        try:
            response = self.http.post(
                url=f"/api/v1/bird-feed",
                domain="elb",
                data=json.dumps({"bird_id": bird_id, "worm_ids": worm_id}),
            )

            if response is None:
                self.log.error(f"<r>⭕ {self.account_name} failed to feed bird!</r>")
                return None

            return response

        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to feed bird!</r>")
            return None

    def start_hunt(self, bird_id):
        try:
            response = self.http.post(
                url=f"/api/v1/bird-hunt/start",
                domain="elb",
                data=json.dumps({"bird_id": bird_id, "task_level": 0}),
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ {self.account_name} failed to start hunting!</r>"
                )
                return None

            return response

        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to start hunting!</r>")
            return None

    def process_hunt(self):
        bird_data = self.get_bird_info()
        bird_data = bird_data.get("data", None)
        if bird_data is None:
            self.log.info(f"{self.account_name} | Can't get bird data...")
            return None
        elif bird_data["status"] == "hunting":
            timestamp_naive = int(parser.isoparse(bird_data["hunt_end_at"]).timestamp())

            now = int(time.time())

            if now < timestamp_naive:
                self.log.info(
                    f"<cyan>{self.account_name}</cyan><g> | 🦅 Bird currently hunting...</g>"
                )
            else:
                self.log.info(
                    f"<cyan>{self.account_name}</cyan><g> | 🦅 Bird hunt completed, claiming reward...</g>"
                )
                self.claim_hunt_reward(bird_data["id"])
        else:
            condition = True
            if bird_data["energy_level"] == 0:
                self.log.info(
                    f"<cyan>{self.account_name}</cyan><g> | 🦅 Feeding bird...</g>"
                )
                from .Worm import Worm

                worm = Worm(self.log, self.http, self.account_name)
                worms = worm.get_worm_list()
                worms = worms.get("data", None)
                if worms is None:
                    condition = False
                    self.log.info(f"{self.account_name} | Failed to fetch worm data")
                elif len(worms) == 0:
                    self.log.warning(
                        f"{self.account_name} | You dont have any worm to feed bird!"
                    )
                    condition = False
                else:
                    try:
                        energy = (
                            bird_data["energy_max"] - bird_data["energy_level"]
                        ) / 1000000000
                    except:
                        energy = 2
                    wormss = []
                    for worm in worms:
                        if worm["type"] == "common" and worm["on_market"] is False:
                            wormss.append(worm["id"])
                            energy -= 2
                            if energy <= 1:
                                break
                    if energy > 1:
                        for worm in worms:
                            if (
                                worm["type"] == "uncommon"
                                and worm["on_market"] is False
                            ):
                                wormss.append(worm["id"])
                                energy -= 4
                                if energy <= 1:
                                    break
                    self.feed_bird(bird_data["id"], wormss)
                    if energy > 1:
                        condition = False
            if bird_data["happiness_level"] == 0:
                self.log.info(
                    f"<cyan>{self.account_name}</cyan><g> | 🦅 Attempting to make bird happy...</g>"
                )
                check = self.make_bird_happy(bird_data["id"])
                if check:
                    self.log.info(
                        f"<cyan>{self.account_name}</cyan><g> | 🦅 Bird is happy now!</g>"
                    )
                else:
                    self.log.info(
                        f"<cyan>{self.account_name}</cyan> | <r>🦅 Failed to make bird happy!</r>"
                    )
                    condition = False

            if condition:
                huntResponse = self.start_hunt(bird_data["id"])
                if huntResponse is not None:
                    self.log.info(
                        f"<cyan>{self.account_name}</cyan><g> | 🦅 Bird is now hunting!</g>"
                    )
