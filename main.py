import os
import time
import requests
import stdiomask
from colorama import Fore, init

os.system('cls')
init(autoreset=True)
session = requests.Session()


class StoryViewer:
    def __init__(self):
        pass

    def login(self, username, password):
        url = "https://www.instagram.com/accounts/login/ajax/"

        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "x-csrftoken": "tZ27MmTvcjiVvkV4aU4h14zCqo7KoIuB",
            "content-type": "application/x-www-form-urlencoded"
        }

        data = {
            "enc_password": "#PWD_INSTAGRAM_BROWSER:0:1662314579:" + password,
            "username": username,
            "queryParams": "{}",
            "optIntoOneTap": "false"
        }

        login = session.post(url, headers=headers, data=data)
        session.cookies = login.cookies

        if 'userId' in login.text:
            print(f"{Fore.LIGHTGREEN_EX}[+] Successfully Logged In{Fore.RESET}")
            time.sleep(2)
        else:
            print(f"{Fore.LIGHTGREEN_EX}[-] Wrong Username/Password{Fore.RESET}")
            time.sleep(3)
            exit()

        os.system('cls')

    def view_stories(self, target):
        headers = {
            "user-agent": "Instagram 85.0.0.21.100 Android (28/9; 380dpi; 1080x2147; OnePlus; HWEVA; OnePlus6T; qcom; en_US; 146536611)",
            "x-csrftoken": "fbMty08hNS2evXP6EB4IsnFqoIUjGPB7",
        }

        target_info_url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={target}"
        target_info = session.get(target_info_url, headers=headers)
        userId = target_info.json()["data"]["user"]["id"]

        get_stories_url = f"https://i.instagram.com/api/v1/feed/reels_media/?reel_ids={userId}"
        stories_info = session.get(get_stories_url, headers=headers)
        stories_ids = stories_info.json()["reels"][userId]["media_ids"]

        count = 0
        for story in stories_ids:
            
            url = "https://i.instagram.com/api/v1/stories/reel/seen"
            data = {
                "reelMediaId": f"{story}",
                "reelMediaOwnerId": f"{userId}",
                "reelId": f"{userId}",
                "reelMediaTakenAt": f"{int(time.time())}",
                "viewSeenAt": f"{int(time.time())}",
            }
            view_response = session.post(url, headers=headers, data=data)

            if view_response.status_code == 200:
                count += 1
                print(f"{Fore.LIGHTGREEN_EX}Viewed Story: {count} [Current Owner: {target}] {Fore.RESET}")
            else:
                print(f"{Fore.LIGHTRED_EX}[ERROR] No stories were found.")

story_viewer = StoryViewer()



def main():
    targets = None
    with open("targets.txt", "r") as reader:
        targets = reader.readlines()

    username = input(f"{Fore.LIGHTGREEN_EX}[+] Username: {Fore.RESET}")
    password = stdiomask.getpass(prompt=f"{Fore.LIGHTGREEN_EX}[+] Password: {Fore.RESET}", mask='*')

    story_viewer.login(username=username, password=password)

    while True:
        for target in targets:
            story_viewer.view_stories(target=target)
            time.sleep(20)


main()
