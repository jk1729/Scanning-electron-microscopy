import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Constants
R = 1.0
omega = 2 * np.pi
num_points = 400

# Angle values
theta = np.linspace(0, 2 * np.pi, num_points)

# Create 5x2 subplot grid
fig, axes = plt.subplots(
    5,
    2,
    figsize=(8, 10),
    subplot_kw={"aspect": "equal"}
)

axes = axes.flatten()

lines = []
titles = []

# Initialize each subplot
for i, ax in enumerate(axes, start=1):
    # Draw reference circle
    ax.plot(R * np.cos(theta), R * np.sin(theta), "k--", lw=0.5)

    # Animated line
    line, = ax.plot([], [], lw=2)
    lines.append(line)

    # Axis settings
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xticks([])
    ax.set_yticks([])

    # Title
    titles.append(ax.set_title(f"n = {i}"))

plt.tight_layout()


def animate(frame):
    t = frame / 30.0

    for i, line in enumerate(lines, start=1):
        n = i
        k = n / R

        displacement = 0.1 * np.sin(k * R * theta - omega * t)

        x = (R + displacement) * np.cos(theta)
        y = (R + displacement) * np.sin(theta)

        line.set_data(x, y)

    return lines


# Create animation
ani = animation.FuncAnimation(
    fig,
    animate,
    frames=200,
    interval=50,
    blit=True
)

plt.show()
