import pygame
import sys
import traceback
from pygame.locals import *
import my_plane
import enemy
import bullet
import supply
import random

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战，是兄弟就来打我")
# 背景图案显示
background = pygame.image.load("./images/background.png").convert()

# 背景音乐配置
pygame.mixer.music.load("./sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("./sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("./sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("./sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("./sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("./sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("./sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("./sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("./sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.1)
enemy2_down_sound = pygame.mixer.Sound("./sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("./sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("./sound/me_down.wav")
me_down_sound.set_volume(0.2)


# 添加飞机方法
def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.Small_enemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.Mid_enemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def add_big_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.Big_enemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def enemy_speed_up(enemies, value):
    for each in enemies:
        each.speed += value


black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)


def main():
    pygame.mixer.music.play(-1)  # -1表示循环播放

    # 生成玩家飞机
    me = my_plane.MyPlane(bg_size)

    # 生成子弹
    bullets = []
    nor_bullets = []
    nor_bullet_index = 0
    nor_bullet_num = 6
    for i in range(nor_bullet_num):
        nor_bullets.append(bullet.Nor_bullet(me.rect.midtop))

    # 生成超级子弹
    sup_bullets = []
    sup_bullet_index = 0
    sup_bullet_num = 12
    for i in range(sup_bullet_num//2):
        sup_bullets.append(bullet.Sup_bullet((me.rect.centerx-33, me.rect.centery)))
        sup_bullets.append(bullet.Sup_bullet((me.rect.centerx+30, me.rect.centery)))
    # 累计得分
    score = 0
    score_font = pygame.font.Font("./font/font.ttf", 36)

    # 生成敌方飞机
    enemies = pygame.sprite.Group()

    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)

    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 2)

    # 切换飞机图片的变量
    switch_plane = True

    # 用于延时变量，使飞机突突突
    tim_delay = 5

    # 表示是否暂停游戏的按钮
    pause = False
    paused_not_image = pygame.image.load("./images/pause_nor.png").convert_alpha()
    paused_pressed_image = pygame.image.load("./images/pause_pressed.png").convert_alpha()
    resume_not_image = pygame.image.load("./images/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("./images/resume_pressed.png").convert_alpha()
    pause_rect = paused_not_image.get_rect()
    pause_rect.left, pause_rect.top = width - pause_rect.width - 10, 10
    paused_image = paused_not_image

    running = True

    # 用于阻止重复打开记录文件
    recording = True

    # 设置难度级别
    leave = 1

    # 击落图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    # 解除玩家飞机复活无敌定时器
    invincible_tim = USEREVENT + 2

    # 游戏结束画面
    gameover_font = pygame.font.Font("./font/font.TTF", 48)
    again_image = pygame.image.load("./images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("./images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()

    # 炸弹补给
    boom_image = pygame.image.load("./images/bomb.png").convert_alpha()
    boom_rect = boom_image.get_rect()
    boom_font = pygame.font.Font("./font/font.ttf", 48)
    boom_num = 3

    # 超级子弹定时器
    super_bullet_tim = USEREVENT + 1
    super_bullet_choice = False

    # 玩家生命数量
    life_image = pygame.image.load("./images/life.png")
    life_rect = life_image.get_rect()
    life_num = 3
    # 每30秒发放一个补给包
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Boom_Supply(bg_size)
    supply_tim = USEREVENT
    pygame.time.set_timer(supply_tim, 30*1000)

    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

                # 按下暂停键
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and pause_rect.collidepoint(event.pos):
                    pause = not pause
                    if pause:
                        pygame.time.set_timer(supply_tim, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(supply_tim, 30*1000)
                        pygame.mixer.music.play(-1)
                        pygame.mixer.unpause()

            elif event.type == MOUSEMOTION:
                if pause_rect.collidepoint(event.pos):
                    if pause:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = paused_pressed_image
                else:
                    if pause:
                        paused_image = resume_not_image
                    else:
                        paused_image = paused_not_image

                # 按下空格键，全屏轰炸
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if boom_num:
                        if not pause:
                            boom_num -= 1
                            bomb_sound.play()
                            for each in enemies:
                                if each.rect.bottom > 0:
                                    each.active = False

            elif event.type == supply_tim:
                supply_sound.play()
                if random.choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
 
            elif event.type == super_bullet_tim:
                super_bullet_choice = False
                pygame.time.set_timer(super_bullet_tim, 0)

            elif event.type == invincible_tim:
                me.Invincible = False
                pygame.time.set_timer(invincible_tim, 0)
        # 绘制背景图片
        screen.blit(background, (0, 0))

        # 根据玩家的分增加难度
        if leave == 1 and score > 90000:
            leave = 2
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            enemy_speed_up(small_enemies, 1)

        elif leave == 2 and score > 300000:
            leave = 3
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            enemy_speed_up(mid_enemies, 1)

        elif leave == 3 and score > 700000:
            leave = 4
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 2)
            enemy_speed_up(small_enemies, 1)
            enemy_speed_up(mid_enemies, 2)

        elif leave == 4 and score > 1200000:
            leave = 5
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 2)
            enemy_speed_up(small_enemies, 1)
            enemy_speed_up(big_enemies, 1)

        if not pause and life_num:
            # 检测玩家的键盘操作
            key_pressed = pygame.key.get_pressed()
            # 玩家飞机移动
            if key_pressed[K_w]:
                me.moveUp()
            if key_pressed[K_s]:
                me.moveDn()
            if key_pressed[K_a]:
                me.moveLf()
            if key_pressed[K_d]:
                me.moveRt()

            # 检测补给数目与是否能获得
            if bomb_supply.active is True:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    if boom_num < 3:
                        get_bomb_sound.play()
                        boom_num += 1
                        bomb_supply.active = False

            # 检测补给数目与是否能获得
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    super_bullet_choice = True
                    get_bullet_sound.play()
                    bullet_supply.active = False
                    pygame.time.set_timer(super_bullet_tim, 18*1000)

            # 类似定时器
            tim_delay -= 1
            if not tim_delay:
                tim_delay = 100

            if tim_delay % 5 == 0:
                switch_plane = not switch_plane

            # 10帧发射一次子弹
            if not (tim_delay % 9):
                bullet_sound.play()
                if super_bullet_choice:
                    bullets = sup_bullets
                    bullets[sup_bullet_index].reset((me.rect.centerx-33, me.rect.centery))
                    bullets[sup_bullet_index+1].reset((me.rect.centerx+30, me.rect.centery))
                    sup_bullet_index = (sup_bullet_index + 2) % 12
                else:
                    bullets = nor_bullets
                    bullets[nor_bullet_index].reset(me.rect.midtop)
                    nor_bullet_index = (nor_bullet_index + 1) % 4

            # 检测子弹击中敌机
            for each in bullets:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                    hit = pygame.sprite.spritecollide(each, enemies, False, pygame.sprite.collide_mask)
                    if hit:
                        each.active = False
                        for e in hit:
                            if e in big_enemies or e in mid_enemies:
                                e.energy = e.energy - 1
                                e.hit = True
                                if e.energy <= 0:
                                    e.active = False
                            else:
                                e.active = False

            # 检测飞机碰撞
            crashed = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if crashed:
                if me.Invincible is False:
                    me.active = False
                for e in crashed:
                    e.active = False

            # 绘制玩家飞机
            if me.active is True:
                if switch_plane:
                    screen.blit(me.image, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                if not (tim_delay % 3):
                    if me_destroy_index == 1:
                        me_down_sound.play()
                    screen.blit(me.destroy_image[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(invincible_tim, 3*1000)

            # 绘制地方飞机
            for each in big_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_plane:
                            screen.blit(each.image, each.rect)
                        else:
                            screen.blit(each.image_2, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, black,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5),
                                     2)
                    energy_part = each.energy / enemy.Big_enemy.energy
                    if energy_part > 0.2:
                        energy_color = green
                    else:
                        energy_color = red
                    pygame.draw.line(screen, energy_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left+energy_part*each.rect.width, each.rect.top - 5),
                                     2)
                    if each.rect.bottom == -50:
                        enemy3_fly_sound.play(-1)
                else:
                    # 敌机毁灭
                    if not (tim_delay % 3):
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            each.reset()
                            enemy3_fly_sound.stop()
                            enemy3_down_sound.play()
                            score += 10000

            # 显示得分
            score_text = score_font.render("Score : %s" % str(score), True, white)
            screen.blit(score_text, (10, 5))

            for each in mid_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)
                    # 绘制血槽
                    pygame.draw.line(screen, black,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5),
                                     2)
                    energy_part = each.energy / enemy.Mid_enemy.energy
                    if energy_part > 0.2:
                        energy_color = green
                    else:
                        energy_color = red
                    pygame.draw.line(screen, energy_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left+energy_part*each.rect.width, each.rect.top - 5),
                                     2)
                else:
                    # 敌机毁灭
                    if not (tim_delay % 3):
                        if e2_destroy_index == 1:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            each.reset()
                            score += 6000

            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    # 敌机毁灭
                    if not (tim_delay % 3):
                        if e1_destroy_index == 1:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            each.reset()
                            score += 1000

        elif life_num == 0:
            # 背景音乐停止, 音效，停止发放补给
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            pygame.time.set_timer(supply_tim, 0)
            if recording:
                # 读取历史最高得分
                recording = False
                with open("./record.txt", "r") as f:
                    record_score = int(f.read())
                if score > record_score:
                    record_score = score
                    with open("./record.txt", "w") as f:
                        f.write(str(score))

            # 绘制结束画面
            record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255))
            screen.blit(record_score_text, (50, 50))

            gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                (width - gameover_text2_rect.width) // 2, \
                gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                (width - again_rect.width) // 2, \
                gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                (width - again_rect.width) // 2, \
                again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                # 如果用户点击“重新开始”
                if again_rect.left < pos[0] < again_rect.right and \
                        again_rect.top < pos[1] < again_rect.bottom:
                    # 调用main函数，重新开始游戏
                    main()
                # 如果用户点击“结束游戏”
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                        gameover_rect.top < pos[1] < gameover_rect.bottom:
                    # 退出游戏
                    pygame.quit()
                    sys.exit()

                    # 绘制剩余生命数量
        if life_num:
            for i in range(life_num):
                screen.blit(life_image,
                            (width - 10 - (i+1)*life_rect.width,
                             height - 10 - life_rect.height))

        # 绘制剩余炸弹补给
        boom_text = boom_font.render("x %d" % boom_num, True, white)
        text_rect = boom_text.get_rect()
        screen.blit(boom_image, (10, height - 10 - boom_rect.height), boom_rect)
        screen.blit(boom_text, (20 + boom_rect.width, height - 5 - text_rect.height))

        screen.blit(paused_image, pause_rect)
        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
