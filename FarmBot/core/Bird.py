# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


class Bird:
    def __init__(self, log, httpRequest, account_name):
        self.log = log
        self.http = httpRequest
        self.account_name = account_name

    def is_leader(self):
        try:
            response = self.http.get(url="/api/v1/bird/is-leader")

            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to get bird info!</r>"
                )
                return None

            return response

        except Exception as e:
            self.log.error(
                f"<r>⭕ <c>{self.account_name}</c> | {e} failed to get bird info!</r>"
            )
            return None
