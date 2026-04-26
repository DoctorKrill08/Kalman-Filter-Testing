from statistics import NormalDist
import matplotlib.pyplot as plt
import math

import random

class Limelight:
    @staticmethod
    def pose_to_sd(pose):
        return pose / 5;
    def __init__(self):
        self.actual = 50
        self.sd = self.pose_to_sd(self.actual)
        self.sdEstimate = self.sd
        self.reading = self.actual

    def setActual(self, actual):
        self.actual = actual
        self.sd = self.pose_to_sd(actual)

    def update(self):
        self.reading = self.sd * 2 * (0.5 - random.random()) + self.actual
        self.sdEstimate = self.pose_to_sd(self.reading)


class KalmanFilter1D:
    def __init__(self, initial_estimate=1, initial_uncertainty=1000):
        self.x = initial_estimate
        self.P = initial_uncertainty

    def update(self, measurement, measurement_sd):
        R = measurement_sd ** 2

        innovation = measurement - self.x
        S = self.P + R

        # --- TELEPORT / OUTLIER DETECTION ---
        threshold = 1.5  # ~99.7% confidence (3-sigma rule)

        sdError = abs(Limelight.pose_to_sd(self.x) - measurement_sd)
        Q = (sdError / Limelight.pose_to_sd(self.x)) + abs(innovation)/(threshold * math.sqrt(abs(S)))

        if abs(innovation) > threshold * math.sqrt(abs(S)) or (Q > threshold):
            # Option A: hard reset (fastest recovery)
            self.x = measurement
            self.P = R
            return self.x

        self.P = self.P + Q

        # --- NORMAL KALMAN UPDATE ---
        K = self.P  * 2/ (self.P + R)
        self.x = self.x + K * innovation
        self.P = (1 - K) * self.P

        return self.x


# Simulation
limelight = Limelight()
kf = KalmanFilter1D()

for i in range(250):
    limelight.update()
    estimate = kf.update(limelight.reading, limelight.sdEstimate)
    plt.scatter(i,limelight.reading,color = "red")
    plt.scatter(i,estimate,color = "blue")
    print(f"Measured: {limelight.reading:.2f}, Estimate: {estimate:.2f}, Actual: {limelight.actual}")
    if i == 50:
        limelight.setActual(60)
    if i == 100:
        limelight.setActual(140)
    if i == 150:
        limelight.setActual(120)
    if i == 200:
        limelight.setActual(20)
plt.show()