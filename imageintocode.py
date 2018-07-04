
#将图像转为由字符构成的灰度图

import matplotlib.pyplot as plt
show_height = 30
show_width = 40
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
char_len = len(ascii_char)
pic = plt.imread("d.jpg")

pic_height ,pic_width,_ = pic.shape
gray = 0.2126 * pic[:,:,0] + 0.7152 * pic[:,:,1] + 0.0722 * pic[:,:,2]
for i in range(show_height):
    y = int(i * pic_height / show_height )
    text = ""
    for j in range(show_width):
        x = int(j * pic_width / show_width)
        text += ascii_char[int(gray[y][x] / 256 * char_len)]
    print(text)