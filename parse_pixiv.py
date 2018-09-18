from pixivpy3 import *
import json
import sys
import csv

if __name__ == '__main__':
    args = sys.argv
    user_id = args[1]
    password = args[2]
    user_num = int(args[3])

    illust_count = 0
    illust_total_view = 0
    illust_total_bookmark = 0
    illust_total_comments = 0
    each_illusts = []

    if len(args) > 3:
        api = AppPixivAPI()
        api.login(user_id, password)   # Not required

        json_result = api.user_illusts(user_num)
        for illust in json_result.illusts:
            print(illust.keys())
            illust_count = illust_count + 1
            illust_total_view = illust_total_view + illust.total_view
            illust_total_bookmark = illust_total_bookmark + illust.total_bookmarks
            illust_total_comments = illust_total_comments + illust.total_comments
            each_illusts.append(
            {
                "id": illust.id,
                "view": illust.total_view,
                "bookmark": illust.total_bookmarks,
                "comments": illust.total_comments,
                "url": illust.image_urls['large']
            })

        next_url = json_result.next_url
        flag = 0

        while flag == 0:
            try:
                next_qs = api.parse_qs(next_url)
                next_result = api.user_illusts(**next_qs)

                for illust in next_result.illusts:
                    illust_count = illust_count + 1
                    illust_total_view = illust_total_view + illust.total_view
                    illust_total_bookmark = illust_total_bookmark + illust.total_bookmarks
                    illust_total_comments = illust_total_comments + illust.total_comments
                    each_illusts.append(
                    {
                        "id": illust.id,
                        "view": illust.total_view,
                        "bookmark": illust.total_bookmarks,
                        "comments": illust.total_comments,
                        "url": illust.image_urls['large']
                    })
                next_url = next_result.next_url
                print(next_url)
            except Exception as e:
                print("end")
                flag = 1
    print(illust_count)
    print(illust_total_view)
    print(illust_total_bookmark)
    print(illust_total_comments)

    f = open("output.json", "w")
    json.dump(each_illusts, f, ensure_ascii=False)
