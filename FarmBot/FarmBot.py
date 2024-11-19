# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot
import sys
import os
import time
import random
from dateutil import parser

from utilities.utilities import getConfig
from .core.HttpRequest import HttpRequest
from .core.Base import Base
from .core.Task import Task
from .core.Hunt import Hunt
from .core.Worm import Worm
from .core.Boost import Boost
from .core.Bird import Bird
from .core.Guild import Guild
from .core.Events import Events
from .core.Seed import Seed


MasterCryptoFarmBot_Dir = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__ + "/../../"))
)
sys.path.append(MasterCryptoFarmBot_Dir)


class FarmBot:
    def __init__(
        self,
        log,
        bot_globals,
        account_name,
        web_app_query,
        proxy=None,
        user_agent=None,
        isPyrogram=False,
        tgAccount=None,
    ):
        self.log = log
        self.bot_globals = bot_globals
        self.account_name = account_name
        self.web_app_query = web_app_query
        self.proxy = proxy
        self.user_agent = user_agent
        self.isPyrogram = isPyrogram
        self.tgAccount = tgAccount

    async def run(self):
        self.display_name = self.account_name.replace("ma_", "")
        self.log.info(
            f"<cyan>{self.account_name}</cyan><g> | 🤖 Starting Seed farming...</g>"
        )

        try:
            self.http = HttpRequest(
                log=self.log,
                proxy=self.proxy,
                user_agent=self.user_agent,
                tgWebData=self.web_app_query,
                account_name=self.account_name,
            )
            base = Base(self.log, self.http, self.account_name)
            task = Task(self.log, self.http, self.account_name)
            hunt = Hunt(self.log, self.http, self.account_name)
            worm = Worm(self.log, self.http, self.account_name)

            if getConfig("auto_add_tag", False):
                await base.check_tag(tgAccount=self.tgAccount)

            self.log.info(
                f"<cyan>{self.account_name}</cyan><g> | 🔄 Getting profile ...</g>"
            )

            profile = base.get_profile2()
            if profile is None or "data" not in profile:
                self.log.error(
                    f"<r>⭕ <c>{self.display_name}</c> failed to get profile!</r>"
                )
                return None

            profile = profile.get("data", {})
            if profile.get("newcomer_event", False) or "tg_id" not in profile:
                self.log.info(
                    f"<cyan>{self.account_name}</cyan><g> | 🐣 Registering account...</g>"
                )

                time.sleep(0.5)
                base.post_profile()
                time.sleep(3)
                profile = base.get_profile()

                if profile is None:
                    self.log.error(
                        f"<r>⭕ <c>{self.account_name}</c> failed to get profile!</r>"
                    )
                    return None

            self.log.info(
                f"<cyan>{self.account_name}</cyan><g> | 🔄 Sending basic requests ...</g>"
            )

            self.log.info(
                f"<cyan>{self.account_name}</cyan><g> | 📊 Getting progresses ...</g>"
            )
            progresses = task.get_progresses()
            self.log.info(
                f"<cyan>{self.account_name}</cyan><g> | 🎁 Getting login bonus ...</g>"
            )
            login_bonus = base.get_login_bonus()
            self.log.info(
                f"<cyan>{self.account_name}</cyan><g> | ⚙️ Getting settings ...</g>"
            )
            settings = base.get_settings()
            self.log.info(
                f"<cyan>{self.account_name}</cyan><g> | 👤 Getting profile ...</g>"
            )
            profile = base.get_profile2()
            if profile is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to get profile!</r>"
                )
                return None

            self.log.info(
                f"<cyan>{self.account_name}</cyan><g> | 💰 Getting balance ...</g>"
            )
            balance = base.get_balance()
            balance_rounded = round(
                balance.get("data", 0) / 1_000_000_000,
                3 if balance.get("data", 0) > 1_000_000_000 else 0,
            )
            self.log.info(
                f"<cyan>{self.account_name}</cyan><g> | 📨 Getting last message ...</g>"
            )
            last_message = base.get_last_message()

            boost = Boost(self.log, self.http, self.account_name)
            self.log.info(
                f"<cyan>{self.account_name}</cyan><g> | 🚀 Getting boosts ...</g>"
            )
            boosts = boost.get_boosts()
            self.log.info(
                f"<cyan>{self.account_name}</cyan><g> | 🐛 Getting worms ...</g>"
            )
            worms = worm.get_worms()
            bird = Bird(self.log, self.http, self.account_name)
            self.log.info(
                f"<cyan>{self.account_name}</cyan><g> | 🦅 Getting bird ...</g>"
            )
            is_leader = bird.is_leader()

            guild = Guild(self.log, self.http, self.account_name)
            self.log.info(
                f"<cyan>{self.account_name}</cyan><g> | 🏰 Getting guild ...</g>"
            )
            guild_detail = guild.get_detail()

            events = Events(self.log, self.http, self.account_name)
            self.log.info(
                f"<cyan>{self.account_name}</cyan><g> | 📅 Getting events ...</g>"
            )
            event_me = events.get_me()

            self.log.info(
                f"<cyan>{self.account_name}</cyan><g> | 📈 Balance: <c>{balance_rounded} 💚</c></g>"
            )

            if (
                "data" in profile
                and profile["data"] is not None
                and "last_claim" in profile["data"]
            ):

                last_claim = profile["data"]["last_claim"]
                if last_claim.startswith("0001"):
                    last_claim = "2022-10-08T22:41:44.069281Z"

                last_claim = int(parser.isoparse(last_claim).timestamp())
                current_time = int(time.time())
                if current_time - last_claim > 1800:
                    seed = Seed(self.log, self.http, self.account_name)
                    self.log.info(
                        f"<cyan>{self.account_name}</cyan><g> | 💚 Claiming seed...</g>"
                    )

                    seed_claim = seed.claim()
                    if seed_claim is not None:
                        self.log.info(
                            f"<cyan>{self.account_name}</cyan><g> | 💚 Claimed <c>{seed_claim.get('data', {}).get('amount', 0) / 1_000_000_000}</c> Seed 💚</g>"
                        )

                    balance = base.get_balance()
                    profile = base.get_profile2()
                else:
                    self.log.info(
                        f"<cyan>{self.account_name}</cyan><g> | 💚 Seed already claimed...</g>"
                    )

            upgrade_levels = base.get_levels(profile)

            self.log.info(
                f"<cyan>{self.account_name}</cyan><g> | 📦 Storage level: <c>{upgrade_levels.get('storage-size', 1)}</c> | ⛏️ Mining level: <c>{upgrade_levels.get('mining-speed', 1)}</c> | 💧 Holy level: <c>{upgrade_levels.get('holy-water', 1)}</c></g>"
            )

            if (
                profile is not None
                and "data" in profile
                and "give_first_egg" in profile["data"]
                and profile["data"]["give_first_egg"] is False
            ):
                self.log.info(
                    f"<cyan>{self.account_name}</cyan><g> | 🐣 Getting first egg...</g>"
                )
                egg = base.get_first_egg_and_hatch()
                if egg is None:
                    self.log.error(
                        f"<r>⭕ <c>{self.account_name}</c> failed to get first egg!</r>"
                    )
            if (
                worms is not None
                and "data" in worms
                and "is_caught" in worms["data"]
                and worms["data"]["is_caught"] is False
            ):
                start_time = int(
                    parser.isoparse(worms["data"]["created_at"]).timestamp()
                )
                end_time = int(parser.isoparse(worms["data"]["ended_at"]).timestamp())

                if start_time < time.time() < end_time:
                    self.log.info(
                        f"<cyan>{self.account_name}</cyan><g> | 🐛 Capturing worm...</g>"
                    )
                    worm_capture = worm.capture_worm()
                    if worm_capture is not None:
                        self.log.info(
                            f"<cyan>{self.account_name}</cyan><g> | 🐛 Captured worm!</g>"
                        )
                        worms = worm.get_worms()
                else:
                    self.log.info(
                        f"<cyan>{self.account_name}</cyan><g> | 🐛 Worm event not started...</g>"
                    )
            else:
                self.log.info(
                    f"<cyan>{self.account_name}</cyan><g> | 🐛 Worm already captured...</g>"
                )

            if (login_bonus is not None) and "data" in login_bonus:
                ready_to_claim = False
                day = 0
                if "no" in login_bonus["data"]:
                    last_claim = int(
                        parser.isoparse(login_bonus["data"]["timestamp"]).timestamp()
                    )
                    current_time = int(time.time())
                    if current_time - last_claim > 86400:
                        ready_to_claim = True
                        day = login_bonus["data"]["no"]
                else:
                    ready_to_claim = True

                day += 1
                streak_reward = None
                if ready_to_claim:
                    self.log.info(
                        f"<cyan>{self.account_name}</cyan><g> | 🎯 Claiming daily bonus! Day: <c>{day} 🗓️</c></g>"
                    )

                    base.get_daily_login_streak()
                    base.get_streak_reward()
                    base.get_login_bonus()
                    base.get_settings()
                    time.sleep(1)

                    dailyBonusResult = base.get_daily_check_in()
                    if dailyBonusResult is not None:
                        self.log.info(
                            f"<cyan>{self.account_name}</cyan><g> | 🎯 Claimed daily bonus! Day: {dailyBonusResult.get('data', {}).get('no', 1)}</g>"
                        )

                    base.get_daily_login_streak()
                    streak_reward = base.get_streak_reward()
                    base.get_login_bonus()

                if (
                    streak_reward is not None
                    and "data" in streak_reward
                    and "status" in streak_reward["data"]
                ):
                    if streak_reward["data"]["status"] == "created":
                        streak_reward_id = streak_reward["data"]["id"]
                        self.log.info(
                            f"<cyan>{self.account_name}</cyan><g> | 🎯 Claiming streak reward...</g>"
                        )
                        base.claim_streak_reward(streak_reward_id)

                        self.log.info(
                            f"<cyan>{self.account_name}</cyan><g> | 🎯 Claimed streak reward!</g>"
                        )

            if getConfig("auto_upgrade_storage", True):
                self.log.info(
                    f"<cyan>{self.account_name}</cyan><g> | 📦 Checking if storage upgrade is possible...</g>"
                )
                base.upgrade("storage")
                time.sleep(1)
            if getConfig("auto_upgrade_mining", True):
                self.log.info(
                    f"<cyan>{self.account_name}</cyan><g> | ⛏️ Checking if mining upgrade is possible...</g>"
                )
                base.upgrade("mining")
                time.sleep(1)
            if getConfig("auto_upgrade_holy", True):
                self.log.info(
                    f"<cyan>{self.account_name}</cyan><g> | 💧 Checking if holy upgrade is possible...</g>"
                )
                base.upgrade("holy")
                time.sleep(1)

            if getConfig("auto_do_tasks", True):
                self.log.info(
                    f"<cyan>{self.account_name}</cyan><g> | 📗 Starting to do tasks...</g>"
                )
                await task.do_tasks(self.bot_globals, tgAccount=self.tgAccount)
                task.do_holy_tasks()
                self.log.info(
                    f"<cyan>{self.account_name}</cyan><g> | 📗 Possible Tasks completed!</g>"
                )

            if getConfig("auto_do_hunt", True):
                hunt.process_hunt()

        except Exception as e:
            self.log.error(f"<r>⭕ <c>{self.account_name}</c> failed to finish!</r>")
            self.log.error(f"<r>⭕ Error (for devs): {e}</r>")
            return None
        finally:
            delay_between_accounts = getConfig("delay_between_accounts", 60)
            random_sleep = random.randint(0, 20) + delay_between_accounts
            self.log.info(
                f"<g>⌛ Farming for <c>{self.display_name}</c> completed. Waiting for <c>{random_sleep}</c> seconds before running the next account...</g>"
            )
            time.sleep(random_sleep)
