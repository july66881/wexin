import json
import random

import requests
import time
from datetime import datetime, timedelta, timezone


def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)


def weather(province, city):
    url = f'https://v0.yiketianqi.com/api?appid=15184581&appsecret=l87CZ3Ap&version=v62&province={province}&city={city}'
    headers = {'header': "Content-Type: application/json;charset=utf-8"}
    req = requests.get(url=url, headers=headers)
    reqtext = eval(req.text)
    weq = reqtext['wea']
    tem1 = reqtext['tem1']
    tem2 = reqtext['tem2']
    win = reqtext['win']
    win1 = reqtext['win_speed']
    return weq, tem1, tem2, win, win1



d1 = '2022-8-26'
times = datetime.now().astimezone(timezone(timedelta(hours=+8))).date()
year = int(times.year)+1
d2 = str(year) + '-1-19'
t = str(times).replace('-', '年', 1).replace('-', '月', 1) + '日'

# 日期差
date1 = datetime.strptime(d1, "%Y-%m-%d").date()
Days = str((times - date1).days)
# 生日
date2 = datetime.strptime(d2, "%Y-%m-%d").date()
hb = str((date2-times).days)

if hb != '365':
    daojishi = f'距离姐姐生日还有 {hb} 天!'
elif hb == '365':
    daojishi = '今天是大美女的生日！要每天开心哦！还有不要忘了我！'

if Days == '30':
    jn = '\n在一起一个月了，感觉怎么样? 哈哈哈!'
elif Days == '50':
    jn = '\n 在一起50天啦，加油，会永远爱你！'
elif Days == '100':
    jn = '\n今天恋爱100天纪念，满足你一个要求，过期不候!'
elif Days == '365':
    jn = '\n和你在一起满一年啦，好诶！想带你回家(认真脸)！'
else:
    jn = ''

d = times.weekday()
if d == 0:
    d = '星期一  Mon.'
elif d == 1:
    d = '星期二  Tue.'
elif d == 2:
    d = '星期三  Wed.'
elif d == 3:
    d = '星期四  Thur.'
elif d == 4:
    d = '星期五  Fn.'
elif d == 5:
    d = '星期六  Sat.'
elif d == 6:
    d = '星期七  Sun.'


def jiejari(day):
    req = requests.get(url='http://api.tianapi.com/jiejiari/index',
                       params={'key': 'f70ff9e841951175e95b90e8ca1231ed', 'date': day}).json()['newslist'][0]
    return req['name']


def verse():
    wea = weather('上海', '闵行')[0]
    s = {'风': 1, '云': 2, '雨': 3, '雪': 4, '霜': 5, '露': 6, '雾': 7, '雷': 8, '晴': 9, '阴': 10}
    keys = s.keys()

    for x in wea:
        if x in keys:
            tqtype = s.get(x)
            req = requests.get(url='http://api.tianapi.com/tianqishiju/index',
                               params={
                                   'key': 'f70ff9e841951175e95b90e8ca1231ed',
                                   'tqtype': tqtype
                               }).json()
            newslist = req['newslist'][0]
            return newslist['content'], newslist['author'], newslist['source']


def caihongpi():
    while True:
        req = requests.get(url='http://api.tianapi.com/caihongpi/index?key=f70ff9e841951175e95b90e8ca1231ed',
                           headers={'Content-Type': 'application/x-www-form-urlencoded'}).json()
        a = req['newslist'][0]['content']
        if len(a) < 50:
            return a.replace('XXX', '你')


def oneyg():
    while True:
        req = requests.get('http://api.tianapi.com/one/index', params={'key': 'f70ff9e841951175e95b90e8ca1231ed',
                                                                       'rand': '1'}).json()['newslist'][0]
        a = req['word']
        if len(a) < 60:
            return a


def send_message_ceshiVX(appid, secret, template_id, weat, province, city, userid):  # 默认发送给自己

    # 获取token
    response = requests.get(
        f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + appid + "&secret=" + secret)
    data = json.loads(response.text)
    access_token = data['access_token']
    a = ['好爱你','好想你','好喜欢你','想带你回家','想吃了你','每天都想你','不想离开你','每天都想亲亲','每天都想抱抱']
    payload = {'touser': userid, 'template_id': template_id,
               'url': 'https://www.yikm.net/',
               "topcolor": get_color(),
               'data': {'caihongpi': {'value': caihongpi(), 'color': get_color()},
                        'date': {'value': t + ' ' + d + '  ' + jiejari(times), 'color': get_color()},
                        'days': {'value': f'❤️今天是在一起的第{Days}天❤️+'\n'+❤️{random.choice(a)}❤️' + jn, 'color': '#FFC0CB'},
                        'daojishi': {'value': '❤️'+daojishi+'❤️', 'color': get_color()},
                        'citywea': {
                            'value': province + ' ' + city + '  ' + weat[0] + '  ' + weat[2] + '°C~' + weat[1] + '°C' +
                                     '  ' + weat[4] + weat[3], 'color': '#348781'},

                        # 'province': {'value': province},
                        # 'city': {'value': city, 'color': get_color()},
                        # 'tq': {'value': weat[0], 'color': get_color()},
                        # 'tem1': {'value': weat[2] + '°C' + ' ~ ' + weat[1] + '°C', 'color': get_color()},
                        # 'win': {'value': weat[3]},
                        # 'win1': {'value': weat[4],'color': get_color()},
                        'verse': {'value': f'{verse()[0]}--{verse()[1]}', 'color': get_color()},
                        'one': {'value': '一言 :  ' + oneyg(), 'color': '#2B1B17'}
                        }
               }

    headers = {'header': "Content-Type: application/json;charset=utf-8"}
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + access_token

    json_template = json.dumps(payload)
    response_send = requests.post(url, headers=headers, data=json_template)
    print(response_send)


if __name__ == '__main__':
    appid = 'wxc406086ca38696f3'
    secret = 'de59ac469f5b914c61e4bd1042a8c08d'
    template_id = '2SRysTS6HRGXK3iX5o29lBi1CQ-8wspTTQr3MjOR390'
    users = ['oMRds5m7cHe9HPKqVN9wo7WNIRGU','oMRds5uSiYdHm9DU9ycQNI0-HpnM']
    province = '上海'
    city = '闵行'
    weat = weather(province, city)
    for user in users:
        send_message_ceshiVX(appid, secret, template_id, weat, province, city, user)
