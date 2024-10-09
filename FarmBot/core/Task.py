# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


import asyncio
import random
import time

from mcf_utils.api import API
from mcf_utils.tgAccount import tgAccount as TG


class Task:
    def __init__(self, log, httpRequest, account_name):
        self.log = log
        self.http = httpRequest
        self.account_name = account_name

    def get_progresses(self):
        try:
            response = self.http.get(
                url="/api/v1/tasks/progresses",
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to get tasks!</r>"
                )
                return None

            return response["data"]

        except Exception as e:
            self.log.error(
                f"<r>⭕ <c>{self.account_name}</c> | {e} failed to get tasks!</r>"
            )
            return None

    async def do_tasks(self, bot_globals, tgAccount=None):
        try:
            response = self.http.get(
                url="/api/v1/tasks/progresses",
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to get tasks!</r>"
                )
                return None

            for task in response["data"]:
                try:
                    if (
                        task.get("task_user", None) is None
                        or task.get("task_user", {}).get("completed", True) is False
                    ):
                        if (task.get("type", "").lower() == "join community"
                            and tgAccount is not None):
                            self.log.info(
                                f"<g>🚀 Starting task <c>{task.get('name', '')}</c>...</g>"
                            )
                            try:
                                url = task.get("metadata", {}).get("url", "")
                                if "me/+" not in url:
                                    url = (
                                        url.replace("https://t.me/", "")
                                        .replace("@", "")
                                        .replace("boost/", "")
                                    )

                                    url = url.split("/")[0] if "/" in url else url

                                if url == "":
                                    print(url)
                                    continue

                                await tgAccount.joinChat(
                                    url,
                                )
                            except Exception as e:
                                pass
                        elif task.get("type", "").lower() == "play app":
                            url = task.get("metadata", {}).get("url", "")

                            if url == "":
                                continue

                            data = {
                                "task_type": "invite",
                                "task_data": url,
                            }

                            api_response = self.get_api_data(data, license_key=bot_globals["license"])
                            if (
                                api_response is None
                                or "status" not in api_response
                                or api_response["status"] != "success"
                            ):
                                print(api_response)
                                continue

                            ref_link = api_response.get("referral")
                            bot_id = api_response.get("bot_id")
                            if ref_link is None or bot_id is None:
                                continue

                            self.log.info(
                                f"<g>🚀 Starting bot <c>{task.get("name", "")}</c>...</g>"
                            )
                            try:
                                tg = TG(
                                    bot_globals=bot_globals,
                                    log=self.log,
                                    accountName=self.account_name,
                                    proxy=self.http.proxy,
                                    BotID=bot_id,
                                    ReferralToken=ref_link,
                                    MuteBot=True,
                                )

                                await tg.getWebViewData()

                                self.log.info(f"<g>✅ Bot <c>{bot_id}</c> started!</g>")
                                await asyncio.sleep(5)
                            except Exception as e:
                                self.log.error(f"<r>⭕ {e} failed to start bot!</r>")
                        elif (
                            task.get("type", "") == "TG story"
                            or task.get("type", "") == "Follow us"
                            or task.get("type", "") == "telegram-name-include"
                            or task.get("type", "") == "Add_list"
                        ):
                            pass
                        else:
                            self.log.info(
                                f"<y>🟡 <c>{self.account_name}</c> task {task.get('name', '')} not supported...</y>"
                            )
                            continue

                        self.log.info(
                            f"<g>📗 <c>{self.account_name}</c> task {task.get('name', '')} started and marked as completed!</g>"
                        )
                        self.complete_task(task["id"], task["name"])
                        time.sleep(random.randint(1, 5))
                except Exception as e:
                    pass
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to get tasks!</r>")
            return None

    def complete_task(self, task_id, task_name):
        try:
            response = self.http.post(
                url=f"/api/v1/tasks/{task_id}",
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to complete task {task_name}!</r>"
                )
                return None

            # self.log.info(
            #     f"<g>📗 <c>{self.account_name}</c> task {task_name} started and marked as completed!</g>"
            # )
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to complete task {task_name}!</r>")
            return None

    def complete_upgrades_task(self, task_id, task_name):
        try:
            response = self.http.post(
                url=f"/api/v1/upgrades/tasks/{task_id}",
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to complete task {task_name}!</r>"
                )
                return None

            # self.log.info(
            #     f"<g>📗 <c>{self.account_name}</c> task {task_name} started and marked as completed!</g>"
            # )
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to complete task {task_name}!</r>")
            return None

    def do_holy_tasks(self):
        try:
            response = self.http.get(
                url="/api/v1/upgrades/tasks/progresses",
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to get tasks!</r>"
                )
                return None

            for task in response["data"]:
                self.complete_upgrades_task(task["id"], task["name"])
                time.sleep(0.5)
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to get tasks!</r>")
            return None

    def get_api_data(self, data, license_key):
        if license_key is None:
            return None

        apiObj = API(self.log)
        data["game_name"] = "seed"
        data["action"] = "get_task"
        response = apiObj.get_task_answer(license_key, data)
        time.sleep(3)
        if "error" in response:
            self.log.error(f"<y>⭕ API Error: {response['error']}</y>")
            return None
        elif "status" in response and response["status"] == "success":
            return response
        elif (
            "status" in response
            and response["status"] == "error"
            and "message" in response
        ):
            self.log.info(f"<y>🟡 {response['message']}</y>")
            return None
        else:
            self.log.error(
                f"<y>🟡 Unable to get task answer, please try again later</y>"
            )
            return None
