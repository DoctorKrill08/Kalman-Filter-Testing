from statistics import NormalDist
import matplotlib.pyplot as plt
import math

import random

class Limelight:
    @staticmethod
    def pose_to_sd(pose):
        return pose / 10;
    def __init__(self):
        self.actual = 50
        self.sd = self.pose_to_sd(self.actual)
        self.sdEstimate = self.sd
        self.reading = self.actual

    def setActual(self, actual):
        self.actual = actual
        self.sd = self.pose_to_sd(actual)

    def update(self):
        self.reading = random.normalvariate(self.actual,self.sd)
        self.sdEstimate = self.pose_to_sd(self.reading)


class KalmanFilter1D:
    def __init__(self, initial_estimate=1, initial_uncertainty=1):
        self.x = initial_estimate
        self.uncertainty = initial_uncertainty
        self.sd = 1
        self.prev_x = 0
        self.prev_measurement = 0
        self.prev_sd = 1

    def two_step_verification(self,measurement, measurement_sd):
        result = False
        if (measurement > self.prev_measurement):
            result = self.prev_measurement > measurement - (1.5 * measurement_sd)
        else:
            result = measurement > self.prev_measurement - (1.5 * self.prev_sd)
        self.prev_x = self.x
        self.prev_sd = measurement_sd
        self.prev_measurement = measurement
        return result
    def update(self, measurement, measurement_sd):
        variance_measure = measurement_sd ** 2
        #CUSTOMIZED normalize variance
        self.sd = Limelight.pose_to_sd(self.x)
        variance = self.sd ** 2
        if (not self.two_step_verification(measurement,measurement_sd)):
            return self.x
        delta_sd = abs(self.sd - measurement_sd)
        

        innovation = measurement - self.x

        z_score_of_error = abs(innovation) / measurement_sd
        # < 2 z-score -> nada. difference from 2
        Q = (z_score_of_error ** 3) * (0.0001 * abs(innovation)) + (0.02 * abs(self.prev_x - self.x))
        self.uncertainty = self.uncertainty + Q
        if (self.uncertainty > 1):
            self.uncertainty = 1
        print(Q)

        # --- NORMAL KALMAN UPDATE ---
        # K = self.uncertainty / (self.uncertainty + variance_measure)
        # Custom Kalman
        K = self.uncertainty
        if (K < 0.1):
            K = 0.1
        print(K)
        self.x = self.x + K * innovation
        #4 Sample rule (it should take about 4 samples from a spike to reach mean)
        #Therefore deterioation should be
        self.uncertainty = self.uncertainty / 1.4

        return self.x

n = 1
prev_average = 0
average = 0

prev_actual = 0

def resetMeanMeasure():
    global n
    n = 1
    global prev_average
    prev_average = limelight.reading
    global average 
    average = limelight.reading

# Simulation
limelight = Limelight()
kf = KalmanFilter1D()


for i in range(200):
    limelight.update()
    if prev_actual != limelight.actual:
        resetMeanMeasure()
    prev_actual = limelight.actual
    estimate = kf.update(limelight.reading, limelight.sdEstimate)
    plt.scatter(i,limelight.reading,color = "red")
    plt.scatter(i,estimate,color = "blue")
    plt.scatter(i,limelight.actual,color = "green")
    print(f"Measured: {limelight.reading:.2f}, Estimate: {estimate:.2f}, Actual: {limelight.actual}")
    #limelight.setActual(10 + (i/2))

    if i == 50:
        limelight.setActual(140)
    if i == 100:
        limelight.setActual(90)
    if i == 150:
          limelight.setActual(80) 
    if i == 200:
          limelight.setActual(50)
    if i > 200:
        limelight.setActual(i - 150)
    average = prev_average + (limelight.reading - prev_average)/n
    n = n + 1
    prev_average = average
    plt.scatter(i,average,color = "black")
    
plt.show()