import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import CLC_ColorFilter as cfilter

import os
import time


#plt.style.use('dark_background')

# 이미지를 jpg 형태로 저장하고
# 파일 이름을 CLC_name_list 리스트에 저장하는 함수

# 책장 사진을 받아 조건에 맞는 컨투어를 찾고

lib_data = 'lib_table.xlsx'


def clc_function(bs_img): # 책장사진 ==> 도서데이터 수정


    try:
        for i in range(100):  # 이전에 저장해뒀던 필요없는 색코드 이미지 삭제
            temp_code_img = 'clcimg_' + str(i) + '.png'
            os.remove(temp_code_img)


    except:
        pass

    final_contours = []  # 컨투어 리스트
    CLC_name_list = []  # 색코드 저장 파일 이름들을 리스트로 저장
    book_info = []
    CLC_list = []  # 색코드 리스트

    def save_img_file(frame, i): # 하나의 색코드 이미지를 저장하고 이름 리스트에 저장
        file = 'clcimg_' + str(i) + '.png'
        cv.imwrite(file, frame)
        print(file + " is saved")
        CLC_name_list.append(file)
        return CLC_name_list

    def CLC(bs_img): # 책장사진 => 색코드 이미지 잘라서 저장
        img_bookshelf = cv.imread(bs_img, cv.IMREAD_COLOR)
        height, width, channel = img_bookshelf.shape

        #  그레이화
        gray_bookshelf = cv.cvtColor(img_bookshelf, cv.COLOR_BGR2GRAY)

        if __name__ == "__main__":
            plt.figure(figsize=(12, 10))
            plt.imshow(gray_bookshelf, cmap='gray')


        # 가우시안, 쓰레스홀드
        img_blurred = cv.GaussianBlur(gray_bookshelf, ksize=(5, 5), sigmaX=0)

        """
        plt.figure(figsize=(12, 10))
        plt.imshow(img_blurred, cmap='gray')
        """

        img_thresh = cv.adaptiveThreshold(
            img_blurred,
            maxValue=255.0,
            adaptiveMethod=cv.ADAPTIVE_THRESH_GAUSSIAN_C,
            thresholdType=cv.THRESH_BINARY_INV,
            blockSize=19,
            C=9
        )

        # plt.figure(figsize=(12, 10))
        # plt.imshow(img_thresh, cmap='gray')

        # 컨투어를 찾는다

        contours, _ = cv.findContours(
            img_thresh,
            mode=cv.RETR_LIST,
            method=cv.CHAIN_APPROX_SIMPLE
        )

        contour_bookshelf = np.zeros((height, width, channel), dtype=np.uint8)

        # 컨투어를 사각형으로

        contours_dict = []

        for contour in contours:
            x, y, w, h = cv.boundingRect(contour)
            cv.rectangle(contour_bookshelf, pt1=(x, y), pt2=(x + w, y + h), color=(255, 255, 255), thickness=2)

            # 사각형화 컨투어 정보를 dictionary에 저장

            contours_dict.append({
                'x': x,
                'y': y,
                'w': w,
                'h': h,
                'cx': x + (w / 2),
                'cy': y + (h / 2)
                #'cont': contour

            })


        # 1차 필터링 (사각형 비율 최소 최대 지정 후 비교)

        MIN_RATIO, MAX_RATIO = 0.13, 0.6  # 클수록 뚱뚱해짐 0.17 / 0.4
        MIN_AREA, MAX_AREA = 1300, 6000 # 1800 / 3300
        MIN_HEIGHT, MAX_HEIGHT = 80, 120 # 90 / 115
        MIN_WIDTH, MAX_WIDTH = 13, 40 # 15 / 35


        possible_contours = []
        cnt = 0

        for d in contours_dict:
            ratio = d['w'] / d['h']
            area = d['w'] * d['h']
            wid = d['w']
            hgt = d['h']

            if MAX_AREA > area > MIN_AREA and MIN_RATIO < ratio < MAX_RATIO and MIN_HEIGHT < hgt < MAX_HEIGHT and MIN_WIDTH < wid < MAX_WIDTH:
                d['idx'] = cnt
                cnt += 1  # 번호지정(인덱스) 0부터 시작
                possible_contours.append(d)  # 조건에 맞는 사각형 값들을 possible_contours - (딕셔너리)에 저장

        temp_result = np.zeros((height, width, channel), dtype=np.uint8)

        for d in possible_contours:
            img_contour = cv.rectangle(temp_result, pt1=(d['x'], d['y']), pt2=(d['x'] + d['w'], d['y'] + d['h']),
                                       color=(255, 255, 255), thickness=2)

        if __name__ == "__main__":
            plt.figure(figsize=(12, 10))
            plt.imshow(temp_result, cmap='gray')
            plt.show()


        # 굵은 선으로 인해 컨투어가 겹치는 현상이 발생
        # 두 컨투어의 거리를 비교하여 거의 차이나지 않는 두 컨투어중 하나를 버린다

        for d1 in possible_contours:

            for d2 in possible_contours:
                if d1['idx'] == d2['idx']:
                    continue

                distance = np.linalg.norm(np.array([d1['cx'], d1['cy']]) - np.array([d2['cx'], d2['cy']]))

                if distance < d1['w']*0.9:
                    possible_contours.remove(d2)

        #  뒤죽박죽 순서를 정렬 ( x 좌표 순으로 재 정렬하고 다시 인덱싱 )
        Sorted_contours = sorted(possible_contours, key=lambda x: x['x'], reverse=False)
        cnt = 0
        for d in Sorted_contours:
            d['idx'] = cnt
            cnt += 1
            final_contours.append(d)


        #  색코드 크기에 맞게 자른다
        for d in final_contours:
            img_cropped = cv.getRectSubPix(
                img_bookshelf,
                patchSize=(d['w'], d['h']),
                center=(d['x'] + d['w'] / 2, d['y'] + d['h'] / 2)
                # 각각의 컨투어 기준이 아닌 중심점으로 부터 거리를 제시하면 모든 이미지의 크기를 통일시킬수도있음...
            )

            save_img_file(img_cropped, d['idx'])  # 이미지 저장
        arrange_info()

    def arrange_info(): # 이떄까지 얻은 모든 정보를 정리

        for i in CLC_name_list:  # 색코드이름 문자열로 리스트에 저장 (ex. clcimg_4.png)
            CLC_list.append(cfilter.clc_dist(i))
            print(i)

        index = 0
        for i in final_contours:

            i["code"] = CLC_list[index]
            book_info.append(i)
            index = index + 1

        return book_info

    def info_rewrite(colorcode, x_position, y_position): # book_info 를 토대로 엑셀파일을 수정

        try :

            which_book = df.loc[df['색코드'] == colorcode]  # 색코드외 일치하는 셀을 변수에 할당
            #print(which_book)

            which_index = which_book.iloc[0, 0] - 1  # 그 셀의 행 번호를 변수에 할당

            df.at[which_index, '제자리'] = 'Y'  # 해당 행에서 '제자리' 열인 셀에 Y를 입력 (또는 수정)
            df.at[which_index, 'x위치'] = x_position
            df.at[which_index, 'y위치'] = y_position

            df.to_excel(lib_data, index=False)

        except: # 색코드가 일치하지 않는 경우에
            pass


    CLC(bs_img)

    df = pd.read_excel(lib_data)  # 엑셀 읽어오기
    df["제자리"] = "N"  # 제자리 초기 셋팅
    df["x위치"] = ""
    df["y위치"] = ""

    for i in book_info: # 색코드 정보 기입 반복문
        print(i)
        info_rewrite(i['code'], i['cx'], i['cy'])





if __name__ == "__main__":

    book_shelf = 'bookshelf.jpg'

    cap = cv.VideoCapture(0)  # 0 번 카메라 캡처 모드
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)  # 가로프레임 길이 설정
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)  # 세로프레임 길이 설정

    ret, frame = cap.read()

    time.sleep(0)
    img_name = "bookshelf.jpg"
    cv.imwrite(img_name, frame)  # 사진 찍기

    cap.release()
    cv.destroyAllWindows()

    clc_function(book_shelf)
