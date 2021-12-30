import openpyxl as opl
import cv2 as cv
import math
from math import dist
import numpy as np
import matplotlib.pyplot as plt


def clc_dist(img):

    CLC = []

    img = cv.imread(img, cv.IMREAD_COLOR)

    b, g, r = cv.split(img)
    img = cv.merge([r, g, b])

    y, x, c = img.shape

    #초점 ( 이 점들에 위치한 색정보를 빼낼 것 )

    location_1 = (int(y/12), int(x/2))
    location_2 = (int(y/4), int(x/2))
    location_3 = (int(y*5/12), int(x/2))
    location_4 = (int(y*7/12), int(x/2))
    location_5 = (int(y*3/4), int(x/2))
    location_6 = (int(y*11/12), int(x/2))

    clc_parts = [[img[location_1], location_1],
                 [img[location_2], location_2],
                 [img[location_3], location_3],
                 [img[location_4], location_4],
                 [img[location_5], location_5],
                 [img[location_6], location_6]]


    for cp in clc_parts:

        i = cp[0] # 0번째 값은 (R, G, B) 1번째 값은 초점좌표
        neighbors = [] # 초점과 이웃하는 8개 픽셀의 rgb값
        #print("예전 RGB : ", i)

        try:
            for n in range(-4, 5):
                neighbors.append(img[cp[1][0], cp[1][1] + n])

        except:
            pass



        #print(np.std(neighbors))


        if np.std(i) < 20: # 표준편차가 20이 넘지 않으면 (회색계열일 경우 초점이 색코드 바깥일 가능성이 높다 )

            for j in range(0, x): # 표준편차 20이 넘을때 까지 초점을 0에서 오른쪽으로 이동
                i = img[cp[1][0], j]

                try:
                    if np.std(i) > 20:
                        i = img[cp[1][0], j + 4]  # 4픽셀 여유두고 지정 ( 경계선에 걸쳐있으면 색판정이 모호해질수 있으니 )
                        continue
                except:
                    pass



        if np.std(neighbors) > 50: # 경계선에 걸쳐서 색판정이 나는걸 방지하기 위해
                                   # 이웃하는 픽셀들 끼리의 표준편차값을 검토하여 초점 재배치 ( 경계선이 끼어있고 하면 표준편차값이 커진다 )

            if np.std(neighbors[0]) < np.std(neighbors[-1]):  # 왼쪽이 회색계열일것 같으면 오른쪽으로 초점이동
                #print('오른쪽으로 이동')
                try:
                    i = img[cp[1][0], cp[1][1] + 3]
                except:
                    i = img[cp[1][0], cp[1][1] - 3]


            elif np.std(neighbors[0]) > np.std(neighbors[-1]): # 오른쪽이 회색계열이면 왼쪽으로 초점이동
                #print('왼쪽으로 이동')
                try:
                    i = img[cp[1][0], cp[1][1] - 3]
                except:
                    i = img[cp[1][0], cp[1][1] + 3]

            else:
                pass

        else:
            pass

        print("보정된 RGB : ", i)


        distances = []

        # 색상거리 계산
        distances.append(dist(i, [150, 37, 23]))  # 0 red
        distances.append(dist(i, [185, 136, 83]))  # 1 orange
        distances.append(dist(i, [253, 248, 104]))  # 2 yellow
        distances.append(dist(i, [153, 177, 83]))  # 3 lightgreen
        distances.append(dist(i, [0, 104, 48]))  # 4 green
        distances.append(dist(i, [15, 109, 137]))  # 5 teal
        distances.append(dist(i, [1, 137, 221]))  # 6 cyan 38, 143, 199
        distances.append(dist(i, [0, 56, 132]))  # 7 blue
        distances.append(dist(i, [98, 13, 72]))  # 8 violet
        distances.append(dist(i, [192, 36, 96]))  # 9 magenta
        distances.append(dist(i, [117, 162, 185]))  # 10 skyblue

        distances.append(dist(i, [190, 22, 31]))  # 11 red
        distances.append(dist(i, [151, 39, 66]))  # 12 magenta
        distances.append(dist(i, [6, 81, 173]))  # 13 blue



        min_distance = distances.index(min(distances))
        print(min_distance)



        if min_distance == 0: # RED 0
            CLC.append("R")
        elif min_distance == 1: # ORANGE 1
            CLC.append("O")
        elif min_distance == 2: # YELLOW 2
            CLC.append("Y")
        elif min_distance == 3: # LIGHT GREEN 3
            CLC.append("L")
        elif min_distance == 4: # GREEN 4
            CLC.append("G")
        elif min_distance == 5: # TEAL 5
            CLC.append("T")
        elif min_distance == 6: # CYAN 6
            CLC.append("B")
        elif min_distance == 7 or min_distance == 13: # BLUE 7
            CLC.append("B")
        elif min_distance == 8: # VIOLET 8
            CLC.append("V")
        elif min_distance == 9 or min_distance == 12: # MAGENTA 9
            CLC.append("M")
        elif min_distance == 10: # SKY BLUE 10
            CLC.append("S")
        elif min_distance == 11: # RED 11
            CLC.append("R")
        else:
            pass
    return "".join(list(CLC))


# for k in range(0, 12):
#     img_name = 'clcimg_'+str(k)+'.png'
#     clc_dist(img_name)

#clc_dist('clcimg_9.png')



def booknamefinder(clc_input): # 테스트용
    try:
        file_path = 'lib_table.xlsx'

        wb = opl.load_workbook(file_path)
        ws = wb['Sheet1']

        rows = ws.iter_rows(min_row=2, min_col=1, max_col=5)

        book_names = []
        book_codes = []

        for a, b, c, d, e in rows:
            book_names.append(b.value)
            book_codes.append(d.value)

        print(book_names[book_codes.index(clc_input)])

    except:
        print('해당 책이 없습니다.')
        pass


if __name__ == "__main__":
    #for k in range(0, 22):
        #img_name = 'clcimg_' + str(k) + '.png'
        #print(clc_dist(img_name))
        #booknamefinder(clc_dist(img_name))
    print(clc_dist('clcimg_8.png'))
