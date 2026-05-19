import requests
import os
import re
import socket
import time
import base64
from concurrent.futures import ThreadPoolExecutor

# =========================
# НАСТРОЙКИ
# =========================

GITHUB_USER = os.getenv("GH_USER")
REPO_NAME = os.getenv("GH_REPO")
TOKEN = os.getenv("GH_TOKEN6")

FILE_PATH = "mini.txt"

SOURCES = [
    "https://gist.githubusercontent.com/flaafix/c79a81037d15163360571c7a7331b153/raw/AetrisVPN.txt"
]

BANNED_COUNTRIES = ['RU', 'CN', 'KP', 'IR']

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# =========================
# СТРАНЫ
# =========================

RU_COUNTRIES = {
    "US": "США",
    "DE": "Германия",
    "NL": "Нидерланды",
    "FI": "Финляндия",
    "TR": "Турция",
    "KZ": "Казахстан",
    "FR": "Франция",
    "GB": "Великобритания",
    "PL": "Польша",
    "SG": "Сингапур",
    "HK": "Гонконг",
    "SE": "Швеция",
    "AT": "Австрия",
    "BY": "Беларусь",
    "UA": "Украина",
    "JP": "Япония",
    "CA": "Канада",
    "CH": "Швейцария",
    "NO": "Норвегия",
    "IT": "Италия",
    "ES": "Испания",
    "CZ": "Чехия",
    "RO": "Румыния",
    "BG": "Болгария",
    "HU": "Венгрия",
    "DK": "Дания",
    "BE": "Бельгия",
    "IE": "Ирландия",
    "PT": "Португалия",
    "GR": "Греция",
    "LT": "Литва",
    "LV": "Латвия",
    "EE": "Эстония",
    "SK": "Словакия",
    "SI": "Словения",
    "HR": "Хорватия",
    "KR": "Южная Корея",
    "TW": "Тайвань",
    "AE": "ОАЭ",
    "IN": "Индия",
    "AU": "Австралия",
    "BR": "Бразилия",
    "MX": "Мексика"
}

# =========================
# PING
# =========================

def get_ping(host, port):

    try:

        ip = socket.gethostbyname(host)

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.settimeout(5)

        start = time.time()

        result = sock.connect_ex((ip, port))

        ping = int((time.time() - start) * 1000)

        sock.close()

        if result == 0:
            return ping

    except:
        pass

    return None

# =========================
# COUNTRY
# =========================

def get_country_info(host):

    try:

        ip = socket.gethostbyname(host)

        r = requests.get(
            f"https://ipwho.is/{ip}",
            headers=HEADERS,
            timeout=10
        )

        data = r.json()

        if not data.get("success"):
            return "UN", "Сервер"

        code = data.get("country_code")

        if not code:
            return "UN", "Сервер"

        if code in BANNED_COUNTRIES:
            return None, None

        country = RU_COUNTRIES.get(code, code)

        return code, country

    except:
        return "UN", "Сервер"

# =========================
# PROCESS
# =========================

def process_key(key):

    try:

        key = key.strip()

        if not key:
            return None

        main_part = key.split('#')[0]

        host_match = re.search(
            r'@([^:/?#\s]+):?(\d+)?',
            main_part
        )

        if not host_match:
            return None

        host = host_match.group(1)

        try:
            port = int(host_match.group(2))
        except:
            port = 443

        ping = get_ping(host, port)

        if ping is None:
            return None

        code, country = get_country_info(host)

        if not code:
            return None

        if code == "UN":
            emoji = "🚀"
        else:
            emoji = "".join(
                chr(127397 + ord(c))
                for c in code.upper()
            )

        return {
            "main": main_part,
            "emoji": emoji,
            "country": country,
            "ping": ping
        }

    except:
        return None

# =========================
# GITHUB
# =========================

def update_repo(content):

    url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{FILE_PATH}"

    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    sha = None

    try:

        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            sha = r.json().get("sha")

    except:
        pass

    encoded = base64.b64encode(
        content.encode("utf-8")
    ).decode("utf-8")

    payload = {
        "message": f"Mini Update {time.strftime('%H:%M:%S')}",
        "content": encoded,
        "branch": "main"
    }

    if sha:
        payload["sha"] = sha

    requests.put(
        url,
        headers=headers,
        json=payload
    )

# =========================
# MAIN
# =========================

def run_once():

    all_keys = []

    for src in SOURCES:

        try:

            r = requests.get(
                src,
                headers=HEADERS,
                timeout=15
            )

            found = re.findall(
                r'(?:vless|vmess|trojan|ss|hysteria2?)://[^\s]+',
                r.text
            )

            all_keys.extend(found)

        except:
            continue

    unique_keys = list(set(all_keys))

    with ThreadPoolExecutor(max_workers=30) as executor:

        results = list(
            filter(
                None,
                executor.map(process_key, unique_keys)
            )
        )

    results.sort(
        key=lambda x: (
            x["country"],
            x["ping"]
        )
    )

    final = []

    counts = {}

    for item in results[:200]:

        country = item["country"]

        counts[country] = counts.get(country, 0) + 1

        line = (
            f"{item['main']}"
            f"#{item['emoji']} "
            f"{country} "
            f"#{counts[country]} "
            f"| @halyava_vpnx"
        )

        final.append(line)

    header = (
        "#profile-title: Халява ВПН | Mini 🎁\n"
        "#profile-update-interval: 12\n"
        "#subscription-userinfo: expire=5774966400; total=10995116277760; used=0\n"
        "#profile-web-page-url: https://t.me/halyava_vpnx\n"
        "#announce: Спасибо вам за 5000 подписчиков ❤️ @halyava_vpnx\n\n"
    )

    update_repo(
        header + "\n".join(final)
    )

    print(f"DONE: {len(final)} configs")

if __name__ == "__main__":
    run_once()
