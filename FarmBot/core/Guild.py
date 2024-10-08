# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


class Guild:
    def __init__(self, log, httpRequest, account_name):
        self.log = log
        self.http = httpRequest
        self.account_name = account_name

    def get_detail(self):
        try:
            response = self.http.get(
                url="/api/v1/guild/member/detail",
            )
            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to get guild detail!</r>"
                )
                return None
            return response
        except Exception as e:
            self.log.error(
                f"<r>⭕ <c>{self.account_name}</c> | {e} failed to get guild detail!</r>"
            )
