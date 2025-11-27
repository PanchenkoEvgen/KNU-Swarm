import math
import matplotlib.pyplot as plt
import random
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize
import numpy as np

N = 50 #кількість "мурах"
T = 100 #кількість переміщень

x_min = -4
x_max = 4
y_min = -4
y_max = 4
V_max = 0.1
V_min = -V_max #для задання швидкості

g = [15,39]

w = 0.7 #w = 0.3 w = 0.3 w = 0.9 w<1
wp = 1  #wp = 1  wp = 4  wp = 1  wp 1..5
wg = 3  #wg = 4  wg = 1  wg = 1  wg 1..5

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
            self.x = x_max
        if self.x < x_min:
            self.vx = -self.vx
            self.x = x_min
        self.y = self.y + self.vy
        if self.y > y_max:
            self.vy = -self.vy
            self.y = x_max
        if self.y < y_min:
            self.vy = -self.vy
            self.y = x_min
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
    return (0.2 * (abs(x) + abs(y)) 
            - 0.6 * math.cos(3*x + y) 
            - 0.5 * math.sin(x*y) 
            - 0.4 * abs(math.cos(2*x - y)))

def func_np(x, y):
    return (0.2 * (np.abs(x) + np.abs(y)) 
            - 0.6 * np.cos(3*x + y) 
            - 0.5 * np.sin(x*y) 
            - 0.4 * np.abs(np.cos(2*x - y)))

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
        rg = 1-rp
        swarm.append(Ant(i+1, xi, yi, Vi1, Vi2, xi, yi, rp, rg))
    return swarm

def move_phase(swarm):
    global g
    for a in swarm:
        # print(a.n)
        # print([a.x, a.y], g)
        # print(func(a.x, a.y), func(g[0],g[1]))
        if func(a.x, a.y) < func(g[0],g[1]):
            g = [a.x, a.y]
        # print(g)
        a.move()

fig, ax = plt.subplots()

ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

swarm = generate_swarm(N)

def last(swarm, T):
    t = 0
    while t < T:
        move_phase(swarm)
        t +=1
    ax.scatter(x_max, y_max, color = "white")
    ax.scatter(x_min, y_min, color = "white")
    x = np.linspace(x_min, x_max, 100)
    y = np.linspace(y_min, y_max, 100)
    X, Y = np.meshgrid(x, y)
    t = func_np(X, Y)
    ax.imshow(t, extent=[x_min, x_max, y_min, y_max], origin='lower',
    aspect='equal')
    for a in swarm:
            # a.stats()
            ax.scatter(a.x, a.y, color = "orange")
    plt.show()
    

def update(frame):
    ax.clear()
    ax.set_title(f"Слайд {frame}")
    ax.scatter(x_max, y_max, color = "white")
    ax.scatter(x_min, y_min, color = "white")
    x = np.linspace(x_min, x_max, 100)
    y = np.linspace(y_min, y_max, 100)
    X, Y = np.meshgrid(x, y)
    t = func_np(X, Y)
    ax.imshow(t, extent=[x_min, x_max, y_min, y_max], origin='lower',
    aspect='equal')
    move_phase(swarm)
    for a in swarm:
            # a.stats()
            ax.scatter(a.x, a.y, color = "orange")

# ani = FuncAnimation(fig, update, frames=T, interval=500)
# plt.show()

last(swarm, T)

print(g)
print(func(g[0], g[1]))
print(func_np(g[0], g[1]))
x = np.linspace(x_min, x_max, 100)
y = np.linspace(y_min, y_max, 100)
X, Y = np.meshgrid(x, y)
t = func_np(X, Y)
plt.imshow(t, extent=[x_min, x_max, y_min, y_max], origin='lower', aspect='equal')
plt.scatter(g[0],g[1], color = "pink")
plt.show()
