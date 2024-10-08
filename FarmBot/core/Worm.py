# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


class Worm:
    def __init__(self, log, httpRequest, account_name):
        self.log = log
        self.http = httpRequest
        self.account_name = account_name

    def is_worm_available(self):
        try:
            response = self.http.get(
                url="/api/v1/worms",
                domain="elb",
            )
            if response is None:
                self.log.error(
                    f"<r>⭕ {self.account_name} failed to get worm status!</r>"
                )
                return None
            return response["data"].get("is_caught", None)

        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to get worm status!</r>")
            return None

    def capture_worm(self):
        try:
            wormInfo = self.is_worm_available()
            if wormInfo:
                response = self.http.post(
                    url="/api/v1/worms/catch",
                    domain="elb",
                    display_errors=False,
                )
                if response is None:
                    return None
                return response
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to capture worm!</r>")
            return None

    def get_worm_list(self):
        try:
            response = self.http.get(
                url="/api/v1/worms/me-all",
                domain="elb",
            )
            if response is None:
                self.log.error(
                    f"<r>⭕ {self.account_name} failed to get worm list!</r>"
                )
                return None
            return response
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to get worm list!</r>")
            return None
