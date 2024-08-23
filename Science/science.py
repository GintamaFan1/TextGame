import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider

# Constants
g = 9.81  # acceleration due to gravity (m/s^2)

def plot_trajectory(v0, theta):
    theta_rad = np.radians(theta)  # convert angle to radians

    # Time array
    t_max = 2 * v0 * np.sin(theta_rad) / g  # time of flight
    t = np.linspace(0, t_max, num=500)  # time array

    # Equations of motion
    x = v0 * np.cos(theta_rad) * t
    y = v0 * np.sin(theta_rad) * t - 0.5 * g * t**2

    # Plotting the trajectory
    plt.figure(figsize=(10, 5))
    plt.plot(x, y)
    plt.title('Projectile Motion')
    plt.xlabel('Distance (m)')
    plt.ylabel('Height (m)')
    plt.grid(True)
    plt.ylim(bottom=0)  # Ensure the y-axis starts at 0
    plt.show()

# Create interactive widgets
v0_slider = FloatSlider(value=20.0, min=0.0, max=100.0, step=1.0, description='Initial Velocity (m/s)')
theta_slider = FloatSlider(value=45.0, min=0.0, max=90.0, step=1.0, description='Launch Angle (degrees)')

# Use interact to create the interactive plot
interact(plot_trajectory, v0=v0_slider, theta=theta_slider)