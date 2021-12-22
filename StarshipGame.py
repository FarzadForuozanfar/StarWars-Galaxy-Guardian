from random import randint
import arcade
from time import time
import math

from arcade.key import S
SCREEN_WIDTh = 800
SCREEN_HEIGHT = 600

def Random_Enemy_arrival_time():
    return randint(4,6)


class StarShip(arcade.Sprite):
    def __init__(self):
        super().__init__("ship.png")
        self.center_x = SCREEN_WIDTh // 2
        self.center_y= 32
        self.width = 65
        self.height = 65
        self.angle = 0
        self.speed = 25
        self.bullet_list = []
        self.score = 0
        self.health = 3
        self.health_pic = arcade.load_texture('heart.png')
    def Fire(self):
        self.bullet_list.append(Bullet(self))
        arcade.play_sound(arcade.sound.Sound(':resources:sounds/laser3.wav'), 1, 0,False)
class Bullet(arcade.Sprite):

    def __init__(self, host):
        super().__init__('laser.png')
        self.speed = 5
        self.angle = host.angle
        self.center_x = host.center_x
        self.center_y = host.center_y
    
    def move(self):
        angle_radious = math.radians(self.angle)
        self.center_x -= self.speed * math.sin(angle_radious)
        self.center_y += self.speed * math.cos(angle_radious)
    
class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__("enemy.png")
        self.center_x = randint(0, SCREEN_WIDTh)
        self.center_y= SCREEN_HEIGHT + 28
        self.width = 55
        self.height = 55
        self.angle = 0
        self.speed = 4

    def move(self):
        self.center_y -= self.speed

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTh, SCREEN_HEIGHT, "🚀 Star War Game 🚀")
        arcade.set_background_color(arcade.color.BLACK)
        self.background_img = arcade.load_texture("staes.jpg")
        self.me = StarShip()
        self.enemy_list = []
        self.start_time = time()
        self.game_over = False
    def on_draw(self):
        arcade.start_render()
        if self.me.health < 1:
            
            self.game_over= True
            arcade.draw_text('GAME OVER', 220,300,arcade.color.SNOW,45)
            arcade.play_sound(arcade.sound.Sound(':resources:sounds/gameover5.wav'), 0.5, 0,False)
            
        else:
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTh, SCREEN_HEIGHT, self.background_img)
            self.me.draw()
            for bullet in self.me.bullet_list:
                bullet.draw()
            for enemy in self.enemy_list:
                enemy.draw()
            for i in range(self.me.health):
                arcade.draw_lrwh_rectangle_textured(i*30 + 5,15 ,28,28 ,self.me.health_pic)
            arcade.draw_text(f"Score: {self.me.score}", 700, 10, arcade.color.APPLE_GREEN, 15)
    def on_update(self, delta_time: float):
        for enemy in self.enemy_list:
            for bullet in self.me.bullet_list:
                if arcade.check_for_collision(bullet, enemy):
                    arcade.play_sound(arcade.sound.Sound(':resources:sounds/hit1.wav'),1,0,False)
                    self.enemy_list.remove(enemy)
                    self.me.bullet_list.remove(bullet)
                    self.me.score += 1
                if bullet.center_x > 800 or bullet.center_y > 600 or bullet.center_x < 0 or bullet.center_y < 0:
                    self.me.bullet_list.remove(bullet)

        for enemy in self.enemy_list:
            if enemy.center_y < 0:
                self.me.health -= 1
                self.enemy_list.remove(enemy)
   
        self.end_time = time()
        if self.end_time - self.start_time > Random_Enemy_arrival_time():
            self.enemy_list.append(Enemy())
            self.start_time = time()  
        for enemy in self.enemy_list:
            enemy.move()
        for bullet in self.me.bullet_list:
            bullet.move()
        for i in range(len(self.me.bullet_list)):
            self.me.bullet_list[i].move()
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            self.me.Fire()
        elif symbol == arcade.key.NUM_4:
            self.me.angle += 15
        elif symbol == arcade.key.NUM_6:
            self.me.angle -= 15
        elif symbol == arcade.key.LEFT:
            self.me.center_x -= self.me.speed
        elif symbol == arcade.key.RIGHT:
            self.me.center_x += self.me.speed
        elif symbol == arcade.key.UP:
            self.me.center_y += self.me.speed
        elif symbol == arcade.key.DOWN:
            self.me.center_y -= self.me.speed

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.NUM_4:
            self.me.angle += 15
        elif symbol == arcade.key.NUM_6:
            self.me.angle -= 15
        elif symbol == arcade.key.LEFT:
            self.me.center_x -= self.me.speed
        elif symbol == arcade.key.RIGHT:
            self.me.center_x += self.me.speed
        elif symbol == arcade.key.UP:
            self.me.center_y += self.me.speed
        elif symbol == arcade.key.DOWN:
            self.me.center_y -= self.me.speed
game =Game()
if game.game_over == False:
    arcade.play_sound(arcade.sound.Sound("main_sound.mp3"),2,0,True)
arcade.run()
