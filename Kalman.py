from statistics import NormalDist
import random
import matplotlib.pyplot as plt

class Limelight:
    def __init__(self):
        self.actual = 50
        self.sd = 10
        self.sdEstimate = self.sd
        self.reading = self.actual
    def setActual(self, actual):
        self.actual = actual
        self.sd = actual/5
    def update(self):
        self.reading = self.sd * 2 * (0.5 - random.random()) + self.actual
        self.sdEstimate = self.reading / 5

class Kalman:
    def __init__(self): 
        self.pn = 100 #pinpoint num
        self.e = 0 #limelight pinpoint error
        self.z = 0 # z score
        self.area = 1 #area under curve
        self.d = 1 #pp drift aka weighting of limelight
        self.limelight = Limelight()

    def predict(self):
        d = 1
        ln = self.limelight.reading  
        self.z = abs(self.pn - ln)/(2 * self.limelight.sdEstimate)
        deltaA = self.area
        self.area = d * pow((NormalDist().cdf(self.z) - 0.5),1)
        deltaA = abs(pow(deltaA,2) - pow(self.area,2))
        if (deltaA < 0.68):
            deltaA = 0
        self.d = self.d + self.area + deltaA
        print(self.d)
        if self.d < 0:
            self.d = 0
        if self.d > 1:
            self.d = 1
    
    def update(self):
        p = 1
        LL = self.limelight
        self.pn = (self.pn * (1-self.d)) + (LL.reading * self.d)
        self.d = ((1 - self.d) * abs(self.d)) * p
        LL.update()

# Create data
x = []
p = []
l = []

kalman = Kalman()
for i in range (0,100):
    print("------")
    print(i)
    kalman.predict()
    kalman.update()
    x.append(i)
    l.append(kalman.limelight.reading)
    p.append(kalman.pn)
    plt.scatter(x,l,color = "red")
    plt.scatter(x,p,color = "blue")
    print(f"Weighting {kalman.d}")
    print(f"Limelight reading {kalman.limelight.reading}")
    print(f"Pinpoint Estimate {kalman.pn}")
    if i == 40:
        kalman.limelight.setActual(130)
        print("TELEPORT!!!")
    if i == 60:
        kalman.limelight.setActual(30)
        print("TELEPORT!!!")
    if i == 80:
        kalman.limelight.setActual(90)
        print("TELEPORT!!!")
plt.show()