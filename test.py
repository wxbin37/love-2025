#!/usr/bin/python3
import math
import random
import time
import turtle
from turtle import Turtle, Screen

# 自定义向量类替代第三方库
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    @property
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __iter__(self):
        yield self.x
        yield self.y

# 颜色渐变函数
def color_shift():
    r = abs(math.sin(time.time() * 0.5))
    g = abs(math.sin(time.time() * 0.7))
    b = abs(math.sin(time.time() * 0.9))
    return (r, g, b)

class LoveFirework:
    def __init__(self):
        self.screen = Screen()
        self.screen.setup(800, 600)
        self.screen.bgcolor('black')
        self.screen.title('粒子爱心烟花')
        self.screen.tracer(0)

        self.particles = []
        self.stars = []
        self.create_stars()

    def create_stars(self):
        for _ in range(100):
            star = Turtle(visible=False)
            star.penup()
            star.color('white')
            star.shape('circle')
            star.shapesize(random.random()*0.3)
            star.setpos(
                random.randint(-380, 380),
                random.randint(-280, 280)
            )
            star.showturtle()
            self.stars.append(star)

    def heart_param(self, t):
        """改良心形参数方程"""
        x = 16 * (math.sin(t)**3)
        y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
        return Vector(x, y)

    def create_particle(self, pos):
        p = Turtle(visible=False)
        p.penup()
        p.setpos(pos.x, pos.y)
        p.color(color_shift())
        p.shape('circle')
        p.shapesize(random.random()*0.5 + 0.3)
        p.showturtle()
        return p

    def launch(self):
        def launch_cycle():
            # 烟花发射起点
            start_pos = Vector(random.random()*400-200, -280)
            firework = self.create_particle(start_pos)
            velocity = Vector(0, 15)

            # 发射轨迹
            while velocity.y > 0:
                firework.setpos(
                    firework.xcor() + velocity.x,
                    firework.ycor() + velocity.y
                )
                velocity.y -= 0.4
                self.screen.update()

            # 触发爆炸
            self.explode(Vector(firework.xcor(), firework.ycor()))
            firework.hideturtle()
            self.screen.ontimer(launch_cycle, 2000)  # 2秒发射间隔

        launch_cycle()
        self.screen.mainloop()

    def explode(self, pos):
        # 生成心形粒子
        for t in range(0, 314, 2):
            rad = math.radians(t)
            base = self.heart_param(rad)
            offset = Vector(
                random.random()*2 - 1,
                random.random()*2 - 1
            )
            direction = base + offset
            self.particles.append({
                'turtle': self.create_particle(pos),
                'vector': direction
            })

        self.animate_particles()

    def animate_particles(self):
        for particle in self.particles[:]:
            t = particle['turtle']
            vec = particle['vector'] * 0.95

            t.setpos(
                t.xcor() + vec.x,
                t.ycor() + vec.y
            )
            t.color(color_shift())

            # 粒子淡出处理
            if vec.magnitude < 0.5:
                t.hideturtle()
                self.particles.remove(particle)

        self.screen.update()
        if self.particles:
            self.screen.ontimer(self.animate_particles, 30)

if __name__ == '__main__':
    demo = LoveFirework()
    demo.launch()