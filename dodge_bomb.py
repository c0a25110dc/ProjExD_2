import os
import sys
import random
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {#移動量
         pg.K_UP: (0, -5), pg.K_w: (0, -5),
         pg.K_DOWN: (0, +5), pg.K_s: (0, +5),
         pg.K_LEFT: (-5, 0), pg.K_a: (-5, 0),
         pg.K_RIGHT: (+5, 0), pg.K_d: (+5, 0)
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rect: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたrectが画面内or画面外を判定する関数
    引数：こうかとんrect, 爆弾rect
    戻り値：横方向、縦方向の判定結果（画面内：True ,画面外：False）
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:
        tate = False
    return yoko, tate

def game_over(screen: pg.Surface) -> None:
    """
    GameOver画面の作成
    """
    back_img = pg.Surface((WIDTH, HEIGHT))
    back_img.set_alpha(200)
    back_img.fill((0, 0, 0))
    
    font = pg.font.Font(None, 100)
    txt = font.render("Game Over ", True, (255, 255, 255))
    txt_rect = txt.get_rect(center=(WIDTH//2, HEIGHT//2))

    kk_img = pg.image.load("fig/8.png")
    kk_rect_r = kk_img.get_rect(center=(WIDTH//2 + 250, HEIGHT//2))
    kk_rect_l = kk_img.get_rect(center=(WIDTH//2 - 250, HEIGHT//2))

    back_img.blit(txt, txt_rect)
    back_img.blit(kk_img, kk_rect_r)
    back_img.blit(kk_img, kk_rect_l)

    screen.blit(back_img, [0, 0])
    pg.display.update()

    time.sleep(5)#修正#1
   
   

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    #移動方向に回転・反転
    kk_img0 = pg.image.load("fig/3.png")
    kk_img_flip = pg.transform.flip(kk_img0, True, False)
    
    kk_dict = {
        (0, 0):   pg.transform.rotozoom(kk_img0, 0, 0.9),    # 静止
        (-5, 0):  pg.transform.rotozoom(kk_img0, 0, 0.9),    # 左
        (-5, -5): pg.transform.rotozoom(kk_img0, -45, 0.9),  # 左上
        (0, -5):  pg.transform.rotozoom(kk_img0, 270, 0.9),  # 上
        (+5, -5): pg.transform.rotozoom(kk_img_flip, 45, 0.9),# 右上
        (+5, 0):  pg.transform.rotozoom(kk_img_flip, 0, 0.9), # 右
        (+5, +5): pg.transform.rotozoom(kk_img_flip, -45, 0.9),# 右下
        (0, +5):  pg.transform.rotozoom(kk_img0, 90, 0.9),   # 下
        (-5, +5): pg.transform.rotozoom(kk_img0, 45, 0.9),   # 左下
    }
    return kk_dict

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    bb_img.set_colorkey((0, 0, 0))
    vx, vy = +5, +5

    #演習3
    kk_imgs = get_kk_imgs()
    kk_img = kk_imgs[(0, 0)]
    kk_rct = kk_img.get_rect(center=kk_rct.center)
    kk_rct.center = 300, 200

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
    #演習1 
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            return
                   
        if kk_rct.colliderect(bb_rct):
            return
        
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]: 
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_img = kk_imgs[tuple(sum_mv)] #演習3
        kk_rct.move_ip(sum_mv)

        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate: 
            vy *= -1

        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
