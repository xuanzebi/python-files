from pyecharts import Map
from collections import Counter
import itchat
import matplotlib.pyplot as plt
import os
import math

from PIL import Image

#利用python进行分析微信好友地区及合并好友头像

itchat.login()

friends = itchat.get_friends(update=True)[0:]


def getdata(var):
    variable = []
    for i in friends:
        value = i[var]
        variable.append(value)
    return variable


# 下载好友头像
def download_images(friends):
    image_dir = "F:\google\machinelearning\Interstingcode\images\\"
    num = 1
    for i in friends:
        image_name = str(num) + '.jpg'
        num += 1
        img = itchat.get_head_img(userName=i["UserName"])
        with open(image_dir + image_name, 'wb') as file:
            file.write(img)


# 合微信头像
def mergeImage():
    print("正在合成头像")
    photo_width = 200  # 头像压缩
    photo_height = 200
    photo_path_list = []
    dirName = 'F:\google\machinelearning\Interstingcode\images'
    # 取所有图像的路径
    for root, dirs, files in os.walk(dirName):  # python oswalk()
        for file in files:
            if "jpg" in file:
                photo_path_list.append(os.path.join(root, file))

    pic_num = len(photo_path_list)
    line_max = int(math.sqrt(pic_num))
    row_max = int(math.sqrt(pic_num))

    if line_max > 20:
        line_max = 20
        row_max = 20
    num = 0
    pic_max = line_max * row_max
    toImage = Image.new('RGBA', (photo_width * line_max, photo_height * row_max))
    for i in range(0, row_max):
        for j in range(0, line_max):
            pic_fole_head = Image.open(photo_path_list[num])
            width, height = pic_fole_head.size
            tmppic = pic_fole_head.resize((photo_width, photo_height))
            loc = (int(j % row_max * photo_width), int(i % row_max * photo_height))
            toImage.paste(tmppic, loc)  # Image.paste 将tmppic粘贴到toImage上  loc是粘贴的位置
            num = num + 1
            if num >= len(photo_path_list):
                break
        if num >= pic_max:
            break
    print(toImage.size)
    toImage.save('merge.png')


def counter2list(_counter):
    name_list = []
    num_list = []

    for item in _counter:
        name_list.append(item[0])
        num_list.append(item[1])

    return name_list, num_list


# 需下载Echarts的中国地图
def get_map(item_name, item_name_list, item_num_list):
    subtitle = "hyp"
    _map = Map(item_name, width=1500, height=800, title_pos='center', title_text_size=30, \
               subtitle=subtitle, subtitle_text_size=25)
    _map.add("", item_name_list, item_num_list, maptype='china', is_visualmap=True, visual_text_color='#000')
    out_file_name = 'map.html'
    _map.render(out_file_name)


if __name__ == '__main__':
    pass
    # Province_counter = Counter()  # Counter 继承 dict 类、用于计数  key-value 元素作为key 计数作为value
    # for friend in friends:
    #     if friend['Province'] != "":
    #         Province_counter[friend['Province']] += 1
    # name_list, num_list = counter2list(Province_counter.most_common(30))  # most_common(指定一个参数n，列出前n个元素，不指定参数，则列出所有)
    # get_map('微信好友地图可视化', name_list, num_list)
    # download_images(friends)
    # mergeImage()


    # male = female = other = 0
    #
    # for i in friends[1:]:
    #     sex = i["Sex"]
    #     if sex == 1:
    #         male += 1
    #     elif sex == 2:
    #         female += 1
    #     else:
    #         other += 1
    #     print(i['NickName'])
    #     print(i['Signature'])
    # total = len(friends[1:])
    # print(total)
    #
    # print("男性好友人数: %f" % male + "\n" +
    #       "女性好友人数: %f" % female + "\n" +
    #       "不明性别好友人数: %f" % other)
