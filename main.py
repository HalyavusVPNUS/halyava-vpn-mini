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
    "AF": "Афганистан",
    "AL": "Албания",
    "DZ": "Алжир",
    "AS": "Американское Самоа",
    "AD": "Андорра",
    "AO": "Ангола",
    "AI": "Ангилья",
    "AQ": "Антарктида",
    "AG": "Антигуа и Барбуда",
    "AR": "Аргентина",
    "AM": "Армения",
    "AW": "Аруба",
    "AU": "Австралия",
    "AT": "Австрия",
    "AZ": "Азербайджан",

    "BS": "Багамы",
    "BH": "Бахрейн",
    "BD": "Бангладеш",
    "BB": "Барбадос",
    "BY": "Беларусь",
    "BE": "Бельгия",
    "BZ": "Белиз",
    "BJ": "Бенин",
    "BM": "Бермуды",
    "BT": "Бутан",
    "BO": "Боливия",
    "BA": "Босния и Герцеговина",
    "BW": "Ботсвана",
    "BR": "Бразилия",
    "BN": "Бруней",
    "BG": "Болгария",
    "BF": "Буркина-Фасо",
    "BI": "Бурунди",

    "KH": "Камбоджа",
    "CM": "Камерун",
    "CA": "Канада",
    "CV": "Кабо-Верде",
    "KY": "Каймановы острова",
    "CF": "ЦАР",
    "TD": "Чад",
    "CL": "Чили",
    "CN": "Китай",
    "CO": "Колумбия",
    "KM": "Коморы",
    "CG": "Конго",
    "CR": "Коста-Рика",
    "HR": "Хорватия",
    "CU": "Куба",
    "CY": "Кипр",
    "CZ": "Чехия",

    "DK": "Дания",
    "DJ": "Джибути",
    "DM": "Доминика",
    "DO": "Доминиканская Республика",

    "EC": "Эквадор",
    "EG": "Египет",
    "SV": "Сальвадор",
    "GQ": "Экваториальная Гвинея",
    "ER": "Эритрея",
    "EE": "Эстония",
    "ET": "Эфиопия",

    "FJ": "Фиджи",
    "FI": "Финляндия",
    "FR": "Франция",

    "GA": "Габон",
    "GM": "Гамбия",
    "GE": "Грузия",
    "DE": "Германия",
    "GH": "Гана",
    "GI": "Гибралтар",
    "GR": "Греция",
    "GL": "Гренландия",
    "GD": "Гренада",
    "GU": "Гуам",
    "GT": "Гватемала",
    "GN": "Гвинея",
    "GW": "Гвинея-Бисау",
    "GY": "Гайана",

    "HT": "Гаити",
    "HN": "Гондурас",
    "HK": "Гонконг",
    "HU": "Венгрия",

    "IS": "Исландия",
    "IN": "Индия",
    "ID": "Индонезия",
    "IR": "Иран",
    "IQ": "Ирак",
    "IE": "Ирландия",
    "IL": "Израиль",
    "IT": "Италия",

    "JM": "Ямайка",
    "JP": "Япония",
    "JO": "Иордания",

    "KZ": "Казахстан",
    "KE": "Кения",
    "KI": "Кирибати",
    "KP": "Северная Корея",
    "KR": "Южная Корея",
    "KW": "Кувейт",
    "KG": "Кыргызстан",

    "LA": "Лаос",
    "LV": "Латвия",
    "LB": "Ливан",
    "LS": "Лесото",
    "LR": "Либерия",
    "LY": "Ливия",
    "LI": "Лихтенштейн",
    "LT": "Литва",
    "LU": "Люксембург",

    "MO": "Макао",
    "MK": "Северная Македония",
    "MG": "Мадагаскар",
    "MW": "Малави",
    "MY": "Малайзия",
    "MV": "Мальдивы",
    "ML": "Мали",
    "MT": "Мальта",
    "MH": "Маршалловы острова",
    "MQ": "Мартиника",
    "MR": "Мавритания",
    "MU": "Маврикий",
    "MX": "Мексика",
    "FM": "Микронезия",
    "MD": "Молдова",
    "MC": "Монако",
    "MN": "Монголия",
    "ME": "Черногория",
    "MA": "Марокко",
    "MZ": "Мозамбик",
    "MM": "Мьянма",

    "NA": "Намибия",
    "NR": "Науру",
    "NP": "Непал",
    "NL": "Нидерланды",
    "NZ": "Новая Зеландия",
    "NI": "Никарагуа",
    "NE": "Нигер",
    "NG": "Нигерия",
    "NO": "Норвегия",

    "OM": "Оман",

    "PK": "Пакистан",
    "PW": "Палау",
    "PS": "Палестина",
    "PA": "Панама",
    "PG": "Папуа — Новая Гвинея",
    "PY": "Парагвай",
    "PE": "Перу",
    "PH": "Филиппины",
    "PL": "Польша",
    "PT": "Португалия",
    "PR": "Пуэрто-Рико",

    "QA": "Катар",

    "RO": "Румыния",
    "RU": "Россия",
    "RW": "Руанда",

    "KN": "Сент-Китс и Невис",
    "LC": "Сент-Люсия",
    "VC": "Сент-Винсент и Гренадины",
    "WS": "Самоа",
    "SM": "Сан-Марино",
    "ST": "Сан-Томе и Принсипи",
    "SA": "Саудовская Аравия",
    "SN": "Сенегал",
    "RS": "Сербия",
    "SC": "Сейшелы",
    "SL": "Сьерра-Леоне",
    "SG": "Сингапур",
    "SK": "Словакия",
    "SI": "Словения",
    "SB": "Соломоновы острова",
    "SO": "Сомали",
    "ZA": "ЮАР",
    "ES": "Испания",
    "LK": "Шри-Ланка",
    "SD": "Судан",
    "SR": "Суринам",
    "SZ": "Эсватини",
    "SE": "Швеция",
    "CH": "Швейцария",
    "SY": "Сирия",

    "TW": "Тайвань",
    "TJ": "Таджикистан",
    "TZ": "Танзания",
    "TH": "Таиланд",
    "TL": "Тимор-Лесте",
    "TG": "Того",
    "TO": "Тонга",
    "TT": "Тринидад и Тобаго",
    "TN": "Тунис",
    "TR": "Турция",
    "TM": "Туркменистан",
    "TV": "Тувалу",

    "UG": "Уганда",
    "UA": "Украина",
    "AE": "ОАЭ",
    "GB": "Великобритания",
    "US": "США",
    "UY": "Уругвай",
    "UZ": "Узбекистан",

    "VU": "Вануату",
    "VA": "Ватикан",
    "VE": "Венесуэла",
    "VN": "Вьетнам",

    "YE": "Йемен",

    "ZM": "Замбия",
    "ZW": "Зимбабве"
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

    # =========================
    # СОРТИРОВКА
    # =========================

    results.sort(
        key=lambda x: (
            x["country"],
            x["ping"]
        )
    )

    # =========================
    # ГРУППИРОВКА
    # =========================

    grouped = {}

    for item in results[:200]:

        country = item["country"]

        if country not in grouped:
            grouped[country] = []

        grouped[country].append(item)

    # =========================
    # ФИНАЛ
    # =========================

    final = []

    for country in sorted(grouped.keys()):

        servers = grouped[country]

        for idx, item in enumerate(servers, 1):

            line = (
                f"{item['main']}"
                f"#{item['emoji']} "
                f"{country} "
                f"#{idx}"
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
