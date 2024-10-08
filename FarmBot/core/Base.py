# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


import json


class Base:
    def __init__(self, log, httpRequest, account_name):
        self.log = log
        self.http = httpRequest
        self.account_name = account_name

    def get_profile(self):
        try:
            response = self.http.get(
                url="/api/v1/profile2",
                domain="elb",
            )

            if response is None:
                self.log.error(f"<r>⭕ {self.account_name} failed to get profile!</r>")
                return None

            return response

        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to get profile!</r>")
            return None

    def post_profile(self):
        try:
            response = self.http.post(
                url="/api/v1/profile",
                domain="elb",
            )
            if response is None:
                self.log.error(
                    f"<r>⭕ {self.account_name} failed to set-up account!</r>"
                )
                return None
            return response
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to set-up account!</r>")
            return None

    def get_levels(self):
        try:
            profile = self.get_profile()
            if profile is None:
                return None
            upgrade_levels = {}
            for upgrade in profile["data"]["upgrades"]:
                upgrade_type = upgrade["upgrade_type"]
                upgrade_level = upgrade["upgrade_level"]
                if upgrade_type in upgrade_levels:
                    if upgrade_level > upgrade_levels[upgrade_type]:
                        upgrade_levels[upgrade_type] = upgrade_level + 1
                else:
                    upgrade_levels[upgrade_type] = upgrade_level + 1
            return upgrade_levels

        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to get levels!</r>")
            return None

    def get_balance(self):
        try:
            response = self.http.get(
                url="/api/v1/profile/balance",
                domain="elb",
            )

            if response is None:
                self.log.error(f"<r>⭕ {self.account_name} failed to get balance!</r>")
                return None

            return response

        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to get balance!</r>")
            return None

    def claim(self):
        try:
            response = self.http.post(
                url="/api/v1/seed/claim",
                domain="elb",
                display_errors=False,
            )

            if response is None:
                # self.log.error(f"<r>⭕ {self.account_name} failed to claim!</r>")
                return None

            return response
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to claim!</r>")
            return None

    def upgrade(self, upgrade_type):
        if upgrade_type not in ["storage", "mining", "holy"]:
            return None
        if upgrade_type == "storage":
            url = "/api/v1/seed/storage-size/upgrade"
        elif upgrade_type == "mining":
            url = "/api/v1/seed/mining-speed/upgrade"
        elif upgrade_type == "holy":
            url = "/api/v1/upgrades/holy-water"
        try:
            response = self.http.post(
                url=url,
                domain="elb",
                display_errors=False,
            )
            if response is None:
                return None
            self.log.info(f"<g> {self.account_name} upgraded {upgrade_type} 🆙⬆️!</g>")
            return response
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to upgrade {upgrade_type}!</r>")
            return None

    def get_daily_checkin(self):
        try:
            response = self.http.post(
                url="/api/v1/login-bonuses",
                domain="elb",
                display_errors=False,
            )

            return response if response is not None else None

        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to get daily checkin!</r>")
            return None

    def hatch_egg(self, egg_id):
        try:
            response = self.http.post(
                url="/api/v1/egg-hatch/complete",
                domain="elb",
                data=json.dumps({"egg_id": egg_id}),
                display_errors=False,
            )

            return response if response is not None else None

        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to hatch egg!</r>")
            return None

    def get_first_egg_and_hatch(self):
        try:
            response = self.http.post(
                url="/api/v1/give-first-egg",
                domain="elb",
                display_errors=False,
            )
            if not response:
                return None
            egg_id = str(response["data"]["id"])
            hatchResponse = self.hatch_egg(egg_id)
            return hatchResponse

        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to get first egg!</r>")
            return None
