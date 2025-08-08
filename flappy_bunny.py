import curses
import time
import random

BUNNY_CHAR = 'B'
CARROT_CHAR = '|'
GRAVITY = 0.5
JUMP_VELOCITY = -5
OBSTACLE_SPACING = 30
GAP_HEIGHT = 6

class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.height, self.width = stdscr.getmaxyx()
        self.bunny_y = self.height // 2
        self.bunny_x = 5
        self.velocity = 0
        self.obstacles = []
        self.tick = 0
        self.score = 0
        stdscr.nodelay(True)
        stdscr.timeout(50)

    def create_obstacle(self):
        gap_y = random.randint(3, self.height - GAP_HEIGHT - 3)
        self.obstacles.append({'x': self.width - 1, 'gap_y': gap_y})

    def update_obstacles(self):
        for obs in list(self.obstacles):
            obs['x'] -= 1
            if obs['x'] < 0:
                self.obstacles.remove(obs)
                self.score += 1

    def draw_obstacles(self):
        for obs in self.obstacles:
            for y in range(self.height):
                if not (obs['gap_y'] <= y < obs['gap_y'] + GAP_HEIGHT):
                    self.stdscr.addch(y, obs['x'], CARROT_CHAR)

    def check_collision(self):
        if self.bunny_y <= 0 or self.bunny_y >= self.height - 1:
            return True
        for obs in self.obstacles:
            if obs['x'] == self.bunny_x:
                if not (obs['gap_y'] <= self.bunny_y < obs['gap_y'] + GAP_HEIGHT):
                    return True
        return False

    def draw(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, f'Score: {self.score}')
        self.stdscr.addch(self.bunny_y, self.bunny_x, BUNNY_CHAR)
        self.draw_obstacles()
        self.stdscr.refresh()

    def step(self, key):
        if key == ord(' ') or key == curses.KEY_UP:
            self.velocity = JUMP_VELOCITY
        self.velocity += GRAVITY
        self.bunny_y += int(self.velocity)
        if self.tick % OBSTACLE_SPACING == 0:
            self.create_obstacle()
        self.update_obstacles()
        self.draw()
        self.tick += 1
        return self.check_collision()

    def run(self):
        while True:
            key = self.stdscr.getch()
            if key == ord('q'):
                break
            if self.step(key):
                break
        self.stdscr.nodelay(False)
        self.draw()
        self.stdscr.addstr(self.height // 2, self.width // 2 - 5, 'Game Over')
        self.stdscr.refresh()
        time.sleep(2)
        return self.score

def main(stdscr):
    game = Game(stdscr)
    return game.run()

if __name__ == '__main__':
    final_score = curses.wrapper(main)
    print(f'Final Score: {final_score}')
