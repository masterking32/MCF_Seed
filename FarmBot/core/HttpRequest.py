# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

import json
import time
import requests


class HttpRequest:
    def __init__(
        self,
        log,
        proxy=None,
        user_agent=None,
        tgWebData=None,
        account_name=None,
    ):
        self.log = log
        self.proxy = proxy
        self.user_agent = user_agent
        self.game_url = {
            "elb": "https://elb.seeddao.org",
        }
        self.tgWebData = tgWebData
        self.account_name = account_name

        if not self.user_agent or self.user_agent == "":
            self.user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.3"

        if "windows" in self.user_agent.lower():
            self.log.warning(
                "🟡 <y>Windows User Agent detected, For safety please use mobile user-agent</y>"
            )

    def get(
        self,
        url,
        domain="elb",
        headers=None,
        send_option_request=True,
        valid_response_code=200,
        valid_option_response_code=204,
        auth_header=True,
        return_headers=False,
        display_errors=True,
        retries=3,
    ):
        try:
            url = self._fix_url(url, domain)
            default_headers = (
                self._get_default_headers() if "seeddao.org" in url else {}
            )

            if headers is None:
                headers = {}

            if auth_header and self.tgWebData:
                headers["telegram-data"] = self.tgWebData

            if headers:
                for key, value in headers.items():
                    default_headers[key] = value
            if send_option_request:
                self.options(
                    url=url,
                    method="GET",
                    headers=headers,
                    valid_response_code=valid_option_response_code,
                    display_errors=display_errors,
                )

            response = requests.get(
                url=url,
                headers=default_headers,
                proxies=self._get_proxy(),
                timeout=30,
            )
            if response.status_code != valid_response_code:
                if display_errors:
                    self.log.error(
                        f"🔴 <red> GET Request Error: <y>{url}</y> Response code: {response.status_code}</red>"
                    )
                return (None, None) if return_headers else None

            return (
                (response.json(), response.headers)
                if return_headers
                else response.json()
            )
        except Exception as e:
            if retries > 0:
                self.log.info(f"🟡 <y> Unable to send request, retrying...</y>")
                time.sleep(0.5)
                return self.get(
                    url=url,
                    domain=domain,
                    headers=headers,
                    send_option_request=send_option_request,
                    valid_response_code=valid_response_code,
                    valid_option_response_code=valid_option_response_code,
                    auth_header=auth_header,
                    return_headers=return_headers,
                    retries=retries - 1,
                    display_errors=display_errors,
                )
            if display_errors:
                self.log.error(f"🔴 <red> GET Request Error: <y>{url}</y> {e}</red>")
            return (None, None) if return_headers else None

    def post(
        self,
        url,
        domain="elb",
        data=None,
        headers=None,
        send_option_request=True,
        valid_response_code=200,
        valid_option_response_code=204,
        auth_header=True,
        return_headers=False,
        only_json_response=True,
        display_errors=True,
        retries=3,
    ):
        try:
            url = self._fix_url(url, domain)
            default_headers = (
                self._get_default_headers() if "seeddao.org" in url else {}
            )

            if headers is None:
                headers = {}

            if auth_header and self.tgWebData:
                headers["telegram-data"] = self.tgWebData

            if headers:
                for key, value in headers.items():
                    default_headers[key] = value

            if send_option_request:
                self.options(
                    url=url,
                    method="POST",
                    headers=headers,
                    valid_response_code=valid_option_response_code,
                    display_errors=display_errors,
                )
            response = None

            if data:
                response = requests.post(
                    url=url,
                    headers=default_headers,
                    data=data,
                    proxies=self._get_proxy(),
                    timeout=30,
                )
            else:
                response = requests.post(
                    url=url,
                    headers=default_headers,
                    proxies=self._get_proxy(),
                    timeout=30,
                )

            if response.status_code != valid_response_code:
                if display_errors:
                    self.log.error(
                        f"🔴 <red> POST Request Error: <y>{url}</y> Response code: {response.status_code}</red>"
                    )
                return (None, None) if return_headers else None

            if (
                "application/json" not in response.headers.get("Content-Type", "")
                and only_json_response is False
            ):
                return (
                    (response.text, response.headers)
                    if return_headers
                    else response.text
                )

            return (
                (response.json(), response.headers)
                if return_headers
                else response.json()
            )
        except Exception as e:
            if retries > 0:
                self.log.info(f"🟡 <y> Unable to send request, retrying...</y>")
                time.sleep(0.5)
                return self.post(
                    url=url,
                    domain=domain,
                    data=data,
                    headers=headers,
                    send_option_request=send_option_request,
                    valid_response_code=valid_response_code,
                    valid_option_response_code=valid_option_response_code,
                    auth_header=auth_header,
                    return_headers=return_headers,
                    only_json_response=only_json_response,
                    display_errors=display_errors,
                    retries=retries - 1,
                )

            if display_errors:
                self.log.error(f"🔴 <red> POST Request Error: <y>{url}</y> {e}</red>")
            return (None, None) if return_headers else None

    def options(
        self,
        url,
        domain=None,
        method="POST",
        headers=None,
        valid_response_code=204,
        display_errors=True,
        retries=3,
    ):
        try:
            url = self._fix_url(url, domain)
            default_headers = (
                self._get_get_option_headers(headers, method)
                if "seeddao.org" in url
                else {}
            )

            if headers is None:
                headers = {}

            if headers:
                for key, value in headers.items():
                    default_headers[key] = value

            response = requests.options(
                url=url,
                headers=default_headers,
                proxies=self._get_proxy(),
                timeout=30,
            )

            if response.status_code != valid_response_code:
                if display_errors:
                    self.log.error(
                        f"🔴 <red> OPTIONS Request Error: <y>{url}</y> Response code: {response.status_code}</red>"
                    )
                return None

            return True
        except Exception as e:
            if retries > 0:
                self.log.info(f"🟡 <y> Unable to send option request, retrying...</y>")
                time.sleep(0.5)
                return self.options(
                    url=url,
                    domain=domain,
                    method=method,
                    headers=headers,
                    valid_response_code=valid_response_code,
                    display_errors=display_errors,
                    retries=retries - 1,
                )
            if display_errors:
                self.log.error(
                    f"🔴 <red> OPTIONS Request Error: <y>{url}</y> {e}</red>"
                )
            return None

    def _get_proxy(self):
        if self.proxy:
            return {"http": self.proxy, "https": self.proxy}

        return None

    def _fix_url(self, url, domain=None):
        if url.startswith("http") or domain is None:
            return url

        game_url = self.game_url.get(domain)
        if not game_url:
            return url

        if url.startswith("/"):
            return f"{game_url}{url}"

        return f"{game_url}/{url}"

    def _get_default_headers(self):
        headers = {
            "accept": "*/*",
            "Origin": "https://cf.seeddao.org",
            "priority": "u=1, i",
            "referer": "https://cf.seeddao.org/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": self.user_agent,
            "pragma": "u=1, i",
            "Lang": "en",
            "cache-control": "no-cache",
            "Content-Type": "application/json",
        }

        if "android" in self.user_agent.lower():
            headers["Sec-CH-UA-Platform"] = '"Android"'
            headers["Sec-CH-UA-Mobile"] = "?1"
            headers["Sec-CH-UA"] = (
                '"Chromium";v="128", "Not;A=Brand";v="24", "Android WebView";v="128"'
            )
            headers["X-Requested-With"] = "org.telegram.messenger"

        return headers

    def _get_get_option_headers(self, headers=None, method="GET"):
        default_headers = {
            "accept": "*/*",
            "Origin": "https://cf.seeddao.org",
            "priority": "u=1, i",
            "referer": "https://cf.seeddao.org/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": self.user_agent,
            "pragma": "u=1, i",
            "cache-control": "no-cache",
            "access-control-request-method": method,
            "access-control-request-headers": "",
        }

        if not headers:
            return default_headers

        if "telegram-data" in headers:
            default_headers["access-control-request-headers"] = (
                default_headers["access-control-request-headers"] + "telegram-data"
            )

        return default_headers
