from statistics import NormalDist
import random
import matplotlib.pyplot as plt

class Limelight:
    def __init__(self):
        self.actual = 50
        self.noise = 10
        self.sd = self.noise
        self.reading = self.actual
    def update(self):
        self.reading = self.noise * 2 * (0.5 - random.random()) + self.actual

class Kalman:
    def __init__(self): 
        self.pn = 100 #pinpoint num
        self.e = 0 #limelight pinpoint error
        self.z = 0 # z score
        self.area = 1 #area under curve
        self.d = 1 #pp drift aka weighting of limelight
        self.limelight = Limelight()

    def predict(self):
        d = 3
        ln = self.limelight.reading  
        self.z = abs(self.pn - ln)/(2 * self.limelight.sd)
        self.area = d * pow((NormalDist().cdf(self.z) - 0.5),2)
        self.d = self.d + self.area
        print(self.d)
        if self.d < 0:
            self.d = 0
        if self.d > 1:
            self.d = 1
    
    def update(self):
        p = 0.5
        LL = self.limelight
        self.pn = (self.pn * (1-self.d)) + (LL.reading * self.d)
        self.d = ((1 - self.d) * abs(self.d)) * p
        LL.update()

# Create data
x = []
p = []
l = []

kalman = Kalman()
for i in range (0,50):
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
    if i == 30:
        kalman.limelight.actual = 150
        print("TELEPORT!!!")

# Plot and display
plt.show()