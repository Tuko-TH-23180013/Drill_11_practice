import time


class AutoRun:
    """AUTO_RUN 상태의 시간 제한, 가속, 크기 증가, 경계 반전을 담당한다."""

    duration = 5.0

    def update(self, boy):
        elapsed = time.monotonic() - boy.state_started_at
        if elapsed >= self.duration:
            boy.finish_auto_run()
            return

        # 5초 동안 속도는 최대 3배, 크기는 최대 1.5배까지 커진다.
        progress = elapsed / self.duration
        boy.speed = boy.base_speed * (1.0 + 2.0 * progress)
        boy.scale = 1.0 + 0.5 * progress

        half_width = 50 * boy.scale
        left_edge, right_edge = half_width, 800 - half_width
        next_x = boy.x + boy.direction * boy.speed
        if next_x >= right_edge:
            boy.x = right_edge
            boy.direction = -1
        elif next_x <= left_edge:
            boy.x = left_edge
            boy.direction = 1
        else:
            boy.x = next_x
