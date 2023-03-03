import requests
import urllib.parse as parse
import csv

API_KEY = "AIzaSyAdx68gOfFZ5PPVQXLMHqTnB2r48Vs8jIA"
URL_HEAD = "https://www.googleapis.com/youtube/v3/commentThreads?"
nextPageToken = ''
item_count = 0
items_output = [
    ['videoId']+  # video ID
    ['textDisplay']+  # 編集後のコメント
    ['textOriginal']+  # 編集前のコメント
    ['likeCount']+  # いいね数
    ['publishedAt']+  # 更新日
    ['updatedAt']  # 最終更新日
]

#パラメータ設定
video_id = "ppVPgoiDRdU"
# channelId = "チャンネルID"
exe_num = 1

for i in range(exe_num):

    #APIパラメータセット
    param = {
        'key':API_KEY,
        'part':'snippet',
        #----↓フィルタ（いずれか1つ）↓-------
        #'allThreadsRelatedToChannelId':channelId,
        'videoId':video_id,
        #----↑フィルタ（いずれか1つ）↑-------
        'maxResults':'100',
        'moderationStatus':'published',
        'order':'relevance',
        'pageToken':nextPageToken,
        'searchTerms':'',
        'textFormat':'plainText',
    }
    #リクエストURL作成
    target_url = URL_HEAD + (parse.urlencode(param))

    #データ取得
    res = requests.get(target_url).json()

    #件数
    item_count += len(res['items'])

    #print(target_url)
    print(str(item_count)+"件")

    #コメント情報を変数に格納
    for item in res['items']:
        items_output.append(
            [str(item['snippet']['topLevelComment']['snippet']['videoId'])]+
            [str(item['snippet']['topLevelComment']['snippet']['textDisplay'].replace('\n', ''))]+
            [str(item['snippet']['topLevelComment']['snippet']['textOriginal'])]+
            [str(item['snippet']['topLevelComment']['snippet']['likeCount'])]+
            [str(item['snippet']['topLevelComment']['snippet']['publishedAt'])]+
            [str(item['snippet']['topLevelComment']['snippet']['updatedAt'])]
        ) 

    #nextPageTokenがなくなったら処理ストップ
    if 'nextPageToken' in res:
        nextPageToken = res['nextPageToken']
    else:
        break

#CSVで出力
f = open('youtube-comments-list.csv', 'w', newline='', encoding='UTF-8')
writer = csv.writer(f)
writer.writerows(items_output)
f.close()