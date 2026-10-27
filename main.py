from pico2d import *
from boy import Boy
from grass import Grass

# Game object class here



def handle_events():
    global running, held_directions

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if boy.state == 'SLEEP':
                boy.wake_up()
        elif event.type == SDL_KEYDOWN and event.key in (SDLK_LEFT, SDLK_RIGHT):
            if event.key not in held_directions:
                held_directions.append(event.key)
            boy.set_direction(1 if held_directions[-1] == SDLK_RIGHT else -1)
            boy.start_running()
        elif event.type == SDL_KEYUP and event.key in (SDLK_LEFT, SDLK_RIGHT):
            if event.key in held_directions:
                held_directions.remove(event.key)
            if held_directions:
                boy.set_direction(1 if held_directions[-1] == SDLK_RIGHT else -1)
                boy.start_running()
            else:
                boy.stop_running()


def reset_world():
    global world
    global boy

    world = []

    grass = Grass()
    world.append(grass)

    boy = Boy()
    world.append(boy)



def update_world():
    # 각 객체가 현재 상태에 맞춰 애니메이션과 동작을 갱신한다.
    for o in world:
        o.update()


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


running = True
held_directions = []

open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
