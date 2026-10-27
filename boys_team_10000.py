from pico2d import *
import random


# Game object class here

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)

    def update(self):
        pass

#초기 로딩하는 시간이 오래 걸리는 이유??
class Boy:
    image   =   None
    def __init__(self):
        self.x, self.y = random.randint(0, 800), 90
        self.frame = random.randint(0, 7)
        #self.image = load_image('run_animation.png') #해당 줄 문제
        #객체의 멤버변수는 객체마닫 따로 만들어진다, 따라서 1000번의 로딩이 반복

        if Boy.image    ==  None:
            Boy.image   =   load_image('run_animation.png')
            #단 한번의 이미지 로딩만 수행, 이미지 리소스를 모든 객체가 공유

        
    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += 5

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)


def handle_events():
    global running
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def reset_world():
    global world

    world = []

    grass = Grass()
    world.append(grass)

    team = [Boy() for i in range(10000)]
    world += team


def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


running = True

open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    #delay(0.05)
# finalization code
close_canvas()
