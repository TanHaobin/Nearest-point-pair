import random
import os

import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.patches as patches

maxRandNum = 100    #最大的随机数，即点的范围
n = 10              #随机点个数
waittime = 0.5     #刷新plot等待时间

#随机点集合
points = []
for i in range(n):
    points.append((random.randint(0, maxRandNum), random.randint(0, maxRandNum)))
points.sort()#预排序

ans = [maxRandNum ** 2] * 3#全局[最小距离,点1,点2]，初始给个大的值

def countDistance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

#蛮力法打印直线
def printplot(a, b):

    k = countDistance(a, b)
    line = lines.Line2D([a[0], b[0]], [a[1], b[1]])#两点确定一条直线

    #全局最优解
    if k < ans[0]:
        line2 = lines.Line2D([a[0], b[0]], [a[1], b[1]])
        line2.set_label("Min:" + str(k))#设置图标
        line2.set_color("black")
        if len(plt.gca().lines) >= 2:#lines[0]是表格用的，不能pop
            plt.gca().lines.pop()
        plt.gca().add_line(line2)#最优解直线放在最前面
        #更新最优解
        ans[0] = k
        ans[1] = a
        ans[2] = b
        print("更新最近点对：", a, b, "距离:", k)
    line.set_label("Cur:" + str(k))

    plt.gca().add_line(line)
    plt.gca().legend(fancybox=True, shadow=True)
    plt.pause(waittime)
    plt.gca().lines.pop()#每次画完一条直线经过等待时间后直接消掉即可

#蛮力法
def force():
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            printplot(points[i], points[j])
    plt.gca().lines.pop()

    print("\n所有点中最近距离的点为", ans[1], ans[2], "距离为",ans[0])
    os.system('pause')          #按任意键继续
    plt.gca().legend_ = None    #去掉图标框框


#返回随机RGB颜色
def randomcolor():
    colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0, 14)]
    return "#" + color

#找到能够框柱poinst[l, r]所有点的rectangle的参数
def findPosition(l, r):
    if l >= r:
        return (points[l][0], points[l][1]), 1, 1, randomcolor()
    maxX = max(i[0] for i in points[l:r + 1])
    maxY = max(i[1] for i in points[l:r + 1])
    minX = min(i[0] for i in points[l:r + 1])
    minY = min(i[1] for i in points[l:r + 1])
    return (minX, minY), maxX - minX, maxY - minY, randomcolor()

#归并
def merge(point, l, r):
    if l == r - 2 and point[l][1] > point[l + 1][1]:
        point[l], point[l + 1] = point[l + 1], point[l]

    tem = []
    mid = l + r >> 1
    rr = (l + r >> 1) + 1
    ll = l + 0

    while ll <= mid and rr <= r:
        if point[ll][1] < point[rr][1]:
            tem.append(point[ll])
            ll = ll + 1
        else:
            tem.append(point[rr])
            rr = rr + 1

    while ll <= mid:
        tem.append(point[ll])
        ll = ll + 1
    while rr <= r:
        tem.append(point[rr])
        rr = rr + 1

    for i in tem:
        point[l] = i
        l = l + 1

    return

#分治
def partition(l=0, r=len(points) - 1):
    plt.pause(waittime)         #刷新图片而已

    #找出两个部分的框框和所有区域的框框
    ll = findPosition(l, int((r - l) / 2 + l))
    rr = findPosition(int((r - l) / 2 + l + 1), r)
    mm = findPosition(l, r)

    #分割线
    mline = (points[int((r - l) / 2 + l)][0] + points[int((r - l) / 2 + l + 1)][0]) / 2
    linem = lines.Line2D([mline, mline], [mm[0][1], mm[2] + mm[0][1]], color="black", linewidth=1)


    plt.pause(0.5)
    if r == l + 2:
        # plt.gca().patches.pop()
        merge(points, l, r)
        a = countDistance(points[l], points[l + 1])
        b = countDistance(points[r], points[l + 1])
        c = countDistance(points[r], points[l])
        if a <= b and a <= c:
            tem = a, points[l], points[l + 1]
        if b <= a and b <= c:
            tem = b, points[l + 1], points[r]
        if c <= a and c <= b:
            tem = c, points[l], points[r]

        print("当前区域有三个点，点", tem[1], tem[2], "距离最小为%f\n" % tem[0])
        plt.gca().add_line(lines.Line2D([tem[1][0], tem[2][0]], [tem[1][1], tem[2][1]], linewidth=3, color="black"))
        plt.pause(waittime)
        return tem
    elif r == l + 1:
        merge(points, l, r)
        tem = countDistance(points[l], points[r]), points[l], points[r]
        print("当前区域有两个点", points[l], points[r], "，距离为%f\n" % tem[0])
        plt.gca().add_line(lines.Line2D([tem[1][0], tem[2][0]], [tem[1][1], tem[2][1]], linewidth=3, color="black"))
        plt.pause(waittime)
        return tem

    print("将当前区域以直线x = %f进行左右两部分划分:" % mline)
    print("\t左部分区域左下角坐标为", ll[0], "宽度为%d,高度为%d" % (ll[1], ll[2]))
    print("\t右部分区域左下角坐标为", rr[0], "宽度为%d,高度为%d\n" % (rr[1], rr[2]))

    #左右两个框框，这里为了完全包住点扩大了0.5的范围
    rectl = patches.Rectangle((ll[0][0] - 0.5, ll[0][1] - 0.5), ll[1] + 1, ll[2] + 1, linewidth=3, edgecolor=ll[3], facecolor='none')
    rectr = patches.Rectangle((rr[0][0] - 0.5, rr[0][1] - 0.5), rr[1] + 1, rr[2] + 1, linewidth=3, edgecolor=rr[3],facecolor='none')

    #闪闪闪
    plt.gca().add_patch(rectl)
    plt.gca().add_patch(rectr)
    plt.gca().add_line(linem)
    plt.pause(0.5)
    plt.gca().patches.pop()
    plt.gca().patches.pop()
    plt.gca().lines.pop()
    plt.pause(0.3)
    plt.gca().add_patch(rectl)
    plt.gca().add_patch(rectr)
    plt.gca().add_line(linem)
    plt.pause(waittime)

    # 只显示左框处理部分
    plt.gca().lines.pop()
    plt.gca().patches.pop() #pop的是右边的框框

    minl = partition(l, int((r - l) / 2 + l))

    plt.gca().patches.pop()
    # 处理完左边铺满闪两次
    rectl.set_facecolor(ll[3])#处理完后变为填充

    #闪闪闪
    plt.pause(0.3)
    plt.gca().add_patch(rectl)
    plt.pause(0.5)
    plt.gca().patches.pop()
    plt.pause(0.3)
    plt.gca().add_patch(rectl)
    plt.pause(0.5)
    plt.gca().patches.pop()
    plt.pause(0.3)

    plt.gca().add_patch(rectr)
    plt.pause(waittime)

    minr = partition(int((r - l) / 2 + l + 1), r)

    plt.gca().patches.pop()
    rectr.set_facecolor(rr[3])
    plt.pause(0.3)
    plt.gca().add_patch(rectr)
    plt.pause(0.5)
    plt.gca().patches.pop()
    plt.pause(0.3)
    plt.gca().add_patch(rectr)
    plt.pause(0.5)
    plt.gca().patches.pop()
    plt.pause(0.3)

    print("左部分区域最小值为", minl, "右部分区域最小值为", minr)
    # 左右铺满闪两次
    plt.pause(waittime)
    plt.gca().add_patch(rectl)
    plt.gca().add_patch(rectr)
    plt.pause(0.5)
    plt.gca().patches.pop()
    plt.gca().patches.pop()
    plt.pause(0.3)
    plt.gca().add_patch(rectl)
    plt.gca().add_patch(rectr)
    plt.pause(0.5)
    plt.gca().patches.pop()
    plt.gca().patches.pop()
    plt.pause(0.3)
    plt.pause(waittime)

    if minl[0] > minr[0]:
        m = minr
    else:
        m = minl

    print("对两边的最小值", m[0], "检测划分直线 x =", mline, "两端距离为", m[0], "中的点对是否存在更小距离的点对")

    #画出Y'的区域
    rectm = patches.Rectangle((mline - m[0], mm[0][1] - 0.5), 2 * m[0], mm[2] + 1, linewidth=3, edgecolor=mm[3],facecolor=mm[3])

    #闪闪闪
    plt.gca().add_line(linem)
    plt.gca().add_patch(rectm)
    plt.pause(0.5)
    plt.gca().patches.pop()
    plt.gca().lines.pop()
    plt.pause(0.3)
    plt.gca().add_line(linem)
    plt.gca().add_patch(rectm)
    plt.pause(0.5)
    plt.gca().patches.pop()
    plt.gca().lines.pop()
    plt.pause(0.3)

    merge(points, l, r)
    points_y = [i for i in points[l : r + 1] if abs(i[0] - mline) < m[0]]
    for i in range(len(points_y)):
        for j in range(i + 1, min(i + 1 + 7, len(points_y))):
            if countDistance(points_y[i], points_y[j]) < m[0]:
                m = countDistance(points_y[i], points_y[j]), points_y[i], points_y[j]
    print("最终当前区域最小值为", m, '\n')

    #pop两次左右最优解的直线，然后整体add最优解直线
    plt.gca().lines.pop()
    plt.gca().lines.pop()
    plt.gca().add_line(lines.Line2D([m[1][0], m[2][0]], [m[1][1], m[2][1]], linewidth=3, color="black"))

    plt.pause(waittime)
    return m


if __name__ == '__main__':
    print("使用Pycharm弹出Plot的方式运行以得到更好的观看体验")
    print("作者：https://github.com/TanHaobin/Nearest-point-pair\n\n")
    fig = plt.figure()  # 新建绘图窗口
    ax = fig.add_subplot(1, 1, 1)
    plt.xlim(0 - 5, maxRandNum + 5)
    plt.ylim(0 - 5, maxRandNum + 5)
    plt.ion()
    plt.plot([i[0] for i in points], [i[1] for i in points], 'ro')


    print("蛮力法")
    plt.pause(0.01)
    force()
    plt.pause(0.01)


    print("分治法")
    ans = partition()
    print("所有点中距离最小的点对为", ans[1], ans[2], "距离为", ans[0])
    plt.pause(100)


