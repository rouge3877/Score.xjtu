import json

import requests
from bs4 import BeautifulSoup

HEAD = {
    "Host": "jwapp.xjtu.edu.cn",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Content-Type": "application/json;charset=UTF-8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
}


#  curl -X POST "http://jwapp.xjtu.edu.cn/api/biz/v410/score/termScore" \
# -H "Authorization: eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6InB2c3VtNzNpNXVnMXJxZzU5cjFsanQ3cnZ1In0.mIxHXSbUcAnIPB3XrodAYK8QrJ5fw17QN567W-eCwoXu3rlDzmUsz-IqD6cQbOZsS8farM-8064g0ttUNFgHZQ" \
# -H "Content-Type: application/json;charset=UTF-8" \
# -d '{"termCode":"2024-2025-1"}'

def get_score(token, term_code):
    url = "http://jwapp.xjtu.edu.cn/api/biz/v410/score/termScore"

    headers = HEAD.copy()
    headers["Authorization"] = token
    data = {
        "termCode": term_code,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_user_info(token):
    """
    Get user info from the server.
    :param token: token
    :return: user info
    """
    url = "http://jwapp.xjtu.edu.cn/api/biz/v410/user/info"
    headers = HEAD.copy()
    headers["Authorization"] = token
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_token(stu_no: str) -> str:
    """
    Get the token from the server.
    :param stu_no: Student number
    :return: token
    """
    response = requests.get(
        "http://jwapp.xjtu.edu.cn/app/index",
        params={"code": "1", "employeeNo": stu_no},
        headers=HEAD,
        allow_redirects=False,
    )
    if response.status_code == 302:
        return response.headers["Location"].split("token=")[1]
    else:
        return None

def get_score_by_stu_no(stu_no: str, term_code: str) -> dict:
    """
    Get the score by student number and term code.
    :param stu_no: Student number
    :param term_code: Term code
    :return: score
    """
    token = get_token(stu_no)
    if token is None:
        return None

    score = get_score(token, term_code)
    if score is None:
        return None

    return score

if __name__ == "__main__":
    import sys
    import os

    if len(sys.argv) != 2:
        print("Usage: python get.py <stu_no>")
        sys.exit(1)
    stu_no = sys.argv[1]


    auth = get_token(stu_no)
    info = get_user_info(auth)
    print(f"User info: {info}")

    terms_list = [
        "2024-2025-1",
        "2023-2024-3",
        "2023-2024-2",
        "2023-2024-1",
        "2022-2023-3",
        "2022-2023-2",
        "2022-2023-1",
            ]

    for term in terms_list:
        print(f"Getting score for {stu_no} in {term}...")
        score = get_score_by_stu_no(stu_no, term)
        if score is None:
            print("Failed to get score.")
            continue

        # Save the score to a file
        with open(f"{stu_no}_{term}.json", "w") as f:
            json.dump(score, f, ensure_ascii=False, indent=4)
        print(f"Score saved to {stu_no}_{term}.json")


