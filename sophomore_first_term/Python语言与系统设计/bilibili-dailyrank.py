import requests
from bs4 import BeautifulSoup


def bs_parse_video(html, video_list=None) -> object:
    video_list = []
    soup = BeautifulSoup(html, "html.parser")
    # 查找所有class属性为title的标签
    div_list = soup.find_all('a', class_="title")
    # 获取每个链接
    for each in div_list:
        video = each.get('href')
        video_list.append(video)

    return video_list


def get_video(name):
    #网页视频分区组成
    link = 'https://www.bilibili.com/v/popular/rank/' + name
    r = requests.get(link)
    if 200 != r.status_code:
        return None
    #返回文本信息
    return bs_parse_video(r.text)


def bs_parse_data(html, video_list=None) -> object:
    soup = BeautifulSoup(html, "html.parser")
    # 查找所有class属性为ops的div标签
    div = soup.find_all('div', class_="ops")
    div2 = soup.find_all('div', class_="video-data")
    # 判断视频是否已失效
    div_error = soup.find_all('div', class_="error-body")
    if div_error:
        return []
    #ops中的信息
    if div:
        # 获取点赞，投币，收藏与分享数
        like = div[0].find('span', class_="like").get_text()
        like = like[:-5]  # 去除无效字符
        coin = div[0].find('span', class_="coin").get_text()
        coin = coin[7:-5]
        collect = div[0].find('span', class_="collect").get_text()
        collect = collect[:-5]
        share = div[0].find('span', class_="share").get_text()
        share = share[:-7]
        a = [like, coin, collect, share]
    else:
        a = []
    #videodata中的信息
    if div2:
        # 获取播放量与弹幕数
        view = div2[0].find('span', class_="view").get_text()
        view = view[:-5]
        dm = div2[0].find('span', class_="dm").get_text()
        dm = dm[:-2]
        b = [view, dm]
    else:
        b = []

    return [a, b]

    #链接地址
def get_data(link):
    links = 'https:' + link
    r = requests.get(links)
    if 200 != r.status_code:
        return None

    return bs_parse_data(r.text)


fenqu = ["all", "guochuang", "music", "douga", "dance", "game", "technology", "digital", "life", "food", "kichiku",
         "fashion", "ent","cinephile", "origin", "rookie"]
data_list = []  # 储存已得到的数据
output = open('bili1.xlsx', 'w')
output.write('分区\t链接\t点赞\t硬币\t收藏\t分享\t播放量\t弹幕数量\n')
for name in fenqu:
    movies = get_video(name)
    for link in movies:
        data = get_data(link)
        link = link[2:]
        data_list.append([name, link, data])
        print([name, link, data])
        if data:
            if (data[0] != []) & (data[1] != []):
                # 按格式读出到excel文件
                output.write(str(name))
                output.write('\t')
                output.write(str(link))
                output.write('\t')
                output.write(str(data[0][0]))
                output.write('\t')
                output.write(str(data[0][1]))
                output.write('\t')
                output.write(str(data[0][2]))
                output.write('\t')
                output.write(str(data[0][3]))
                output.write('\t')
                output.write(str(data[1][0]))
                output.write('\t')
                output.write(str(data[1][1]))
                output.write('\n')
            output.flush()
output.close()
