import requests
from urllib import parse

# 닉네임으로 encryptId 찾기
def encrypt(DEVELOPMENTAPIKEY,summonerName):
    encodingSummonerName = parse.quote(summonerName)
    APIURL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + encodingSummonerName
    headers = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": DEVELOPMENTAPIKEY,
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
        }
    res = requests.get(APIURL, headers=headers)
    data = res.json()
    # print(data)
    print('encryptId: '+ str(data["id"]))
    return data["id"]

# encryptId로 티어 구하기
def getTier(DEVELOPMENTAPIKEY,summonerName):
    encryptedId = encrypt(DEVELOPMENTAPIKEY,summonerName)
    headers = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": DEVELOPMENTAPIKEY,
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
        }
    APIURL = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + encryptedId
    res = requests.get(APIURL, headers=headers)
    data = res.json()
    return data[0]["tier"]

# PUUID 구해야하나?
def PUUID(DEVELOPMENTAPIKEY,summonerName):
    encodingSummonerName = parse.quote(summonerName)
    APIURL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + encodingSummonerName
    headers = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": DEVELOPMENTAPIKEY,
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
        }
    res = requests.get(APIURL, headers=headers)
    data = res.json()
    # print(data)
    # print('ppuid: '+ str(data["puuid"]))
    return data["puuid"]


APIKEY = "API_KEY"
nickName = "HIDE ON BUSH"

print(getTier(APIKEY,nickName))
print(PUUID(APIKEY,nickName))


