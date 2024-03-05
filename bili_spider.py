import requests
import time
import pandas as pd
import re

# 日期转换函数
def trans_data(timeStamp):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

def search_bilibili(keyword, max_page, out_file):
    for page in range(1, max_page + 1):
        print('正在爬取第', page, '页')
        # 构建请求URL和查询参数
        url = 'https://api.bilibili.com/x/web-interface/search/type'
        headers = {
            # 请确保以下headers包括User-Agent和Cookie是最新的
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            # 更新你的Cookie值
            'Cookie': "buvid3=83B979CF-3BC6-32E3-22D3-964861D3AC8321559infoc; b_nut=1708959821; i-wanna-go-back=-1; b_ut=7; _uuid=1351059F9-10271-5883-DC32-931DA5B3223126186infoc; enable_web_push=DISABLE; header_theme_version=CLOSE; DedeUserID=9552818; DedeUserID__ckMd5=b4c870f95007b415; hit-dyn-v2=1; CURRENT_FNVAL=4048; rpdid=|(J|)k)J)JuR0J'u~|m|JY|Jk; CURRENT_QUALITY=80; FEED_LIVE_VERSION=V8; buvid_fp_plain=undefined; buvid4=DC388901-AC12-FF04-8BC5-36EA28462B6D25168-024022615-DtgSrDL24kcpC%2Fs4auvC7Q%3D%3D; SESSDATA=1322a8ee%2C1725080477%2Ce3447%2A31CjAN73qBSUwbhhnLO6pi9sFp8yh6brppsAd_S7fuT-5XVYTt8X99N1lmbQmaqpQB46MSVkZQcmc1Z2pRUy02d0hNc2JTdm44NDNKQ1Q5MV9UUTZ1dHphSzU1aWt4d294TlUxZy1DNndCTzh1YUgyM19rR3BuOWplSkhacWFDeE1FeUhuOHM0dnNRIIEC; bili_jct=67e068afc842b0e79079b491accf9e83; home_feed_column=4; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDk4NzI4NjgsImlhdCI6MTcwOTYxMzYwOCwicGx0IjotMX0.k5aKAapMZ3tu62GuMybeR386xwZLnjg4CPmsHagPSTY; bili_ticket_expires=1709872808; fingerprint=8d846a880e718f07d071627a9ac7f1f9; PVID=3; b_lsid=99771D39_18E0E4C5423; sid=6kt9e1co; buvid_fp=8d846a880e718f07d071627a9ac7f1f9; bp_video_offset_9552818=905375382297903141; browser_resolution=794-634",
        }
        params = {
            'search_type': 'video',
            'keyword': keyword,
            'page': page,
        }

        try:
            r = requests.get(url, headers=headers, params=params)
            # 确保响应状态码为200
            if r.status_code == 200:
                j_data = r.json()
                data_list = j_data['data']['result']
                print('数据长度', len(data_list))

                # 解析并收集数据
                collected_data = []
                for data in data_list:
                    title = re.compile(r'<[^>]+>', re.S).sub('', data['title'])  # 清理标题中的HTML标签
                    collected_data.append({
                        '标题': title,
                        '作者': data['author'],
                        'bvid': data['bvid'],
                        '上传时间': trans_data(data['pubdate']),
                        '视频时长': data['duration'],
                        '弹幕数': data.get('video_review', 0),  # 如果键不存在，则默认为0
                        '点赞数': data.get('like', 0),  # 如果键'like'不存在，这里您需要确认正确的键或逻辑
                        '播放量': data['play'],
                        '收藏量': data['favorites'],
                        '分区类型': data['typename'],
                        '标签': data['tag'],
                        '描述': data['description'],
                    })

                # 将数据保存到DataFrame然后输出到CSV文件
                df = pd.DataFrame(collected_data)
                with open(out_file, 'a', encoding='utf-8-sig', newline='') as f:
                    df.to_csv(f, index=False, header=f.tell()==0)

                print(f'第{page}页爬取完成。')
            else:
                print(f'请求失败，状态码：{r.status_code}')
        except Exception as e:
            print('发生错误:', e)

        time.sleep(1)  # 添加延迟以减少被封的风险

if __name__ == '__main__':
    search_keyword = '指环王'
    max_page = 2
    result_file = 'b站_指环王_搜索结果_前2页.csv'
    search_bilibili(search_keyword, max_page, result_file)
