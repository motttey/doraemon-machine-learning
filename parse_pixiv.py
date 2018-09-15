from pixivpy3 import *
import json
import sys

if __name__ == '__main__':
    args = sys.argv
    user_id = args[1]
    password = args[2]
    user_num = int(args[3])

    illust_num = 0
    total_view = 0
    total_bookmark = 0

    api = AppPixivAPI()
    api.login(user_id, password)   # Not required

    json_result = api.user_illusts(user_num)
    for illust in json_result.illusts:
        print(illust.total_view)
    next_url = json_result.next_url
    flag = 0

    while flag == 0:
        try:
            next_qs = api.parse_qs(next_url)
            next_result = api.user_illusts(**next_qs)

            for illust in next_result.illusts:
                print(illust.total_view)
            next_url = next_result.next_url
            print(next_url)
        except Exception as e:
            print("end")
            flag = 1
