#For everything to work, you need to have the asd and fiv libraries preinstalled and that the photos from which you want to get encodings are in the same folder with the code.
#The whole program is made functional in case you need to encode not the whole face, but its individual parts.

import face_recognition as fr
import cv2

image_fr = fr.load_image_file('1.jpg')
image_cv = cv2.imread('1.jpg')
landmarks = fr.face_landmarks(image_fr)[0]
keys = ['chin', 'left_eyebrow', 'right_eyebrow', 'nose_bridge', 'nose_tip', 'left_eye', 'right_eye', 'top_lip', 'bottom_lip']

def landmarks_out(landmarks = landmarks, keys = keys):
    '''
    постепенный вывод всех точек словаря landmarks
    '''
    for key in keys:
        ch = landmarks[key]
        flag = False
        for point in ch:
            cv2.circle(image_cv, point, 1, (0, 0, 255), 5)
            if flag == True:
                cv2.line(image_cv, point, last_p, (0, 0, 255), 1)
            flag = True
            last_p = point
            cv2.imshow('kkk', image_cv)
            cv2.waitKey(0)
    cv2.imshow('kkk', image_cv)
    cv2.waitKey(0)

def chin(key = keys[0], landmarks = landmarks):
    '''
    return: возвращает следующий список:
     1 элемент - ширина челючсти
     2 элемент - высота челюсти
    '''

    lst = []
    left_point_chin, right_point_chin = landmarks[key][0], landmarks[key][-1]

    a = abs(left_point_chin[0] - right_point_chin[0])
    b = abs(left_point_chin[1] - right_point_chin[1])
    res_1 = (a**2 + b**2) ** 0.5

    median_y_up = int((left_point_chin[1] + right_point_chin[1]) / 2) #среднее расстояние по оси y верхней части челюсти
    median_x_up = int((left_point_chin[0] + right_point_chin[0]) / 2) #среднее расстояние по оси x верхней части челюсти
    median_y_down = int((landmarks[key][7][1] + landmarks[key][8][1] + landmarks[key][9][1]) / 3) #среднее расстояние по оси y нижней части челюсти
    median_x_down = int((landmarks[key][7][0] + landmarks[key][8][0] + landmarks[key][9][0]) / 3) #среднее расстояние по оси x верхней части челюсти

    a =  abs(median_x_down - median_x_up)
    b = abs(median_y_up - median_y_down)
    res_2 = (a**2 + b**2) ** 0.5

    lst.append(res_1)
    lst.append(res_2)

    '''
    #вывод сравниваемых точек
    
    cv2.circle(image_cv, (left_point_chin), 1, (0, 0, 255), 5)
    cv2.circle(image_cv, (right_point_chin), 1, (0, 0, 255), 5)
    cv2.line(image_cv, left_point_chin, right_point_chin, (0, 0, 255), 1)

    cv2.circle(image_cv, (median_x_up, median_y_up), 1, (0, 0, 255), 5)
    cv2.circle(image_cv, (median_x_down, median_y_down), 1, (0, 0, 255), 5)
    cv2.line(image_cv, (median_x_up, median_y_up), (median_x_down, median_y_down), (0, 0, 255), 1)

    cv2.imshow('kkk', image_cv)
    cv2.waitKey(0)
    '''

    return lst

def eyebrows(key_eyebrow_left = landmarks[keys[1]], key_eyebrow_right = landmarks[keys[2]]):
    '''
    return: возвращает следующий списокЖ
    1 элемент - средняя длина брови
    2 элемент - средняя высота брови
    3 элемент - кратчайшее расстояние между бровями
    4 элемент - широчайшее расстояние между бровями
    '''

    lst = []
    for eyebrows in (key_eyebrow_left, key_eyebrow_right): #длина всех точек брови
        last_point = eyebrows[0]
        res = 0
        for index_point in range(1, len(eyebrows)):
            a = abs(last_point[0] - eyebrows[index_point][0])
            b = abs(last_point[1] - eyebrows[index_point][1])
            res += (a ** 2 + b ** 2) ** 0.5
            last_point = eyebrows[index_point]
        lst.append(res)
    average_length = (lst[0] + lst[1]) / 2

    a = abs(key_eyebrow_left[0][0] - key_eyebrow_left[-1][0])
    b = abs(key_eyebrow_left[0][1] - key_eyebrow_left[-1][1])
    res_1 = (a ** 2 + b ** 2) ** 0.5
    a = abs(key_eyebrow_right[0][0] - key_eyebrow_right[-1][0])
    b = abs(key_eyebrow_right[0][1] - key_eyebrow_right[-1][1])
    res_2 = (a ** 2 + b ** 2) ** 0.5
    diagonal = (res_1 + res_2) / 2

    a = abs(key_eyebrow_left[-1][0] - key_eyebrow_right[0][0])
    b = abs(key_eyebrow_left[-1][1] - key_eyebrow_right[0][1])
    min_dist = (a ** 2 + b ** 2) ** 0.5 #кратчайшее расстояние

    a = abs(key_eyebrow_left[0][0] - key_eyebrow_right[-1][0])
    b = abs(key_eyebrow_left[0][1] - key_eyebrow_right[-1][1])
    max_dist = (a ** 2 + b ** 2) ** 0.5 #расстояние крайних точек

    '''
    #вывод сравниваемых точек

    for list in (key_eyebrow_left, key_eyebrow_right):
        last_point = list[0]
        for point in list:
            cv2.circle(image_cv, point, 1, (0, 0, 255), 5)
            cv2.circle(image_cv, point, 1, (0, 0, 255), 5)
            cv2.line(image_cv, last_point, point, (0, 0, 255), 1)
            last_point = point
            cv2.imshow('kkk', image_cv)
            cv2.waitKey(0)

    cv2.line(image_cv, key_eyebrow_left[0], key_eyebrow_left[-1], (0, 0, 255), 1)
    cv2.line(image_cv, key_eyebrow_right[0], key_eyebrow_right[-1], (0, 0, 255), 1)
    last_point = point
    cv2.imshow('kkk', image_cv)
    cv2.waitKey(0)
    cv2.line(image_cv, key_eyebrow_left[-1], key_eyebrow_right[0], (0, 0, 255), 1)
    cv2.imshow('kkk', image_cv)
    cv2.waitKey(0)
    cv2.line(image_cv, key_eyebrow_left[0], key_eyebrow_right[-1], (0, 0, 255), 1)
    cv2.imshow('kkk', image_cv)
    cv2.waitKey(0)
    '''

    return [average_length, diagonal, min_dist, max_dist]

def nose(bridge=landmarks[keys[3]], tip=landmarks[keys[4]]):
    '''
    return: возвращает следующий списокЖ
    1 элемент - высота носа
    2 элемент - ширина носа
    '''
    a = abs(bridge[0][0] - tip[2][0])
    b = abs(bridge[0][1] - tip[2][1])
    res_1 = (a ** 2 + b ** 2) ** 0.5

    a = abs(tip[0][0] - tip[-1][0])
    b = abs(tip[0][1] - tip[-1][1])
    res_2 = (a ** 2 + b ** 2) ** 0.5

    '''
    #вывод сравниваемых точек

    cv2.circle(image_cv, bridge[0], 1, (0, 0, 255), 5)
    cv2.circle(image_cv, tip[2], 1, (0, 0, 255), 5)
    cv2.line(image_cv, bridge[0], tip[2], (0, 0, 255), 1)
    cv2.circle(image_cv, tip[0], 1, (0, 0, 255), 5)
    cv2.circle(image_cv, tip[-1], 1, (0, 0, 255), 5)
    cv2.line(image_cv, tip[0], tip[-1], (0, 0, 255), 1)
    cv2.imshow('kkk', image_cv)
    cv2.waitKey(0)
    '''

    return [res_1, res_2]

def eyes(left_eye=landmarks[keys[5]], right_eye=landmarks[keys[6]]):
    '''
    return: возвращает следующий списокЖ
    1 элемент - средняя ширина глаз
    2 элемент - средняя высота глаз
    '''

    a = abs(left_eye[0][0] - left_eye[3][0])
    b = abs(left_eye[0][1] - left_eye[3][1])
    res_1 = (a ** 2 + b ** 2) ** 0.5

    a = abs(right_eye[0][0] - right_eye[3][0])
    b = abs(right_eye[0][1] - right_eye[3][1])
    res_2 = (a ** 2 + b ** 2) ** 0.5

    median_width = (res_1 + res_2) / 2

    a = abs(left_eye[1][0] + left_eye[2][0]) / 2
    b = abs(left_eye[1][1] + left_eye[2][1]) / 2
    median_up_left = (int(a), int(b))
    a = abs(left_eye[4][0] + left_eye[5][0]) / 2
    b = abs(left_eye[4][1] + left_eye[5][1]) / 2
    median_down_left = (int(a), int(b))
    a = abs(median_up_left[0] - median_down_left[0])
    b = abs(median_up_left[0] - median_down_left[0])
    median_left = (a ** 2 + b ** 2) ** 0.5

    a = abs(right_eye[1][0] + right_eye[2][0]) / 2
    b = abs(right_eye[1][1] + right_eye[2][1]) / 2
    median_up_right = (int(a), int(b))
    a = abs(right_eye[4][0] + right_eye[5][0]) / 2
    b = abs(right_eye[4][1] + right_eye[5][1]) / 2
    median_down_right = (int(a), int(b))
    a = abs(median_up_right[0] - median_down_right[0])
    b = abs(median_up_right[0] - median_down_right[0])
    median_right = (a ** 2 + b ** 2) ** 0.5

    median_height = (median_right + median_left) / 2

    '''
    #вывод сравниваемых точек

    cv2.circle(image_cv, median_up_left, 1, (0, 0, 255), 5)
    cv2.circle(image_cv, median_down_left, 1, (0, 0, 255), 5)
    cv2.line(image_cv, median_up_left,  median_down_left, (0, 0, 255), 1)
    cv2.circle(image_cv, median_up_right, 1, (0, 0, 255), 5)
    cv2.circle(image_cv, median_down_right, 1, (0, 0, 255), 5)
    cv2.line(image_cv, median_up_right, median_down_right, (0, 0, 255), 1)
    cv2.line(image_cv, left_eye[0] , left_eye[3], (0, 0, 255), 1)
    cv2.line(image_cv, right_eye[0] , right_eye[3], (0, 0, 255), 1)
    cv2.imshow('kkk', image_cv)
    cv2.waitKey(0)
    '''

    return [median_width, median_height]

def lips(top_lip = landmarks[keys[7]], bottom_lip = landmarks[keys[8]]):
    '''
    return: возвращает следующий списокЖ
    1 элемент - ширина губ
    2 элемент - высота верхней губы
    3 элемент - высота нижней губы
    '''

    a = abs(top_lip[0][0] - top_lip[6][0])
    b = abs(top_lip[0][1] - top_lip[6][1])
    width = (a**2 + b**2) ** 0.5

    a = abs(top_lip[2][0] - top_lip[10][0])
    b = abs(top_lip[2][1] - top_lip[10][1])
    x = (a**2 + b**2) ** 0.5
    a = abs(top_lip[3][0] - top_lip[9][0])
    b = abs(top_lip[3][1] - top_lip[9][1])
    y = (a ** 2 + b ** 2) ** 0.5
    a = abs(top_lip[4][0] - top_lip[8][0])
    b = abs(top_lip[4][1] - top_lip[8][1])
    z = (a ** 2 + b ** 2) ** 0.5
    median_top_height = (x + y + z) / 3

    a = abs(bottom_lip[2][0] - bottom_lip[10][0])
    b = abs(bottom_lip[2][1] - bottom_lip[10][1])
    x = (a ** 2 + b ** 2) ** 0.5
    a = abs(bottom_lip[3][0] - bottom_lip[9][0])
    b = abs(bottom_lip[3][1] - bottom_lip[9][1])
    y = (a ** 2 + b ** 2) ** 0.5
    a = abs(top_lip[4][0] - bottom_lip[8][0])
    b = abs(bottom_lip[4][1] - bottom_lip[8][1])
    z = (a ** 2 + b ** 2) ** 0.5
    median_bottom_height = (x + y + z) / 3

    '''
    #вывод сравниваемых точек

    cv2.circle(image_cv, top_lip[0], 1, (0, 0, 255), 5)
    cv2.circle(image_cv, top_lip[6], 1, (0, 0, 255), 5)
    cv2.line(image_cv, top_lip[0], top_lip[6], (0, 0, 255), 1)

    cv2.circle(image_cv, top_lip[2], 1, (0, 0, 255), 5)
    cv2.circle(image_cv, top_lip[10], 1, (0, 0, 255), 5)
    cv2.line(image_cv, top_lip[2], top_lip[10], (0, 0, 255), 1)

    cv2.circle(image_cv, top_lip[3], 1, (0, 0, 255), 5)
    cv2.circle(image_cv, top_lip[9], 1, (0, 0, 255), 5)
    cv2.line(image_cv, top_lip[3] , top_lip[9], (0, 0, 255), 1)

    cv2.circle(image_cv, top_lip[4], 1, (0, 0, 255), 5)
    cv2.circle(image_cv, top_lip[8], 1, (0, 0, 255), 5)
    cv2.line(image_cv, top_lip[4], top_lip[8], (0, 0, 255), 1)

    cv2.circle(image_cv, bottom_lip[2], 1, (0, 0, 255), 5)
    cv2.circle(image_cv, bottom_lip[10], 1, (0, 0, 255), 5)
    cv2.line(image_cv, bottom_lip[2], bottom_lip[10], (0, 0, 255), 1)

    cv2.circle(image_cv, bottom_lip[3], 1, (0, 0, 255), 5)
    cv2.circle(image_cv, bottom_lip[9], 1, (0, 0, 255), 5)
    cv2.line(image_cv, bottom_lip[3] , bottom_lip[9], (0, 0, 255), 1)

    cv2.circle(image_cv, bottom_lip[4], 1, (0, 0, 255), 5)
    cv2.circle(image_cv, bottom_lip[8], 1, (0, 0, 255), 5)
    cv2.line(image_cv, bottom_lip[4], bottom_lip[8], (0, 0, 255), 1)
    cv2.imshow('kkk', image_cv)
    cv2.waitKey(0)
    '''

    return [width, median_top_height, median_bottom_height]

