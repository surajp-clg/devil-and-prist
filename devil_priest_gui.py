import sys
try:
    import pygame
except Exception:
    print("pygame is required to run this file. Install with: pip install pygame")
    sys.exit(1)

import character
import boat


class DevilPriestGame:
    def __init__(self, start_n=2):
        self.level = 1
        self.start_n = start_n
        self.n = start_n
        self._setup_game()

        # Pygame setup
        pygame.init()
        self.WIDTH, self.HEIGHT = 900, 500
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Devil vs Priest')
        self.font = pygame.font.SysFont(None, 24)
        self.clock = pygame.time.Clock()

        # layout
        self.left_x = 120
        self.right_x = self.WIDTH - 120
        self.bank_y_start = 80
        self.bank_y_step = 50
        self.boat_y = self.HEIGHT // 2
        self.boat_left_x = self.WIDTH // 2 - 120
        self.boat_right_x = self.WIDTH // 2 + 20

    def _setup_game(self):
        # create characters
        self.devils = [character.devil(i) for i in range(self.n)]
        self.priests = [character.priest(i) for i in range(self.n)]
        self.all_chars = []
        for d in self.devils:
            d.side = 0  # left bank
            d.is_on_boat = False
            self.all_chars.append(d)
        for p in self.priests:
            p.side = 0
            p.is_on_boat = False
            self.all_chars.append(p)

        # boat
        self.boat = boat.Boat()
        self.boat.boat_side = 0

        # UI state
        self.message = 'Click characters to board/unboard. Click the boat to move.'

    def reset_level(self, win=True):
        if win:
            # progression rule: first level 2 -> 3, then increase by 2 afterwards
            if self.level == 1:
                self.n = 3
            else:
                self.n += 2
            self.level += 1
        # clear and re-setup
        self._setup_game()

    def count_bank(self):
        left = {'devil': 0, 'priest': 0}
        right = {'devil': 0, 'priest': 0}
        for c in self.all_chars:
            if c.is_on_boat:
                continue
            if c.side == 0:
                if c.is_devil:
                    left['devil'] += 1
                else:
                    left['priest'] += 1
            else:
                if c.is_devil:
                    right['devil'] += 1
                else:
                    right['priest'] += 1
        return left, right

    def check_loss(self):
        left, right = self.count_bank()
        # lose if devils > priests and priests > 0 on any bank
        if (left['devil'] > left['priest'] and left['priest'] > 0) or (
            right['devil'] > right['priest'] and right['priest'] > 0
        ):
            return True
        return False

    def check_win(self):
        # win when all characters are on right bank (side == 1) regardless of boat
        for c in self.all_chars:
            if c.side != 1:
                return False
        return True

    def char_screen_pos(self, c, index_same_side):
        # place characters on the bank in vertical stacks
        if c.is_on_boat:
            # on boat
            bx = self.boat_left_x if self.boat.boat_side == 0 else self.boat_right_x
            return bx + 30 + (10 if c.is_devil else -10), self.boat_y - 10 + index_same_side * 18
        if c.side == 0:
            x = self.left_x
        else:
            x = self.right_x
        y = self.bank_y_start + index_same_side * self.bank_y_step
        return x, y

    def draw(self):
        self.screen.fill((135, 206, 235))  # sky
        # draw river
        pygame.draw.rect(self.screen, (30, 144, 255), (self.WIDTH // 2 - 160, 0, 320, self.HEIGHT))

        # draw banks
        pygame.draw.rect(self.screen, (34, 139, 34), (0, 0, 160, self.HEIGHT))
        pygame.draw.rect(self.screen, (34, 139, 34), (self.WIDTH - 160, 0, 160, self.HEIGHT))

        # draw boat
        boat_x = self.boat_left_x if self.boat.boat_side == 0 else self.boat_right_x
        boat_rect = pygame.Rect(boat_x, self.boat_y - 20, 120, 40)
        pygame.draw.rect(self.screen, (139, 69, 19), boat_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), boat_rect, 2)
        boat_label = self.font.render('Boat', True, (255, 255, 255))
        self.screen.blit(boat_label, (boat_x + 40, self.boat_y - 10))

        # draw characters
        left_count = 0
        right_count = 0
        boat_count = 0
        char_rects = []
        # sort for stable ordering: priests then devils
        for side in (0, 1):
            same_side = [c for c in self.all_chars if (not c.is_on_boat) and c.side == side]
            # place priests first then devils for grouping
            same_side.sort(key=lambda x: (x.is_devil, x.id))
            for i, c in enumerate(same_side):
                idx = i
                x, y = self.char_screen_pos(c, idx)
                color = (200, 0, 0) if c.is_devil else (255, 255, 255)
                pygame.draw.circle(self.screen, color, (x, y), 16)
                pygame.draw.circle(self.screen, (0, 0, 0), (x, y), 16, 2)
                lbl = self.font.render(('D' if c.is_devil else 'P') + str(c.id), True, (0, 0, 0))
                self.screen.blit(lbl, (x - 10, y - 8))
                char_rects.append((pygame.Rect(x - 16, y - 16, 32, 32), c))

        # characters on boat
        on_boat = [c for c in self.all_chars if c.is_on_boat]
        for i, c in enumerate(on_boat):
            x, y = self.char_screen_pos(c, i)
            color = (200, 0, 0) if c.is_devil else (255, 255, 255)
            pygame.draw.circle(self.screen, color, (int(x), int(y)), 14)
            pygame.draw.circle(self.screen, (0, 0, 0), (int(x), int(y)), 14, 2)
            lbl = self.font.render(('D' if c.is_devil else 'P') + str(c.id), True, (0, 0, 0))
            self.screen.blit(lbl, (int(x) - 8, int(y) - 6))
            char_rects.append((pygame.Rect(int(x) - 14, int(y) - 14, 28, 28), c))

        # HUD
        lvl = self.font.render(f'Level: {self.level}  Count: {self.n}', True, (0, 0, 0))
        self.screen.blit(lvl, (10, 10))
        msg = self.font.render(self.message, True, (0, 0, 0))
        self.screen.blit(msg, (10, 40))

        pygame.display.flip()
        return char_rects, boat_rect

    def handle_click(self, pos, char_rects, boat_rect):
        # character click
        for rect, c in char_rects:
            if rect.collidepoint(pos):
                if c.is_on_boat:
                    # unboard to current boat side
                    self.boat.remove_passenger(c)
                else:
                    # try to board
                    self.boat.add_passenger(c)
                return
        # boat click
        if boat_rect.collidepoint(pos):
            if len(self.boat.passengers) > 0:
                self.boat.boat_move()
                return

    def run(self):
        running = True
        while running:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    char_rects, boat_rect = self.draw()
                    self.handle_click(event.pos, char_rects, boat_rect)

                    if self.check_loss():
                        self.message = 'You lost! Resetting level.'
                        pygame.time.delay(1000)
                        self._setup_game()
                        continue

                    if self.check_win():
                        self.message = 'You won! Advancing level.'
                        pygame.time.delay(1000)
                        self.reset_level(win=True)
                        continue

            # regular draw
            self.draw()

        pygame.quit()


def main():
    g = DevilPriestGame(start_n=2)
    g.run()


if __name__ == '__main__':
    main()
