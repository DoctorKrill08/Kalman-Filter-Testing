from statistics import NormalDist
import matplotlib.pyplot as plt
import math

import random

class Limelight:
    def __init__(self):
        self.actual = 50
        self.sd = 10
        self.sdEstimate = self.sd
        self.reading = self.actual

    def setActual(self, actual):
        self.actual = actual
        self.sd = actual / 5

    def update(self):
        self.reading = self.sd * 2 * (0.5 - random.random()) + self.actual
        self.sdEstimate = abs(self.reading) / 5


class KalmanFilter1D:
    def __init__(self, initial_estimate=0, initial_uncertainty=1000):
        self.x = initial_estimate
        self.P = initial_uncertainty

    def update(self, measurement, measurement_sd):
        R = measurement_sd ** 2

        innovation = measurement - self.x
        S = self.P + R

        # --- TELEPORT / OUTLIER DETECTION ---
        threshold = 3  # ~99.7% confidence (3-sigma rule)

        if abs(innovation) > threshold * math.sqrt(S):
            # Option A: hard reset (fastest recovery)
            self.x = measurement
            self.P = R
            return self.x

        # --- NORMAL KALMAN UPDATE ---
        K = self.P / (self.P + R)
        self.x = self.x + K * innovation
        self.P = (1 - K) * self.P

        return self.x


# Simulation
limelight = Limelight()
kf = KalmanFilter1D()

for i in range(150):
    limelight.update()
    estimate = kf.update(limelight.reading, limelight.sdEstimate)
    plt.scatter(i,limelight.reading,color = "red")
    plt.scatter(i,estimate,color = "blue")
    print(f"Measured: {limelight.reading:.2f}, Estimate: {estimate:.2f}, Actual: {limelight.actual}")
    if i == 50:
        limelight.setActual(140)
    if i == 100:
        limelight.setActual(90)
plt.show()