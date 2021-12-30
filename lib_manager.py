# 적외선 센서 신호를 여기서 받고 카메라 캡쳐 명령해야함
# 대출 반납시 적외선 신호 작동 -> 도서관리 프로그램 -> 카메라 -> CLC -> 도서관리 프로그램 새로고침 해줘야 하기때문에.

from tkinter import *
from tkinter import filedialog, messagebox, ttk

import serial
import time
import pandas as pd
#import camera as cam
import CLC
import cv2 as cv


bs_img = '1.jpg' # 책장 이미지 사진

ser = serial.Serial('COM3', 9600) # 시리얼통신

def capture(): # 사진 찍기
    cap = cv.VideoCapture(0)  # 0 번 카메라 캡처 모드
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)  # 가로프레임 길이 설정
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)  # 세로프레임 길이 설정

    ret, frame = cap.read()
    img_name = "test_bookshelf.png"
    cv.imwrite(img_name, frame)  # 사진 찍기

    cap.release()
    cv.destroyAllWindows()


root = Tk()
root.title("도서관리프로그램")
root.geometry("1280x720")
root.resizable(False, False)

# 파일열기
def file_open():
    global filename
    filename = filedialog.askopenfilename(initialdir=r"C:\Users",
                                          title="엑셀 파일을 선택하세요",
                                          filetypes=(("xlsx 파일", "*.xlsx"), ("모든 파일", "*.*")))
    make_table(filename)

def make_table(filename):
    try:
        global df
        df = pd.read_excel(filename)
        draw_table(df)

    except ValueError:
        messagebox.showerror("오류", "파일이 유효하지 않음")
        return None

    except FileNotFoundError:
        messagebox.showerror("오류", f"{filename} 파일을 찾을 수 없음")
        return None

def draw_table(df):

    clear_data()
    excel_data["column"] = list(df.columns)
    excel_data["show"] = "headings"

    for column in excel_data["column"]:
        excel_data.heading(column, text=column)

    excel_data.column("번호", width=50)
    excel_data.column("제목", width=180)
    excel_data.column("저자", width=100)
    excel_data.column("색코드", width=100)
    excel_data.column("대출여부", width=100)
    excel_data.column("제자리", width=100)

    excel_data.column("x위치", width=100)
    excel_data.column("y위치", width=100)
    excel_data.column("위치기록x", width=100)
    excel_data.column("위치기록y", width=100)
    excel_data.column("대출상태", width=100)


    df_rows = df.to_numpy().tolist()

    print(df_rows)

    for row in df_rows:
        excel_data.insert("", "end", values=row)

    return None


def clear_data():
    excel_data.delete(*excel_data.get_children())

def refresh():

    CLC.clc_function(bs_img)

    df = pd.read_excel(filename)
    draw_table(df)
    pass


# 탑 메뉴
menu = Menu(root)
menu_file = Menu(menu, tearoff=0)
menu_file.add_command(label="파일 불러오기", command=file_open)
menu_file.add_command(label="파일 새로고침", command=refresh)
menu_file.add_command(label="카메라 ON", command=capture)

menu.add_cascade(label="파일", menu=menu_file)
menu.add_cascade(label="도움말")

root.config(menu=menu)

# 제목
title = Label(root, text="도서관리프로그램", font=("맑은 고딕", 30))
title.pack(pady=20)

# 검색 창, 버튼
search_frame = Frame(root)
search_frame.pack()

def search_function():

    keyword = str(search_box.get())

    if keyword == "":
        draw_table(df)

    else :
        result = df[df['제목'].str.contains(keyword)]
        draw_table(result)


search_box = Entry(search_frame, width=120)
search_button = Button(search_frame, font=("맑은 고딕", 15), text="검색", width=10, height=1, command = search_function)

search_box.grid(row=0, column=0, sticky=N+E+W+S, padx=5, pady=5, ipady=5)
search_button.grid(row=0, column=1, sticky=N+E+W+S)


# 검색결과 (엑셀연동)
excel_frame = LabelFrame(root, text="검색결과")
excel_frame.pack(fill='x', padx=10, pady=10, ipadx=100, ipady=180)
excel_data = ttk.Treeview(excel_frame, height=1)
excel_data.place(relheight=1, relwidth=1)
#excel_data.grid(ipadx=500, padx=3, row=0, column=0, sticky=N+E+W+S)


# 수직 수평 스크롤
treescrollx = Scrollbar(excel_frame, orient="horizontal", command=excel_data.xview)
treescrolly = Scrollbar(excel_frame, orient="vertical", command=excel_data.yview)
excel_data.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
treescrollx.pack(side="bottom", fill="x")
treescrolly.pack(side="right", fill="y")

#treescrolly.grid(row=0, column=1, sticky=N+S)
#treescrollx.grid(row=1, column=0, columnspan=1, sticky=E+W)


# 버튼들의 기능
def find_book():
    selected_book = excel_data.focus()
    getvalue = excel_data.item(selected_book).get("values")

    if getvalue == "":
        pass

    else :
        book_x = str(int((float(getvalue[6]) - 664) * (30/469))+3)
        print(bytes(book_x, 'utf-8')) # 아두이노는 bytes 형식으로 데이터를 보내줘야함

        if ser.readable(): # 시리얼 통신
            ser.write(bytes(book_x, 'utf-8'))


def loan_book():
    selected_book = excel_data.focus()
    getvalue = excel_data.item(selected_book).get("values")

    if getvalue == "":
        pass

    else:
        book_x = str(int((float(getvalue[6]) - 497) *(27/497))+3)
        print(bytes(book_x, 'utf-8')) # 아두이노는 bytes 형식으로 데이터를 보내줘야함

        #if ser.readable(): # 시리얼 통신
            #ser.write(bytes(book_x, 'utf-8'))

        df = pd.read_excel(filename)

        which_book = df.loc[df['색코드'] == getvalue[3]] # 선택된 책의 색코드와 일치하는 행을 엑셀파일에서 따온다
        which_index = which_book.iloc[0, 0] - 1  # 선택된 책의 인덱스를 따온다

        df.at[which_index, '대출상태'] = 1 # 대출상태를 1로 바꾸고
        df.at[which_index, '위치기록x'] = getvalue[6]  # 위치기록도 수정한다
        df.at[which_index, '위치기록y'] = getvalue[7]

        df.to_excel(filename, index=False)

        refresh()




def return_book():
    pass


# 버튼 프레임
button_frame = LabelFrame(root, text="상호 작용")
button_frame.pack(fill="both", expand=True, padx=20, pady=10, ipady=5)

 # 도서찾기
button_find = Button(button_frame,
                     padx=325, pady=4,
                     font=("맑은 고딕", 15), text="위치 안내 (클릭)",
                     command=find_book)

button_find.pack(side="left", padx=5, pady=5)

 # 대출
button_loan = Button(button_frame,
                     padx=55, pady=4,
                     font=("맑은 고딕", 15), text="도서 대출",
                     bg="green",
                     fg="yellow",
                     command=loan_book)

button_loan.pack(side="left", padx=5, pady=5)

 # 반납
button_return = Button(button_frame,
                       padx=55, pady=4,
                       font=("맑은 고딕", 15), text="도서 반납",
                       bg="red",
                       fg="white",
                       command=return_book)
button_return.pack(side="left", padx=5, pady=5)

root.mainloop()
