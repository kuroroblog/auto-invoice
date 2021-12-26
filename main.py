import json
import cv2
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from dateutil.relativedelta import *
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# 参考 : https://kuroro.blog/python/Omz54Dk1uR1d23yNow7e/
def put_text_from_img(img, position, text):
    # OSError: cannot open resourceのエラーが出た場合 : https://qiita.com/Afo_guard_enthusiast/items/60e21acc6259a58e7ff0
    font_path = '/Library/Fonts//Arial Unicode.ttf'
    font_size = 12

    font = ImageFont.truetype(font_path, font_size)
    # cv2(numpy.ndarray)型の画像を、PILライブラリに合わせた型の画像へ変換する。
    img = Image.fromarray(img)
    # 文字列を挿入するために、描画用のDraw関数を用意する。
    draw = ImageDraw.Draw(img)
    # 文字列を描画(位置, 文字列, フォント情報, 文字列色)する。
    draw.text((position[0], position[1]), text, font=font, fill=(0, 0, 0))

    return np.array(img)

def calc_price(hour, minute, price):
    sub_total = int(hour) * price['wage'] + int((int(minute) / 60) * price['wage'])
    tax = int(sub_total * 0.1)
    total = sub_total + tax + price['traffic']

    return sub_total, tax, total

# 参考 : https://tanuhack.com/operate-spreadsheet/
# 参考 : https://tanuhack.com/library-gspread/#i-5
def get_work_time_from_spreadsheet(spreadsheet):
    credentials = ServiceAccountCredentials.from_json_keyfile_name('./service-account.json', scope)
    gc = gspread.authorize(credentials)
    worksheet = gc.open_by_key(spreadsheet['id'])
    worksheet = worksheet.worksheet(spreadsheet['name'])

    return worksheet.acell(spreadsheet['cell']).value.split(':')

def get_today():
    return datetime.date.today()

# 参考 : https://qiita.com/kikuchiTakuya/items/53990fca06fb9ba1d8a7
def get_json_data(path):
    return json.load(open(path, 'r'))

def get_image(path):
    img = cv2.imread(path)

    if img is None:
        sys.exit("Could not read the image.")

    return img

img = get_image('./sample.jpg')
result = get_json_data('env.json')
today = get_today()

hour, minute, _ = get_work_time_from_spreadsheet(result['data']['spreadsheet'])
sub_total, tax, total = calc_price(hour, minute, result['data']['price'])

img = put_text_from_img(img, (590, 164), today.strftime('%Y/%m/%d'))
img = put_text_from_img(img, (590, 258), result['data']['address'])
img = put_text_from_img(img, (590, 280), result['data']['name'])
img = put_text_from_img(img, (590, 300), result['data']['tel'])

img = put_text_from_img(img, (90, 205), result['data']['company'])
img = put_text_from_img(img, (90, 700), result['data']['transfer'])
# 参考 : https://qiita.com/etern/items/8a48cff7915efd565fab
img = put_text_from_img(img, (90, 422), '%s(%s)' % (result['data']['content'], (today - relativedelta(months=1)).strftime('%Y年%m月度')))

img = put_text_from_img(img, (240, 321), '%s' % (total))

img = put_text_from_img(img, (645, 422), '%s円' % (sub_total))
img = put_text_from_img(img, (645, 652), '%s円' % (sub_total))
img = put_text_from_img(img, (645, 673), '%s円' % (tax))
img = put_text_from_img(img, (645, 695), '%s円' % (str(result['data']['price']['traffic'])))
img = put_text_from_img(img, (645, 716), '%s円' % (total))

cv2.imwrite('/path_to/output.jpg', img)
