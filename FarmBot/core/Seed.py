# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


import json


class Seed:
    def __init__(self, log, httpRequest, account_name):
        self.log = log
        self.http = httpRequest
        self.account_name = account_name

    def claim(self):
        try:
            response = self.http.post(
                url="/api/v1/seed/claim",
                display_errors=False,
            )

            if response is None:
                # self.log.error(f"<r>⭕ <c>{self.account_name}</c> failed to claim!</r>")
                return None

            return response
        except Exception as e:
            self.log.error(f"<r>⭕ {self.account_name}</c> | {e} failed to claim!</r>")
            return None
