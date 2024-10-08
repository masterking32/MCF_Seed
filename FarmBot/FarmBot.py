# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot
import sys
import os
import time
import random

from utilities.utilities import getConfig
from .core.HttpRequest import HttpRequest
from .core.Base import Base
from .core.Task import Task
from .core.Hunt import Hunt
from .core.Worm import Worm

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
                base.check_tag(tgAccount=self.tgAccount)

            profile = base.get_profile2()
            if profile is None or "data" not in profile:
                self.log.error(
                    f"<r>⭕ <c>{self.display_name}</c> failed to get profile!</r>"
                )
                return None

            profile = profile.get("data", {})
            if (
                "newcomer_event" in profile
                and profile["newcomer_event"] is True
                or "tg_id" not in profile
            ):
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
                    return None, None

            balance = base.get_balance()
            balance_rounded = round(
                balance.get("data", 0) / 1_000_000_000,
                3 if balance.get("data", 0) > 1_000_000_000 else 0,
            )

            self.log.info(
                f"<cyan>{self.account_name}</cyan><g> | 📈 Balance: {balance_rounded}</g>"
            )

            progresses = task.get_progresses()
            login_bonus = base.get_login_bonus()

            upgrade_levels = base.get_levels()

            self.log.info(
                f"<cyan>{self.account_name}</cyan><g> | 📦 Storage level: {upgrade_levels.get('storage-size', 1)} | ⛏️ Mining level: {upgrade_levels.get('mining-speed', 1)} | 💧 Holy level: {upgrade_levels.get('holy-water', 1)}</g>"
            )

            wormCaught = worm.capture_worm()
            claimStatus = base.claim()

            if claimStatus is not None:
                self.log.info(
                    f"<cyan>{self.account_name}</cyan><g> | ⛏️ Claimed {claimStatus.get('data', {}).get('amount', 0) / 1_000_000_000} Seed 💚</g>"
                )

            if wormCaught:
                self.log.info(
                    f"<cyan>{self.account_name}</cyan><g> | 🐛 Worm caught from the tree!</g>"
                )

            profile = profile["data"]

            if profile.get("give_first_egg", True) is False:
                self.log.info(
                    f"<cyan>{self.account_name}</cyan><g> | 🐣 Getting first egg...</g>"
                )
                egg = base.get_first_egg_and_hatch()
                if egg is None:
                    self.log.error(
                        f"<r>⭕ <c>{self.account_name}</c> failed to get first egg!</r>"
                    )

            dailyBonusResult = base.get_daily_checkin()

            if dailyBonusResult is not None:
                self.log.info(
                    f"<cyan>{self.account_name}</cyan><g> | 🎯 Claimed daily bonus! Day: {dailyBonusResult.get('data', {}).get('no', 1)}</g>"
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
                task.do_tasks()
                task.do_holy_tasks()
                self.log.info(
                    f"<cyan>{self.account_name}</cyan><g> | 📗 Possible Tasks completed!</g>"
                )

            if getConfig("auto_do_hunt", True):
                hunt.process_hunt()

        except Exception as e:
            self.log.error(f"<r>⭕ <c>{self.account_name}</c> failed to login!</r>")
            self.log.error(f"<r>⭕ Error (for devs): {e}</r>")
            return None, None
        finally:
            delay_between_accounts = getConfig("delay_between_accounts", 60)
            random_sleep = random.randint(0, 20) + delay_between_accounts
            self.log.info(
                f"<g>⌛ Farming for <c>{self.display_name}</c> completed. Waiting for <c>{random_sleep}</c> seconds before running the next account...</g>"
            )
            time.sleep(random_sleep)
