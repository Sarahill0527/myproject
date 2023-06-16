# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 21:22:32 2023

@author: QXzym
"""

# 1 引入需要的模块
import pygame    # 导入 pygame 模块
import random    # 导入 random 模块


# 1 配置图片地址
IMAGE_PATH = 'D:\zhuomianyingyong\Desktop\python期末\imgs'
# 1 设置页面宽高
scrrr_width = 880
scrrr_height = 700
# 1 创建控制游戏结束的状态
GAMEOVER = False
# 4 图片加载报错处理
LOG = '文件:{}中的方法:{}出错'.format(__file__, __name__)
#__file__ 是用于获取当前脚本文件的文件名，__name__ 是用于获取当前脚本文件的模块名


# 3 创建地图类
class Map():
    # 3 存储两张不同颜色的图片名称
    map_names_list = [IMAGE_PATH + '//green.jpg', IMAGE_PATH + '//green1.jpg']
    # 3 初始化地图
    def __init__(self, x, y, img_index): #参数表示地图的位置和图片编号 
        #首先根据 img_index 选取对应的图片路径，然后使用 pygame.image.load() 方法加载该图片，最后将位置信息等存储到地图对象的属性中。
        self.image = pygame.image.load(Map.map_names_list[img_index])
        self.position = (x, y)    
        # 是否能够种植
        self.can_grow = True
    # 3 加载地图
    def load_map(self):
        MainGame.window.blit(self.image, self.position)
    #通过blit() 方法将地图图片绘制在游戏窗口上，并根据存储的位置信息确定图片的显示位置。
    

# 4 植物类
class Plant(pygame.sprite.Sprite):
    #在Pygame中使用精灵(Sprite)类实现游戏对象，因它能够方便地实现碰撞检测、图形渲染等功能
    def __init__(self):
        super(Plant, self).__init__()
        #并将live属性设置为True，表示植物存在。
        self.live = True
    # 加载图片
    def load_image(self):
        if hasattr(self, 'image') and hasattr(self, 'rect'):  #self.rect 属性是一个用于定位植物位置的Rect对象
            MainGame.window.blit(self.image, self.rect)
           # 如果该植物对象已经存在 image 和 rect 属性，则将其渲染到主窗口中。
        else:
            print(LOG)
           # 否则，输出一条提示信息。

# 5 向日葵类
class Sunflower(Plant): #Sunflower类继承Plant的类
    def __init__(self, x, y):
        super(Sunflower, self).__init__()
        self.image = pygame.image.load('imgs/sunflower.jpg')
        self.rect = self.image.get_rect() #获取其矩形区域，并设置其位置
        self.rect.x = x
        self.rect.y = y
        self.price = 50
        self.hp = 100  #价格和生命值也被赋值为 50 和 100
        # 5 时间计数器（初始化为 0）
        self.time_count = 0
    # 5 新增功能：生成阳光
    def produce_money(self):
        self.time_count += 1
        if self.time_count == 25:
            MainGame.money += 5  #每隔 25 次循环，就会让玩家获得 5 个阳光（类似于货币），而这个阳光是存在一个名为 MainGame 的类中的一个静态变量 money 中的
            self.time_count = 0  #再次初始化
    # 5 向日葵加入到主窗口中
    def display_sunflower(self):
        MainGame.window.blit(self.image, self.rect)


# 6 豌豆射手类
class PeaShooter(Plant): #继承Plant 类
    def __init__(self, x, y):
        #__init__ 方法是该类的构造函数，在初始化一个豌豆射手对象时会被调用
        super(PeaShooter, self).__init__() 
        # self.image 为一个 surface
        self.image = pygame.image.load('imgs/peashooter.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 50
        self.hp = 200 #价格和生命值也被赋值为 50 和 200
        # 6 发射计数器
        self.shot_count = 0
    # 6 增加射击方法
    def shot(self):
        #先判断当前是否有僵尸在豌豆射手的攻击范围内，如果有则判断是否要进行射击并触发子弹的生成。
        # 6 记录是否应该射击
        should_fire = False
        for zombie in MainGame.zombie_list: #zombie僵尸类
            if zombie.rect.y == self.rect.y and zombie.rect.x < 880 and zombie.rect.x > self.rect.x:
                should_fire = True
        # 6 如果活着
        if self.live and should_fire:
            self.shot_count += 1
            # 6 计数器到10发射一次
            if self.shot_count == 10:
                # 6 基于当前豌豆射手的位置，创建子弹
                peabullet = PeaBullet(self)
                # 6 将子弹存储到子弹列表中
                MainGame.peabullet_list.append(peabullet) #peabullet子弹类
                self.shot_count = 0
    # 6 将豌豆射手加入到窗口中的方法
    def display_peashooter(self):
        MainGame.window.blit(self.image, self.rect)


# 7 豌豆子弹类
class PeaBullet(pygame.sprite.Sprite): #继承自 Pygame 的 Sprite 类
    def __init__(self, peashooter):
        self.live = True
        self.image = pygame.image.load('imgs/peabullet.jpg')
        self.damage = 50
        self.speed = 10
        self.rect = self.image.get_rect()
        self.rect.x = peashooter.rect.x + 60
        self.rect.y = peashooter.rect.y + 15
    def move_bullet(self):
        # 7 在屏幕范围内，沿着 x 轴实现往右移动子弹
        if self.rect.x < scrrr_width:
            self.rect.x += self.speed
        else:
            self.live = False
    # 7 新增，子弹与僵尸的碰撞
    def hit_zombie(self):
        for zombie in MainGame.zombie_list:
            if pygame.sprite.collide_rect(self, zombie):
                # 打中僵尸之后，修改子弹的状态，
                self.live = False
                # 僵尸掉血
                zombie.hp -= self.damage
                if zombie.hp <= 0:
                    #没血则死
                    zombie.live = False
                    self.nextLevel()
    # 7闯关方法
    def nextLevel(self): 
        MainGame.score += 20 #score会增加20分
        MainGame.remnant_score -= 20 #减少20分
        for i in range(1, 100): #1到99之间
            #当当前得分扩大100倍满足i值，并且剩余得分为0时，才满足升级的条件
            if MainGame.score == 100 * i and MainGame.remnant_score == 0:
                #将remnant_score设置为当前得分的100倍
                MainGame.remnant_score = 100 * i
                #升级时对状态属性shaoguan进行+1的操作，produce_zombie进行+50的操作。
                MainGame.shaoguan += 1
                MainGame.produce_zombie += 50
    #将子弹的图像渲染到主窗口上
    def display_peabullet(self):
        MainGame.window.blit(self.image, self.rect)


# 9 僵尸类
class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Zombie, self).__init__()
        self.image = pygame.image.load('imgs/zombie.jpg')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y  
        self.hp = 1000  #生命值
        self.damage = 2 #攻击伤害
        self.speed = 1  #速度
        self.live = True #是否存活
        self.stop = False #是否停止移动
    # 9 僵尸的移动
    def move_zombie(self):
        #检测该对象是否“活着”（live），并且没有被“停止”（stop）
        if self.live and not self.stop:
            #把该对象沿着X轴负方向移动（即向左），移动的距离等于该对象的移动速度
            self.rect.x -= self.speed
            if self.rect.x < -80:
                # 8 调用游戏结束方法
                MainGame().gameOver()
    # 9 判断僵尸是否碰撞到植物，如果碰撞，调用攻击植物的方法
    def hit_plant(self):
        for plant in MainGame.plants_list:
            #利用collide_rect()函数检测该僵尸对象与MainGame.plants_list列表中的各个植物对象是否碰撞。
            if pygame.sprite.collide_rect(self, plant):
                # 8  僵尸移动状态的修改
                #发生碰撞，表示它已经停止并开始吃植物
                self.stop = True
                self.eat_plant(plant)
    # 9 僵尸攻击植物
    def eat_plant(self, plant):
        # 9 植物生命值减少
        plant.hp -= self.damage
        # 9 植物死亡后的状态修改，以及地图状态的修改
        if plant.hp <= 0:
            a = plant.rect.y // 80 - 1
            b = plant.rect.x // 80
            #计算出被吃掉植物下方的地图块位置，并将其状态修改为可种植
            map = MainGame.map_list[a][b] 
            map.can_grow = True
            plant.live = False
            # 8 修改僵尸的移动状态
            self.stop = False #僵尸继续移动
    # 9 将僵尸加载到地图中
    def display_zombie(self):
        MainGame.window.blit(self.image, self.rect)


# 1 主程序
class MainGame():
    i = 0
    for i in range(3):
    #提示输入用户名和密码
       username = input('用户名：')
       password = input('密码：')
    #判断输入的是否正确 boke 1234
       if username == 'jack' and password =='123':
          print('用户登录成功!')
          break
       else:
          print('用户名或密码有误！\n')
          i = i + 1
    if i == 2:
       print('错误次数超过3次，即将退出系统！')


    # 2 创建关数，得分，剩余分数，钱数
    shaoguan = 1
    score = 0
    remnant_score = 100
    money = 200
    # 3 存储所有地图坐标点
    map_points_list = []
    # 3 存储所有的地图块
    map_list = []
    # 4 存储所有植物的列表
    plants_list = []
    # 7 存储所有豌豆子弹的列表
    peabullet_list = []
    # 9 新增存储所有僵尸的列表
    zombie_list = []
    count_zombie = 0
    produce_zombie = 100

    # 1 加载游戏窗口
    def init_window(self):
        # 1 调用显示模块的初始化
        pygame.display.init()
        # 1 创建窗口
        MainGame.window = pygame.display.set_mode([scrrr_width, scrrr_height])

    # 2 文本绘制
    def draw_text(self, content, size, color):
        pygame.font.init() #用于初始化pygame.font模块，以确保字体可用。
        font = pygame.font.SysFont('kaiti', size)
        text = font.render(content, True, color)
        return text #将渲染后的文本图像返回，以便在游戏窗口中显示。

    # 2 加载帮助提示
    def load_help_text(self):
        #调用draw_text 方法，生成一个文本图像。
        text1 = self.draw_text('1.按左键创建向日葵 2.按右键创建豌豆射手', 26, (0, 0, 0))
        MainGame.window.blit(text1, (5, 5))#文本图像被绘制在窗口左上角位置，坐标为（5，5）

    # 3 初始化坐标点
    def init_plant_points(self):
        #在y轴方向上循环6次（即从第 1 行到第 6 行），在每一行中遍历10个点（即从第 1 列到第 10 列）
        for y in range(1, 7):
            points = []
            for x in range(10):
                point = (x, y)
                points.append(point)
            MainGame.map_points_list.append(points) #二维列表，其中第一维表示行，第二维表示列
            print("MainGame.map_points_list", MainGame.map_points_list)

    # 3 初始化地图
    def init_map(self):
        for points in MainGame.map_points_list:
            temp_map_list = list() #临时列表
            for point in points:
                # map = None
                #如果坐标点的行列之和为偶数，则将生成的地图块的类型设为 0，否则设为 1。
                if (point[0] + point[1]) % 2 == 0:
                    map = Map(point[0] * 80, point[1] * 80, 0)
                else:
                    map = Map(point[0] * 80, point[1] * 80, 1)
                # 将地图块加入到窗口中
                temp_map_list.append(map)
                print("temp_map_list", temp_map_list)
            MainGame.map_list.append(temp_map_list) #添加临时列表
        print("MainGame.map_list", MainGame.map_list)

    # 3 将地图加载到窗口中
    def load_map(self):
        #遍历 MainGame.map_list 列表中的每个临时列表
        for temp_map_list in MainGame.map_list:
            #遍历其中的每个地图块实例
            for map in temp_map_list:
                map.load_map()

    # 6 增加豌豆射手发射处理
    def load_plants(self):
        for plant in MainGame.plants_list:
            # 6 优化加载植物的处理逻辑
            if plant.live:
                #子弹的生命值大于零（即子弹存活）
                if isinstance(plant, Sunflower):#向日葵类型，则展示该植物的图片并生产阳光。
                    plant.display_sunflower()
                    plant.produce_money()
                elif isinstance(plant, PeaShooter): #豌豆射手类型，则展示该植物的图片并进行射击。
                    plant.display_peashooter()
                    plant.shot()
            else:
                #生命值小于等于零，则删除该植物
                MainGame.plants_list.remove(plant)

    # 7 加载所有子弹的方法
    def load_peabullets(self):
        for b in MainGame.peabullet_list:
            if b.live:
                b.display_peabullet()
                b.move_bullet()
                #  调用子弹是否打中僵尸的方法
                b.hit_zombie()
            else:
                MainGame.peabullet_list.remove(b)

    # 8事件处理
    def deal_events(self):
        # 8 获取所有事件
        eventList = pygame.event.get()
        # 8 遍历事件列表，判断
        for e in eventList:
            #游戏被关闭，需要调用self.gameOver()方法来结束游戏
            if e.type == pygame.QUIT:
                self.gameOver()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                # print('按下鼠标按键')
                print(e.pos)
                # print(e.button)#左键1  按下滚轮2 上转滚轮为4 下转滚轮为5  右键 3

                x = e.pos[0] // 80
                y = e.pos[1] // 80
                print(x, y)
                map = MainGame.map_list[y - 1][x]
                print(map.position)
                # 8 增加创建时候的地图装填判断以及金钱判断
                if e.button == 1:
                    if map.can_grow and MainGame.money >= 50: #判断种植植物以及当前金币
                        sunflower = Sunflower(map.position[0], map.position[1])
                        MainGame.plants_list.append(sunflower)
                        print('当前植物列表长度:{}'.format(len(MainGame.plants_list)))
                        map.can_grow = False
                        MainGame.money -= 50 #表示该位置已经有植物了，不能再种植了，并且减少了金币数量。
                elif e.button == 3:
                    if map.can_grow and MainGame.money >= 50:
                        peashooter = PeaShooter(
                            map.position[0], map.position[1])
                        MainGame.plants_list.append(peashooter)
                        print('当前植物列表长度:{}'.format(len(MainGame.plants_list)))
                        map.can_grow = False
                        MainGame.money -= 50

    # 9 新增初始化僵尸的方法
    def init_zombies(self):
        #生成6个僵尸对象，并将它们的位置随机分布在右侧1000个像素中
        for i in range(1, 7):
            dis = random.randint(1, 5) * 200 #随机生成200到1000之间的整数，以避免僵尸们位置太靠近
            zombie = Zombie(800 + dis, i * 80)#创建每个僵尸对象，并将它们添加到MainGame.zombie_list列表中。
            MainGame.zombie_list.append(zombie) #zombie_list是一个静态变量

    # 9将所有僵尸加载到地图中
    def load_zombies(self):
        for zombie in MainGame.zombie_list: #循环遍历在其中的每个僵尸对象
            if zombie.live: #活着则调用以下方法
                zombie.display_zombie()#负责将僵尸对象渲染到屏幕上
                zombie.move_zombie()#负责在屏幕上向左移动僵尸对象
                # v2.0 调用是否碰撞到植物的方法
                zombie.hit_plant()
            else:
                MainGame.zombie_list.remove(zombie)

    # 1 开始游戏
    def start_game(self):
        # 1 初始化窗口
        self.init_window()
        # 3 初始化坐标和地图
        self.init_plant_points()
        self.init_map()
        # 9 调用初始化僵尸的方法
        self.init_zombies()
        # 1 只要游戏没结束，就一直循环
        while not GAMEOVER:
            # 1 渲染白色背景
            MainGame.window.fill((255, 255, 255))
            # 2 渲染的文字和坐标位置
            MainGame.window.blit(self.draw_text('当前钱数$: {}'.format( MainGame.money), 26, (255, 0, 0)), (500, 40))
            MainGame.window.blit(self.draw_text(
                '当前关数{}，得分{},距离下关还差{}分'.format(
                    MainGame.shaoguan, MainGame.score, MainGame.remnant_score), 26,
                (255, 0, 0)), (5, 40))
            self.load_help_text()

            # 3 需要反复加载地图
            self.load_map()
            # 6 调用加载植物的方法
            self.load_plants()
            # 7  调用加载所有子弹的方法
            self.load_peabullets()
            # 8 调用事件处理的方法
            self.deal_events()
            # 9 调用展示僵尸的方法
            self.load_zombies()
            # 9 计数器增长，每数到100，调用初始化僵尸的方法
            MainGame.count_zombie += 1
            if MainGame.count_zombie == MainGame.produce_zombie:
                self.init_zombies()
                MainGame.count_zombie = 0
            # 9 pygame自己的休眠
            pygame.time.wait(10)
            # 1 实时更新
            pygame.display.update()

    # 10 程序结束方法
    def gameOver(self):
        #draw_text()方法接受三个参数：要显示的文本内容、文本字号和字体颜色。（300，200）表示在游戏窗口中输出文本的位置坐标。
        MainGame.window.blit(self.draw_text('游戏结束', 50, (0, 0, 0)), (300, 200))
        print('游戏结束')
        pygame.time.wait(400) #等待400毫秒
        global GAMEOVER #全局变量
        GAMEOVER = True
#屏幕左上角为坐标原点（0，0），x轴向右递增，y轴向下递增。

# 1 启动主程序
if __name__ == '__main__':
    game = MainGame()
    game.start_game()
