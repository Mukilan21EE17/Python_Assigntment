import pgzrun
from random import randint
HEIGHT =612
WIDTH = 612

white= (255,255,255)
black = (0,0,0)

car = Actor('car3')
car.bottom = HEIGHT
car.x = WIDTH / 2
car_velocity = 1

background1 = 'road'
background2 = 'road'
background_time = 1
back1 = Actor('road')
back2 = Actor('road')
g_backgrounds = [back1,back2]

score = 0
speed = 0

coins = []
enemies = []

game_over= False


def draw():
    screen.blit('road',(0,0))
    b1,b2 = g_backgrounds
    b1.draw()
    b2.draw()
    car.draw()
    if game_over:
        screen.draw.text('GAME\nOVER', (540,10), fontsize=30, color=white)
    elif score == 500:
        screen.draw.text('YOU\nWIN', (540, 10), fontsize=30, color=white)
    elif score >= 300:
        screen.draw.text('level 4\ncompleted', (540, 10), fontsize=20, color=black)
    elif score >= 160:
        screen.draw.text('level 3\ncompleted', (540,10), fontsize=20, color=black)
    elif score >= 60:
        screen.draw.text('level 2\ncompleted', (540, 10), fontsize=20, color=black)
    elif score >= 30:
        screen.draw.text('level 1\ncompleted', (540,10), fontsize=20, color=black)
    for coin in coins:
        coin.draw()
    for enemy in enemies:
        enemy.draw()

    screen.draw.text('SCORE:' + str(score), (0, 10), fontsize=20, color=black)
    screen.draw.text('SPEED:+' + str(speed), (0, 50), fontsize=18, color=black)


def background_repeat():
        b1 = g_backgrounds.pop(0)
        g_backgrounds.append(b1)
        scroll_backgrounds(g_backgrounds)
        return


def scroll_backgrounds(backs):
    b1,b2 =backs
    TOP= 306
    bottom = 306
    b1.pos = (TOP,bottom)
    animate(b1,tween='linear',duration=background_time,on_finished=background_repeat,pos=(TOP,bottom-612))
    b2.pos = (TOP,bottom+612)
    animate(b2,tween='linear',duration=background_time,on_finished=None,pos=(TOP,bottom))


def update():
        move_car()
        move_coins()
        move_enemies()
        check_car_boundary()
        check_coin_car_collision()
        check_car_collision()


def move_car():
    if not game_over:
        if keyboard.left:
            car.x -= 5
        if keyboard.right:
            car.x += 5


def move_coins():
    global speed
    if not game_over:
        if keyboard.up:
            sounds.acceleration.play()
            if speed != 220:
                speed += 1
            else:
                speed = 220
            for coin in coins:
                if coin.top > HEIGHT:
                    coins.remove(coin)
                    create_new_coin()
                else:
                    coin.y += 5

        else:
            scroll_backgrounds(g_backgrounds)
            sounds.acceleration.stop()
            if speed != 0:
                speed -= 1
            else:
                speed = 0
    else:
        scroll_backgrounds(g_backgrounds)
        if speed != 0:
            speed -= 1
        else:
            speed = 0


def move_enemies():
        for enemy in enemies:
            if enemy.top > HEIGHT:
                enemies.remove(enemy)
                create_new_enemy()
            else:
                enemy.y += 2


def check_car_boundary():
    if car.left < 100:
        car.left = 100
    elif car.right > 510:
        car.right = 510


def create_new_coin():
    if not game_over:
        coin = Actor('coin1')
        coin.x = randint(130,490)
        coin.y =  5
        coins.append(coin)


def create_new_enemy():
    if not game_over:
        enemy = Actor('enemy')
        enemy.x = randint(130,490)
        enemy.y = 0
        enemies.append(enemy)


def check_coin_car_collision():
    global score
    for coin in coins:
        if coin.colliderect(car):
            score += 2
            coins.remove(coin)
            create_new_coin()


def check_car_collision():
    global game_over
    for enemy in enemies:
        if enemy.colliderect(car):
            sounds.acceleration.stop()
            sounds.horn.play()
            car.image = 'crashed'
            game_over = True


for i in range(2):
    create_new_coin()

create_new_enemy()
pgzrun.go()
