import json
import random

import requests
import time
import datetime


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


time_tuple = time.localtime(time.time())
t = "{}年{}月{}日".format(time_tuple[0], time_tuple[1], time_tuple[2], time_tuple[3])
hour = time_tuple[3]
mins = time_tuple[4]
if hour < 10:
    hour = '0'+ str(hour)
if mins < 10:
    mins = '0' + str(mins)

ti = f'上午 {hour}:{mins}'
d = datetime.datetime.now().weekday()
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


def caihongpi():
    req = requests.get(url='http://api.tianapi.com/caihongpi/index?key=f70ff9e841951175e95b90e8ca1231ed',
                       headers={'Content-Type': 'application/x-www-form-urlencoded'}).json()
    return req['newslist'][0]['content'].replace('xxx', '小杰')


def oneyg():
    req = requests.get('http://api.tianapi.com/one/index', params={'key': 'f70ff9e841951175e95b90e8ca1231ed',

                                                                   'rand': '1'}).json()['newslist'][0]
    return req['word'], req['wordfrom']


def send_message_ceshiVX(appid, secret, template_id, weat, province, city, userid):  # 默认发送给自己

    # 获取token
    response = requests.get(
        f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + appid + "&secret=" + secret)
    data = json.loads(response.text)
    access_token = data['access_token']

    one = oneyg()
    payload = {'touser': userid, 'template_id': template_id,
               'url': '',
               "topcolor": get_color(),
               'data': {'caihongpi': {'value': caihongpi(), 'color': get_color()},
                        'date': {'value': t + ' ' + d+'\n'+ti, 'color': get_color()},
                        'province': {'value': province},
                        'city': {'value': city, 'color': get_color()},
                        'tq': {'value': weat[0], 'color': get_color()},
                        'tem1': {'value': weat[2] + '°C' + ' ~ ' + weat[1] + '°C', 'color': get_color()},
                        'win': {'value': weat[3]},
                        'win1': {'value': wet[4],'color': get_color()}
                        'one': {'value': '每日一言 :  ' + one[0], 'color': get_color()}
                        }
               }

    headers = {'header': "Content-Type: application/json;charset=utf-8"}
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + access_token

    json_template = json.dumps(payload)
    response_send = requests.post(url, headers=headers, data=json_template)
    print("测试公众号：", response_send.text)


if __name__ == '__main__':
    appid = 'wxc406086ca38696f3'
    secret = 'de59ac469f5b914c61e4bd1042a8c08d'
    template_id = 'PuWYwK3C8jVjtU671rgUs3Hr4ocfsSDGiXfxD5Ys7Aw'
    users = ['oMRds5m7cHe9HPKqVN9wo7WNIRGU','oMRds5uSiYdHm9DU9ycQNI0-HpnM']
    province = '上海'
    city = '闵行'
    weat = weather(province, city)
    for user in users:
        send_message_ceshiVX(appid, secret, template_id, weat, province, city, user)
