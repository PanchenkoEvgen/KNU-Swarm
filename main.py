import math
import matplotlib.pyplot as plt
import random
from matplotlib.animation import FuncAnimation

N = 20 #кількість "мурах"
T = 100 #кількість переміщень

x_min = 0
x_max = 100
y_min = 0
y_max = 100
V_min = -5 #для задання швидкості
V_max = 5

g = [15,39]

w = 0.7
wp = 2
wg = 2

class Ant:
    def __init__(self,n, x, y, vx, vy, px, py, rp, rg):
        self.n = n
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.px = px
        self.py = py
        self.rp = rp
        self.rg = rg
    def move(self):
        self.x = self.x + self.vx
        if self.x > x_max:
            self.vx = -self.vx
            self.x = 100
        if self.x < x_min:
            self.vx = -self.vx
            self.x = 0
        self.y = self.y + self.vy
        if self.y > y_max:
            self.vy = -self.vy
            self.y = 100
        if self.y < y_min:
            self.vy = -self.vy
            self.y = 0
        if func(self.x, self.y) < func(self.px, self.py):
            self.px = self.x
            self.py = self.y
        self.vx = w*self.vx + self.rp*wp*(self.px - self.x) + self.rg*wg*(g[0] - self.x)
        if self.vx > V_max:
            self.vx = V_max
        if self.vx < V_min:
            self.vx = V_min
        self.vy = w*self.vy + self.rp*wp*(self.py - self.y) + self.rg*wg*(g[1] - self.y)
        if self.vy > V_max:
            self.vy = V_max
        if self.vy < V_min:
            self.vy = V_min
    def stats(self):
        print(self.n, self.x, self.y, self.vx, self.vy, self.px, self.py)


def func(x, y):
    # return (x-50)**2 + (y-50)**2
    return x+y

def generate_swarm(num):
    swarm = []
    global g
    for i in range(num):
        xi = random.uniform(x_min, x_max)
        yi = random.uniform(y_min, y_max)
        if func(xi, yi) < func(g[0],g[1]):
            g = [xi, yi]
        Vi1 = random.uniform(V_min, V_max)
        Vi2 = random.uniform(V_min, V_max)
        rp = random.uniform(0,1)
        rg = random.uniform(0,1)
        swarm.append(Ant(i+1, xi, yi, Vi1, Vi2, xi, yi, rp, rg))
    return swarm

def move_phase(swarm):
    global g
    for a in swarm:
        a.move()
        if func(a.x, a.y) < func(g[0],g[1]):
            g = [a.x, a.y]

fig, ax = plt.subplots()

ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

swarm = generate_swarm(N)

def update(frame):
    ax.clear()
    print(frame)
    ax.set_title(f"Слайд {frame}")
    ax.scatter(x_max, y_max, color = "white")
    ax.scatter(x_min, y_min, color = "white")
    move_phase(swarm)
    for a in swarm:
            a.stats()
            ax.scatter(a.x, a.y, color = "orange")

ani = FuncAnimation(fig, update, frames=T, interval=500)
plt.show()
print(g)