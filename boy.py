import math
import time

from pico2d import load_image
from transitions import Machine
from auto_run import AutoRun


class Boy:
    states = ['IDLE', 'SLEEP', 'RUN', 'AUTO_RUN']
    transitions = [
        {'trigger': 'start_run', 'source': ['IDLE', 'SLEEP'], 'dest': 'RUN'},
        {'trigger': 'stop_run', 'source': 'RUN', 'dest': 'IDLE'},
        {'trigger': 'wake_up', 'source': 'SLEEP', 'dest': 'IDLE'},
        {'trigger': 'fall_asleep', 'source': 'IDLE', 'dest': 'SLEEP'},
        {'trigger': 'start_auto_run', 'source': 'IDLE', 'dest': 'AUTO_RUN'},
        {'trigger': 'cancel_auto_run', 'source': 'AUTO_RUN', 'dest': 'RUN'},
        {'trigger': 'finish_auto_run', 'source': 'AUTO_RUN', 'dest': 'IDLE'},
    ]

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.direction = 1
        self.speed = 5
        self.base_speed = self.speed
        self.scale = 1.0
        self.auto_run = AutoRun()
        self.image = load_image('animation_sheet.png')
        self.idle_started_at = time.monotonic()
        self.state_started_at = self.idle_started_at
        self.machine = Machine(
            model=self,
            states=Boy.states,
            transitions=Boy.transitions,
            initial='IDLE',
            auto_transitions=False,
            after_state_change='reset_state_timer',
        )

    def reset_state_timer(self):
        self.state_started_at = time.monotonic()
        if self.state != 'AUTO_RUN':
            self.speed = self.base_speed
            self.scale = 1.0
        if self.state == 'IDLE':
            # IDLE에 돌아올 때마다 5초 대기 시간을 새로 잰다.
            self.idle_started_at = self.state_started_at

    def start_running(self):
        if self.state == 'AUTO_RUN':
            self.cancel_auto_run()
            return
        if self.state in ('IDLE', 'SLEEP'):
            self.start_run()

    def start_auto_running(self):
        if self.state == 'IDLE':
            self.start_auto_run()

    def stop_running(self):
        if self.state == 'RUN':
            self.stop_run()

    def set_direction(self, direction):
        self.direction = direction

    def update(self):
        if self.state == 'IDLE':
            if time.monotonic() - self.idle_started_at >= 5.0:
                self.fall_asleep()
                return
            self.frame = (self.frame + 1) % 8
        elif self.state == 'RUN':
            # 캐릭터 중심이 화면 안쪽에 있도록 경계에서 이동을 제한한다.
            self.x = max(50, min(750, self.x + self.direction * self.speed))
            self.frame = (self.frame + 1) % 8
        elif self.state == 'AUTO_RUN':
            self.auto_run.update(self)
            self.frame = (self.frame + 1) % 8

    def draw(self):
        if self.state == 'IDLE':
            idle_row = 300 if self.direction > 0 else 200
            self.image.clip_draw(self.frame * 100, idle_row, 100, 100, self.x, self.y)
        elif self.state == 'RUN':
            run_row = 100 if self.direction > 0 else 0
            self.image.clip_draw(self.frame * 100, run_row, 100, 100, self.x, self.y)
        elif self.state == 'SLEEP':
            # 마지막으로 달린 방향을 향해 원본 프레임을 회전시켜 쓰러지게 한다.
            sleep_elapsed = time.monotonic() - self.state_started_at
            fall_progress = min(sleep_elapsed / 0.45, 1.0)
            breathing = math.sin(sleep_elapsed * 2 * math.pi) * 0.025
            angle = -self.direction * math.pi / 2 * fall_progress + breathing
            sleep_y = self.y - 22 * fall_progress
            sleep_row = 300 if self.direction > 0 else 200
            self.image.clip_composite_draw(
                self.frame * 100, sleep_row, 100, 100,
                angle, '',
                self.x, sleep_y, 100, 100,
            )
        elif self.state == 'AUTO_RUN':
            run_row = 100 if self.direction > 0 else 0
            size = 100 * self.scale
            self.image.clip_draw(self.frame * 100, run_row, 100, 100,
                                 self.x, self.y, size, size)
