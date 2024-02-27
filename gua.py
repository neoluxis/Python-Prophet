import random
import time
import hashlib
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


def strhash(string):
    """
    计算一个字符串的sha256
    """
    encoded_string = string.encode()
    hashed_string = hashlib.sha256(encoded_string)
    unique_number = int(hashed_string.hexdigest(), 16)
    return unique_number


def unio():
    """
    生成一个爻
    """
    mu = 25
    sigma2 = 4
    # 因为人分蓍草总是习惯从中间分，所以把分两堆的数字设置为μ为25，σ²为4的正态分布
    ran = [random.gauss(mu, sigma2) for i in range(200)]
    nums = [x for x in ran if 0 <= x <= 50]  # 大衍之数五十，所以筛选正态分布中小于50的数

    hold = 0  # 扐蓍之数
    grand = 50  # 大衍之数五十 - 取出50根蓍草
    taichi = 1  # 其用四十有九 - 取出一根
    grand -= taichi  # 剩余49根

    for i in range(3):
        # 分而为二以象两 - 把49分为2份代表两仪
        caelum = round(nums[i])  # 天
        terra = grand - caelum  # 地
        # print(caelum, terra)
        # 挂一以象三 - 从其中一份取出一根，代表三种事物
        homme = 1  # 人
        terra -= homme
        hold += homme  # 挂一

        # 揲之以四以象四时，归奇于扐以象闰
        hold += terra % 4 if terra % 4 > 0 else 4
        hold += caelum % 4 if caelum % 4 > 0 else 4

        group = terra//4 + caelum // 4 - \
            (0 if terra % 4 > 0 else 1) - (0 if caelum % 4 > 0 else 1)
        # print(group, hold)
        grand = group * 4
        hold = 0
        # 五岁再闰，故再扐而后挂
    return group


def gua():
    """
    生成六个爻，为一卦
    """
    res = []
    yao = []
    bin_seq = []
    for i in range(6):
        une = unio()
        res.append(une)
        if une == 6:
            yao.append("太阴")
            bin_seq.append(1)
        elif une == 7:
            yao.append("少阳")
            bin_seq.append(1)
        elif une == 8:
            yao.append("少阴")
            bin_seq.append(0)
        elif une == 9:
            yao.append("太阳")
            bin_seq.append(0)
    # print(res, yao, bin_seq)
    value = 0
    for i in range(-1, -7, -1):
        value = value * 2 + bin_seq[i]
    return res, yao, value


def draw(yao=None, save=True, fname="images/gua.png", show=False):
    """
    绘制/保存/展示卦象图片
    """
    if yao == None:
        yao = gua()[0]
    # 定义图像大小和颜色
    image_size = (950, 950)  # 图像宽度和高度
    background_color = 255  # 白色背景颜色 (B, G, R)

    ys = [850, 700, 550, 400, 250, 100]  # 爻的y坐标
    startx = 100  # 爻的起始x坐标
    midsx = 400  # 爻的中间x坐标
    midex = 550  # 爻的中间x坐标
    endx = 850  # 爻的结束x坐标
    thickness = 100  # 爻的线宽

    lcolor = (0, 0, 0)  # 爻的颜色 (B, G, R)

    # 创建空白图像
    image = np.ones((image_size[1], image_size[0], 3),
                    dtype=np.uint8) * background_color

    # 在指定高度上绘制多条横线
    for i in range(6):
        if yao[i] == 6 or yao[i] == 7 or yao[i] == 1:  # 6, 7, 1 阳爻
            cv.line(image, (startx, ys[i]), (endx, ys[i]), lcolor, thickness)
        else:  # 8, 9, 0 阴爻
            cv.line(image, (startx, ys[i]), (midsx, ys[i]), lcolor, thickness)
            cv.line(image, (midex, ys[i]), (endx, ys[i]), lcolor, thickness)

    # 保存图像
    if save:
        cv.imwrite(fname, image)
        print(f"Image saved as {fname}")

    # 展示图像
    if show:
        plt.imshow(image)
        plt.axis('on')
        plt.show()


def main():
    seed = strhash(input("(Optional) Input seed: ")) + \
        int(round(time.time()) * 1000)  # 输入的字符串进行散列后与时间戳相加，构造独一无二的随机数种子
    # print(seed)
    random.seed(seed)
    res, yao, bsq = gua()
    print(res, yao, bsq)
    draw(res, show=True)


if __name__ == '__main__':
    main()
