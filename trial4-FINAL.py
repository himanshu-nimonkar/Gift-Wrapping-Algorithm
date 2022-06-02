from tkinter import *
import random


pointList = []
points = []


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class LinePlotLoop:


    def assignValues(self, n):
        self.n = n
        self.left = leftmostPointIndex()
        self.hull = []
        self.far = self.left
        self.next = 0
        self.i = 0
        self.blueLine = 0


    def rotation(self, farPoint, checkPoint, refPoint):

        crossProd = (checkPoint.y - farPoint.y) * (refPoint.x - checkPoint.x) - \
            (checkPoint.x - farPoint.x) * (refPoint.y - checkPoint.y)

        mainCanvas.delete(self.blueLine)

        self.blueLine = mainCanvas.create_line(
            points[self.far].x, points[self.far].y, points[self.i].x, points[self.i].y, width=3, fill="blue")
        pointList.append(self.blueLine)

        if crossProd == 0:
            return 0
        elif crossProd > 0:
            return 1
        else:
            return 2


    def plotLine(self):

        if (self.far == self.next) or (self.i == 0):

            self.hull.append(self.far)
            self.next = (self.far + 1) % self.n

            self.whiteLine = mainCanvas.create_line(
                points[self.far].x, points[self.far].y, points[self.next].x, points[self.next].y, width=4, fill='white')
            pointList.append(self.whiteLine)

        if(self.rotation(points[self.far],
                         points[self.i], points[self.next])) == 2:

            mainCanvas.delete(self.whiteLine)

            self.next = self.i

            self.whiteLine = mainCanvas.create_line(
                points[self.far].x, points[self.far].y, points[self.next].x, points[self.next].y, width=4, fill='white')
            pointList.append(self.whiteLine)

        self.i += 1

        if self.i == self.n:

            self.far = self.next
            self.i = 0

            if self.far != self.left:
                root.after(self.time, self.plotLine)

            else:
                mainCanvas.delete(self.blueLine)
                for each in self.hull:

                    pointObj = mainCanvas.create_oval(points[each].x - 10, points[each].y - 10,
                                                      points[each].x + 10, points[each].y + 10, fill="#00ff00")
                    pointList.append(pointObj)
                resetBtn.config(state="normal")
                plotBtn.config(state="disabled")
        else:
            root.after(self.time, self.plotLine)


    def updateTime(self, var):
        self.time = speedScale.get()


loopObj = LinePlotLoop()


def leftmostPointIndex():
    leftmost = 0

    for i in range(1, len(points)):

        if points[i].x < points[leftmost].x:
            leftmost = i

        elif points[i].x == points[leftmost].x:

            if points[i].y > points[leftmost].y:
                leftmost = i

    return leftmost


def pointGenerator():

    number = genScale.get()

    for _ in range(number):

        randomx = random.randrange(40, Xgrid-30)
        randomy = random.randrange(40, Ygrid-30)

        pointObj = mainCanvas.create_oval(
            randomx-6, randomy-6, randomx+6, randomy+6, fill="yellow")

        pointList.append(pointObj)
        points.append(Point(randomx, randomy))

    loopObj.assignValues(number)

    simuBtn.config(state="normal")
    resetBtn.config(state="normal")
    plotBtn.config(state="disabled")


def startSim():
    loopObj.plotLine()
    resetBtn.config(state="disabled")
    simuBtn.config(state="disabled")


def clearCanvas():

    points.clear()
    resetBtn.config(state="disabled")
    simuBtn.config(state="disabled")
    plotBtn.config(state="normal")
    
    if len(pointList) != 0:
        for _ in range(len(pointList)):
            mainCanvas.delete(pointList.pop())


root = Tk()
root.state("zoomed")
root.title("JARVIS MARCH (GIFT WRAPPING) ALGORITHM")
root.iconbitmap("present.ico")
root.configure(background='#272929')

screenheight = root.winfo_screenheight()
Xgrid = Ygrid = int((screenheight//10)*10 - (0.045*screenheight))

mainCanvas = Canvas(root, width=Xgrid,
                    height=Ygrid, bg="white", background='#000000')

for i in range(0, Xgrid, 40):
    mainCanvas.create_line(i, 0, i, Ygrid, fill="#191a19")

for i in range(0, Ygrid, 40):
    mainCanvas.create_line(0, i, Xgrid, i, fill="#191a19")


numLabel = Label(root, text="CHOOSE NUMBER OF DATA POINTS",
                 font=("Arial 16 bold"), foreground="#ffffff", bg='#272929')

genScale = Scale(root, from_=10, to=100, resolution=5, sliderlength=40,
                 length=400, orient='horizontal', width=20, foreground="#ffffff", bg="#545454", font="Arial 14 bold")

plotBtn = Button(root, text="PLOT DATA POINTS", font=(
    "Arial 14 bold"), foreground="#ffffff", bg="#545454", borderwidth=4, state="normal", command=pointGenerator)

simuBtn = Button(root, text="START JARVIS MARCH", font=(
    "Arial 14 bold"), foreground="#ffffff", bg="#545454", borderwidth=4, state="disabled", command=startSim)

resetBtn = Button(root, text="CLEAR CANVAS", font=(
    "Arial 14 bold"), foreground="#ffffff", bg="#545454", borderwidth=4, state="disabled", command=clearCanvas)

speedLabel = Label(root, text="CHOOSE SIMULATION SPEED", font=(
    "Arial 14 bold"), foreground="#ffffff", bg='#272929')

speedScale = Scale(root, from_=10, to=1000, resolution=10, sliderlength=40, width=20, length=400, orient='horizontal',
                   foreground="#ffffff", bg="#545454", font="Arial 14 bold", command=loopObj.updateTime)
speedScale.set(100)
tempLabel = Label(root, text="", foreground="#ffffff", bg='#272929')


mainCanvas.grid(row=0, column=0, rowspan=8, pady=8, padx=90)
numLabel.grid(row=0, column=1, sticky="S")
genScale.grid(row=1, column=1, sticky="N")
speedLabel.grid(row=2, column=1, sticky="S")
speedScale.grid(row=3, column=1, sticky="N")
plotBtn.grid(row=4, column=1, sticky="NWES")
simuBtn.grid(row=5, column=1, sticky="NWES")
resetBtn.grid(row=6, column=1, sticky="NWES")
tempLabel.grid(row=7, column=1, sticky="NWES")

root.mainloop()
