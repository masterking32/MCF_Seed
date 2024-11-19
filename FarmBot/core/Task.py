# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


import asyncio
import random
import time
import os
import json
import uuid

from mcf_utils.api import API
from mcf_utils.tgAccount import tgAccount as TG
from utilities import utilities as utils


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
                    f"<r><c>{self.account_name}</c> | ⭕ Failed to get tasks!</r>"
                )
                return None

            return response["data"]

        except Exception as e:
            self.log.error(
                f"<r><c>{self.account_name}</c> | ⭕ {e} failed to get tasks!</r>"
            )
            return None

    async def do_tasks(self, bot_globals, tgAccount=None):
        try:
            response = self.http.get(
                url="/api/v1/tasks/progresses",
            )

            if response is None:
                self.log.error(
                    f"<r><c>{self.account_name}</c> | ⭕ Failed to get tasks!</r>"
                )
                return None

            for task in response["data"]:
                try:
                    pwd = None
                    if (
                        task.get("task_user", None) is None
                        or task.get("task_user", {}).get("completed", True) is False
                    ):
                        if (
                            task.get("type", "") in ["Join community", "OKX_community"]
                            and tgAccount is not None
                        ):

                            if not utils.getConfig("auto_join_channels", True):
                                continue

                            self.log.info(
                                f"<g><c>{self.account_name}</c> | 🚀 Starting task <c>{task.get('name', '')}</c>...</g>"
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
                                    continue

                                await tgAccount.joinChat(
                                    url,
                                )
                            except Exception as e:
                                continue
                        elif task.get("type", "").lower() == "play app":
                            if not utils.getConfig("auto_start_bots", True):
                                continue
                            url = task.get("metadata", {}).get("url", "")

                            if url == "":
                                continue

                            data = {
                                "task_type": "invite",
                                "task_data": url,
                            }

                            api_response = self.get_api_data(
                                data, license_key=bot_globals["license"]
                            )
                            if (
                                api_response is None
                                or "status" not in api_response
                                or api_response["status"] != "success"
                            ):
                                continue

                            ref_link = api_response.get("referral")
                            bot_id = api_response.get("bot_id")
                            if ref_link is None or bot_id is None:
                                continue

                            self.log.info(
                                f"<g><c>{self.account_name}</c> | 🚀 Starting bot <c>@{bot_id}</c> for task <c>{task.get('name', '')}</c>...</g>"
                            )

                            try:
                                tg = TG(
                                    bot_globals=bot_globals,
                                    log=self.log,
                                    accountName=self.account_name,
                                    proxy=self.http.proxy,
                                    BotID=bot_id,
                                    ReferralToken=ref_link,
                                    AppURL=None,
                                    MuteBot=True,
                                )

                                await tg.getWebViewData():

                                self.log.info(
                                    f"<g><c>{self.account_name}</c> | ✅ Bot <c>{bot_id}</c> started!</g>"
                                )
                                await asyncio.sleep(5)
                            except Exception as e:
                                self.log.error(
                                    f"<r><c>{self.account_name}</c> | ⭕ {e} failed to start bot!</r>"
                                )
                        elif task.get("type", "") in [
                            "TG story",
                            "Follow us",
                            "telegram-name-include",
                            "Add_list",
                            "OKX",
                        ]:
                            pass
                        elif (
                            task.get("type", "") in ["academy"]
                            and task.get("metadata", {}).get("answer_length", -1) > 0
                        ):
                            if task.get("metadata", {}).get("url", "") == "":
                                continue

                            data = {
                                "task_type": "keyword",
                                "task_id": task.get("metadata", {}).get("url", ""),
                                "task_name": task.get("name", ""),
                            }
                            api_response = self.get_api_data(
                                data, bot_globals["license"]
                            )
                            if not api_response:
                                self.log.info(
                                    f"<y><c>{self.account_name}</c> | 🟡 Answer for task {task.get('name', '')} not found on API ...</y>"
                                )
                                continue
                            answer = api_response.get("answer", "")
                            if not answer:
                                continue

                            pwd = answer
                        else:
                            self.log.info(
                                f"<y><c>{self.account_name}</c> | 🟡 Task {task.get('name', '')} not supported...</y>"
                            )
                            continue

                        self.log.info(
                            f"<g><c>{self.account_name}</c> | 📗 Task {task.get('name', '')} started and marked as completed!</g>"
                        )
                        self.complete_task(task["id"], task["name"], pwd)
                        time.sleep(random.randint(1, 5))
                except Exception as e:
                    pass
        except Exception as e:
            self.log.error(
                f"<r><c>{self.account_name}</c> | ⭕ {e} failed to get tasks!</r>"
            )
            return None

    def complete_task(self, task_id, task_name, pwd=""):
        try:
            response = self.http.post(
                url=f"/api/v1/tasks/{task_id}",
                data=json.dumps({"answer": pwd}) if pwd is not None else "{}",
            )

            if response is None:
                raise Exception(f"Complete task response is NULL")
            self.log.info(
                f"<g><c>{self.account_name}</c> | 📗 Task {task_name} started ...</g>"
            )
            time.sleep(random.randint(3, 5))
            notify_id = response.get("data", "")
            if not notify_id or not self._is_uuid(notify_id):
                raise Exception(f"Unable to get notify id.")

            is_completed = self._task_notification(notify_id)
            status = "completed" if is_completed else f"<y>not completed</y>"
            self.log.info(
                f"<g><c>{self.account_name}</c> | 📗 Task {task_name} {status}!</g>"
            )
        except Exception as e:
            self.log.error(
                f"<r><c>{self.account_name}</c> | ⭕ Failed to complete task {task_name}!</r>"
            )
            self.log.error(f"<r><c>{self.account_name}</c> | ⭕ {str(e)}</r>")
            return None

    def _task_notification(self, notify_id):
        response = self.http.get(
            url=f"/api/v1/tasks/notification/{notify_id}",
        )
        if response is None or "data" not in response:
            return False
        data = response.get("data", {}).get("data", {})
        is_completed = data.get("completed", False)
        return is_completed

    def _is_uuid(self, value: str, version: int = 4) -> bool:
        try:
            uuid_obj = uuid.UUID(value, version=version)
            return str(uuid_obj) == value
        except ValueError:
            return False

    def complete_upgrades_task(self, task_id, task_name):
        try:
            response = self.http.post(
                url=f"/api/v1/upgrades/tasks/{task_id}",
            )

            if response is None:
                self.log.error(
                    f"<r><c>{self.account_name}</c> | ⭕ Failed to complete task {task_name}!</r>"
                )
                return None

            # self.log.info(
            #     f"<g>📗 <c>{self.account_name}</c> task {task_name} started and marked as completed!</g>"
            # )
        except Exception as e:
            self.log.error(
                f"<r><c>{self.account_name}</c> | ⭕ {e} failed to complete task {task_name}!</r>"
            )
            return None

    def do_holy_tasks(self):
        try:
            response = self.http.get(
                url="/api/v1/upgrades/tasks/progresses",
            )

            if response is None:
                self.log.error(
                    f"<r><c>{self.account_name}</c> | ⭕ Failed to get tasks!</r>"
                )
                return None

            for task in response["data"]:
                self.complete_upgrades_task(task["id"], task["name"])
                time.sleep(0.5)
        except Exception as e:
            self.log.error(
                f"<r><c>{self.account_name}</c> | ⭕ {e} failed to get tasks!</r>"
            )
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
            self.log.info(
                f"<y><c>{self.account_name}</c> | 🟡 {response['message']}</y>"
            )
            return None
        else:
            self.log.error(
                f"<y><c>{self.account_name}</c> | 🟡 Unable to get task answer, please try again later</y>"
            )
            return None
