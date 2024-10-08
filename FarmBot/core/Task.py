# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


import time


class Task:
    def __init__(self, log, httpRequest, account_name):
        self.log = log
        self.http = httpRequest
        self.account_name = account_name

    def do_tasks(self):
        try:
            response = self.http.get(
                url="/api/v1/tasks/progresses",
                domain="elb",
            )

            if response is None:
                self.log.error(f"<r>⭕ {self.account_name} failed to get tasks!</r>")
                return None

            for task in response["data"]:
                if (
                    task.get("task_user", None) is None
                    or task.get("task_user", {}).get("completed", True) is False
                ):
                    self.complete_task(task["id"], task["name"])

        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to get tasks!</r>")
            return None

    def complete_task(self, task_id, task_name):
        try:
            response = self.http.post(
                url=f"/api/v1/tasks/{task_id}",
                domain="elb",
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ {self.account_name} failed to complete task {task_name}!</r>"
                )
                return None

            # self.log.info(
            #     f"<g>📗 {self.account_name} task {task_name} started and marked as completed!</g>"
            # )
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to complete task {task_name}!</r>")
            return None

    def complete_upgrades_task(self, task_id, task_name):
        try:
            response = self.http.post(
                url=f"/api/v1/upgrades/tasks/{task_id}",
                domain="elb",
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ {self.account_name} failed to complete task {task_name}!</r>"
                )
                return None

            # self.log.info(
            #     f"<g>📗 {self.account_name} task {task_name} started and marked as completed!</g>"
            # )
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to complete task {task_name}!</r>")
            return None

    def do_holy_tasks(self):
        try:
            response = self.http.get(
                url="/api/v1/upgrades/tasks/progresses",
                domain="elb",
            )

            if response is None:
                self.log.error(f"<r>⭕ {self.account_name} failed to get tasks!</r>")
                return None

            for task in response["data"]:
                self.complete_upgrades_task(task["id"], task["name"])
                time.sleep(0.5)
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to get tasks!</r>")
            return None
