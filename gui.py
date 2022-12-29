#!/usr/bin/env python
# coding=utf-8
# Created by Valera at 19.11.2022

"""
def switch():
    if b1["state"] == "normal":
        b1["state"] = "disabled"
        b2["text"] = "enable"
    else:
        b1["state"] = "normal"
        b2["text"] = "disable"


"""


import Tkinter as tk

import random
import time
import math
from ttk import Combobox, Frame, Scale, Style, Button
import tkFileDialog
from Tkinter import Canvas, LEFT, RIGHT, TOP, IntVar, DoubleVar, StringVar
from ACO import ant_colony


class Settings():
    # Можно ли запустить на исполнение?
    isRunASO = False
    # Можно ли сохранить?
    isSave = False
    # Можно ли рисовать?
    isEnableDraw = False
    drawCounterDots = 0

    nodes = {0: (0, 7), 1: (3, 9), 2: (12, 4), 3: (14, 11), 4: (8, 11),
              5: (15, 6), 6: (6, 15), 7: (15, 9), 8: (12, 10), 9: (10, 7)}
    zoom = 50
    # Ответ решения задачи (массив путей)
    answer = []
    # Размер точки  на экране муравьиного
    canvasDotSize = 3
    # Какой из вариантов отобразить -1 последний
    drawAnswerPositionAnswer = -1

    # Какое минимальное расстояние
    minDistance = 0

    def __init__(self):
        self.varZoom = DoubleVar()
        self.varZoom.set(self.zoom)
        self.varZoom.trace("w", self.changeZoom)

    def changeZoom(self, v, i, m):
        self.zoom = self.varZoom.get()

        drawMapByNodes(s, c)
        drawAnswer(s, c)
        print(self.zoom)



# ******** Методы ********

def distance(start, end):
    x_distance = abs(start[0] - end[0])
    y_distance = abs(start[1] - end[1])

    import math
    return math.sqrt(pow(x_distance, 2) + pow(y_distance, 2))

def runACO():
    global s
    global c
    global lMinDistance
    print("Запуск муравьиного алгоритма")
    colony = ant_colony(s.nodes, distance)
    answer = colony.mainloopMultipleResult()
    s.answer = answer
    drawAnswer(s, c)

    # Считаем дистанцию
    minDistance = 0
    for i, startNode in enumerate(s.answer[s.drawAnswerPositionAnswer]):
        if i+1 < len(s.answer[s.drawAnswerPositionAnswer]):
            endNode = s.answer[s.drawAnswerPositionAnswer][i+1]
            minDistance += distance(s.nodes[startNode], s.nodes[endNode])
    print("minDistance", minDistance)
    lMinDistance.config(text="Мин. расстояние: "+str(round(minDistance, 1)))

    # Выключаем рисование
    s.isEnableDraw = False


def generateACO():
    global s, c
    print("Cгенерировать задачу")
    drawClear()
    # Очищаем ноды
    s.nodes = {}
    s.answer = []
    # Начинаем с первой (нулевой) точки
    s.drawCounterDots = 0


    numsNodes = random.randint(2, 40)

    for _ in range(numsNodes):
        s.nodes[s.drawCounterDots] = (random.randint(0, c.winfo_width()), random.randint(0, c.winfo_height()))
        s.drawCounterDots += 1

    # Устанавливаем масштаб в 100% т.е. без масштаба
    s.varZoom.set(1)

def saveACO():
    print("Сохранить задачу")
    f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")
    f.write("EDGE_WEIGHT_TYPE : ATT\n")
    f.write("NODE_COORD_SECTION\n")
    for x in s.nodes:
        f.write(str(x) + " " + str(s.nodes[x][0]) + " " + str(s.nodes[x][1]) + "\n")
    f.close()


def loadACO():
    print("Загрузить задачу")
    filedescriptor = tkFileDialog.askopenfile()
    print(filedescriptor)
    ##############
    # Тип задания вершин
    EDGE_WEIGHT_TYPE = ""
    #############
    nodes = {}
    isNodeSectionATT = False
    for line in filedescriptor:
        line = line.replace("\n", "")

        if line.startswith("EDGE_WEIGHT_TYPE"):
            _, EDGE_WEIGHT_TYPE = line.split(" : ")
            EDGE_WEIGHT_TYPE = EDGE_WEIGHT_TYPE
            print("EDGE_WEIGHT_TYPE ", EDGE_WEIGHT_TYPE)
            continue
        if line.startswith("NODE_COORD_SECTION") and (EDGE_WEIGHT_TYPE == "ATT"):
            isNodeSectionATT = True
            print("Next lines is coords")
            continue
        if isNodeSectionATT:
            print("Line", line[0], line[0] in "0123456789")
            if line[0] in "0123456789":
                nodeID, x, y = line.split(" ")
                print ("nodeID, x, y", nodeID, x, y)
                nodes[int(nodeID)] = (float(x), float(y))
                continue
            else:
                isNodeSectionATT = False
    print ("Загрузка завершена")
    print ("Nodes", nodes)
    drawClear()
    # Очищаем ноды
    s.nodes = nodes
    s.answer = []

    # Ищем максимальную высоту/ширину для скалирования
    max = 0
    for x in nodes:
        if nodes[x][0] > max:
            max = nodes[x][0]
        if nodes[x][1] > max:
            max = nodes[x][1]

    # Устанавливаем масштаб в расчетный
    s.varZoom.set( c.winfo_width() / max)

def drawACO():
    print("В режиме рисования")
    drawClear()
    # Очищаем ноды
    s.nodes = {}
    s.answer = []
    # Включаем рисование
    s.isEnableDraw = True
    # Начинаем с первой (нулевой) точки
    s.drawCounterDots = 0
    # Устанавливаем масштаб в 100% т.е. без масштаба
    s.varZoom.set(1)


# ****** Рисование
def clickPointDraw(event):
    global s, c
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))
    if s.isEnableDraw:
        s.nodes[s.drawCounterDots] = (x, y)
        s.drawCounterDots += 1
        drawMapByNodes(s, c)
        print("Точка создана по координатам X: " + str(x) + " Y:" + str(y))

def generateRandomColor():
    color = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    return color


# **** canvas
def drawMapByNodes(s, canv):
    drawClear()
    for node in s.nodes:
        print("s.nodes[node]", s.nodes[node])
        print("s.nodes[node]0", s.nodes[node][0]*s.zoom)
        print("s.nodes[node]1", s.nodes[node][1]*s.zoom)
        print("node", node)

        canv.create_oval(s.nodes[node][0]*s.zoom,
                         s.nodes[node][1]*s.zoom,
                         s.nodes[node][0]*s.zoom+s.canvasDotSize,
                         s.nodes[node][1]*s.zoom+s.canvasDotSize,
                         fill="#000000"
                         )
        canv.create_text(s.nodes[node][0]*s.zoom + 1,
                         s.nodes[node][1]*s.zoom - 8,
                         text=str(node))


def drawAnswer(s, canv):
    if (len(s.answer) > 0) and (len(s.nodes) > 0):
        for i, node in enumerate(s.answer[s.drawAnswerPositionAnswer]):
            posXY = s.nodes[node]
            print("posxy", posXY)
            if i+1 < len(s.answer[s.drawAnswerPositionAnswer]):
                # print("s.answer[i+1]", s.answer[s.drawAnswerPositionAnswer][i+1])
                pos2XY = s.nodes[s.answer[s.drawAnswerPositionAnswer][i+1]]
                print("pos2XY", pos2XY)
                canv.create_line(posXY[0]*s.zoom+s.canvasDotSize/2,
                                 posXY[1]*s.zoom+s.canvasDotSize/2,
                                 pos2XY[0]*s.zoom+s.canvasDotSize/2,
                                 pos2XY[1]*s.zoom+s.canvasDotSize/2, fill=generateRandomColor())
            else:
                pos2XY = s.nodes[s.answer[s.drawAnswerPositionAnswer][0]]

                canv.create_line(posXY[0] * s.zoom + s.canvasDotSize / 2,
                                 posXY[1] * s.zoom + s.canvasDotSize / 2,
                                 pos2XY[0] * s.zoom + s.canvasDotSize / 2,
                                 pos2XY[1] * s.zoom + s.canvasDotSize / 2, fill=generateRandomColor())

            print(node)


def drawClear():
    global s
    global c
    c.create_rectangle(
        0, 0,
        c.winfo_width(),
        c.winfo_height(),
        fill="#ffffff"
    )
window = tk.Tk()
s = Settings()

#window.style.theme_use("alt")
window.option_add( "*font", "clearlyu 12" )
window.title("Лабораторная работа Сиренко В. Н. Муравьиный алгоритм")
window.geometry('1010x900')

c = Canvas(window, width=800, height=900, bg='white')
c.bind('<Button 1>', clickPointDraw)
c.pack(side=LEFT)




fRightPanel = Frame(window, width=200, height=900, style='My.TFrame')

fRightPanel.pack(side=RIGHT, anchor=tk.N)

btnRunACO = tk.Button(fRightPanel,
                        text="Запустить",
                        command=runACO,
                        width=22,
                        height=1
                      )
btnRunACO.pack(side=TOP)

btnGenerate = tk.Button(fRightPanel,
                        text="Сгенерировать",
                        command=generateACO,
                        width=22,
                        height=1)
btnGenerate.pack(side=TOP)

btnSave = tk.Button(fRightPanel,
                        text="Сохранить",
                        command=saveACO,
                        width=22,
                        height=1)
btnSave.pack(side=TOP)

btnLoad = tk.Button(fRightPanel,
                        text="Загрузить",
                        command=loadACO,
                        width=22,
                        height=1)
btnLoad.pack(side=TOP)

btnDraw = tk.Button(fRightPanel,
                        text="Нарисовать",
                        command=drawACO,
                        width=22,
                        height=1)
btnDraw.pack(side=TOP)

lZoom = tk.Label(fRightPanel, text="Увеличение")
lZoom.pack()

eZoom = tk.Entry(fRightPanel, width=30, textvariable=s.varZoom)
eZoom.pack(side=TOP)

lMinDistance = tk.Label(fRightPanel, text="Мин. расстояние: ")
lMinDistance.pack()

# Кнопки сгенерировать, нарисовать, сохранить в файл, загрузить из файла
def init():
    drawMapByNodes(s, c)

window.after(500, init)

window.mainloop()



