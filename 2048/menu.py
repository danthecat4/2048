import pygame
from game import play_game
from train import train_agent
from params import WIDTH, HEIGHT

pygame.init()

# Colors
BG_COLOR = (130, 125, 115)
BUTTON_COLOR = (245, 225, 40)
BUTTON_HOVER_COLOR = (255, 240, 80)
BUTTON_CLICK_COLOR = (235, 215, 30)
INPUT_COLOR = (50, 50, 50)
INPUT_FOCUS_COLOR = (100, 100, 100)
TEXT_COLOR = (50, 50, 50)
TEXT_LIGHT_COLOR = (240, 230, 230)


class Button:
    """Simple button class."""
    def __init__(self, x, y, width, height, text, font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont("arial", font_size, bold=True)
        self.hovered = False
        self.clicked = False
        
    def draw(self, screen):
        color = BUTTON_CLICK_COLOR if self.clicked else (BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR)
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, TEXT_COLOR, self.rect, 3, border_radius=10)
        
        text_surface = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def update(self, mouse_pos, mouse_pressed):
        self.hovered = self.rect.collidepoint(mouse_pos)
        self.clicked = self.hovered and mouse_pressed


class InputField:
    """Simple input field class."""
    def __init__(self, x, y, width, height, label, default_value="", font_size=24):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.value = str(default_value)
        self.focused = False
        self.font = pygame.font.SysFont("arial", font_size)
        self.label_font = pygame.font.SysFont("arial", 20)
        
    def draw(self, screen):
        # Draw label
        label_surface = self.label_font.render(self.label, True, TEXT_LIGHT_COLOR)
        screen.blit(label_surface, (self.rect.x, self.rect.y - 30))
        
        # Draw input box
        color = INPUT_FOCUS_COLOR if self.focused else INPUT_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, TEXT_LIGHT_COLOR, self.rect, 2, border_radius=5)
        
        # Draw text
        text_surface = self.font.render(self.value, True, TEXT_LIGHT_COLOR)
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.focused = self.rect.collidepoint(mouse_pos)
        elif event.type == pygame.KEYDOWN and self.focused:
            if event.key == pygame.K_BACKSPACE:
                self.value = self.value[:-1]
            elif event.key in [pygame.K_RETURN, pygame.K_TAB]:
                self.focused = False
            elif event.unicode.isdigit() or (event.unicode == "." and "." not in self.value):
                self.value += event.unicode


class Menu:
    """Main menu system."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("2048 - Main Menu")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_screen = "main"
        
    def draw_title(self, title):
        """Draw a centered title."""
        font = pygame.font.SysFont("arial", 56, bold=True)
        text_surface = font.render(title, True, TEXT_LIGHT_COLOR)
        text_rect = text_surface.get_rect(center=(self.width // 2, 50))
        self.screen.blit(text_surface, text_rect)
    
    def main_screen(self):
        """Main menu screen."""
        run = True
        play_button = Button(self.width // 2 - 150, 200, 300, 80, "Play Game")
        train_button = Button(self.width // 2 - 150, 320, 300, 80, "Train AI")
        exit_button = Button(self.width // 2 - 150, 440, 300, 80, "Exit")
        
        while run and self.running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    run = False
            
            play_button.update(mouse_pos, mouse_pressed)
            train_button.update(mouse_pos, mouse_pressed)
            exit_button.update(mouse_pos, mouse_pressed)
            
            if play_button.clicked:
                self.current_screen = "game_settings"
                run = False
            elif train_button.clicked:
                self.current_screen = "train_settings"
                run = False
            elif exit_button.clicked:
                self.running = False
                run = False
            
            self.screen.fill(BG_COLOR)
            self.draw_title("2048")
            play_button.draw(self.screen)
            train_button.draw(self.screen)
            exit_button.draw(self.screen)
            
            pygame.display.update()
            self.clock.tick(60)
    
    def game_settings_screen(self):
        """Game settings configuration screen."""
        run = True
        agent_type = "ai"
        model_path = "2048_model.pth"
        fps = 6
        
        ai_button = Button(150, 200, 150, 60, "AI", 28)
        human_button = Button(350, 200, 150, 60, "Human", 28)
        model_input = InputField(150, 300, 400, 40, "Model Path:", model_path)
        fps_input = InputField(150, 420, 400, 40, "FPS:", fps)
        back_button = Button(100, self.height - 80, 100, 60, "Back", 24)
        play_button = Button(self.width - 200, self.height - 80, 100, 60, "Play", 24)
        
        while run and self.running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    run = False
                model_input.handle_event(event, mouse_pos)
                fps_input.handle_event(event, mouse_pos)
            
            ai_button.update(mouse_pos, mouse_pressed)
            human_button.update(mouse_pos, mouse_pressed)
            back_button.update(mouse_pos, mouse_pressed)
            play_button.update(mouse_pos, mouse_pressed)
            
            if ai_button.clicked:
                agent_type = "ai"
            elif human_button.clicked:
                agent_type = "human"
            elif back_button.clicked:
                self.current_screen = "main"
                run = False
            elif play_button.clicked:
                try:
                    fps = int(fps_input.value) if fps_input.value else 6
                    model_path = model_input.value if model_input.value else "2048_model.pth"
                    play_game(agent_type=agent_type, model_path=model_path, fps=fps)
                except ValueError:
                    pass
                self.current_screen = "main"
                run = False
            
            self.screen.fill(BG_COLOR)
            self.draw_title("Game Settings")
            
            # Player type label and buttons
            font = pygame.font.SysFont("arial", 24)
            player_label = font.render("Select Player:", True, TEXT_LIGHT_COLOR)
            self.screen.blit(player_label, (150, 160))
            
            ai_button.text = "AI" if agent_type != "ai" else "AI"
            human_button.text = "Human" if agent_type != "human" else "Human"
            ai_button.draw(self.screen)
            human_button.draw(self.screen)
            
            # Conditionally draw model path input
            if agent_type == "ai":
                model_input.draw(self.screen)
            
            fps_input.draw(self.screen)
            back_button.draw(self.screen)
            play_button.draw(self.screen)
            
            pygame.display.update()
            self.clock.tick(60)
    
    def train_settings_screen(self):
        """Training settings configuration screen."""
        run = True
        episodes = 50000
        model_path = "2048_model.pth"
        log_interval = 10
        save_interval = 1000
        
        episodes_input = InputField(150, 200, 400, 40, "Episodes:", episodes)
        model_input = InputField(150, 310, 400, 40, "Model Path:", model_path)
        log_input = InputField(150, 420, 400, 40, "Log Interval:", log_interval)
        save_input = InputField(150, 530, 400, 40, "Save Interval:", save_interval)
        back_button = Button(100, self.height - 80, 100, 60, "Back", 24)
        train_button = Button(self.width - 200, self.height - 80, 100, 60, "Train", 24)
        
        while run and self.running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    run = False
                episodes_input.handle_event(event, mouse_pos)
                model_input.handle_event(event, mouse_pos)
                log_input.handle_event(event, mouse_pos)
                save_input.handle_event(event, mouse_pos)
            
            back_button.update(mouse_pos, mouse_pressed)
            train_button.update(mouse_pos, mouse_pressed)
            
            if back_button.clicked:
                self.current_screen = "main"
                run = False
            elif train_button.clicked:
                try:
                    episodes = int(episodes_input.value) if episodes_input.value else 50000
                    model_path = model_input.value if model_input.value else "2048_model.pth"
                    log_interval = int(log_input.value) if log_input.value else 10
                    save_interval = int(save_input.value) if save_input.value else 1000
                    
                    train_agent(
                        episodes=episodes,
                        model_save_path=model_path,
                        log_interval=log_interval,
                        save_interval=save_interval
                    )
                except ValueError:
                    pass
                self.current_screen = "main"
                run = False
            
            self.screen.fill(BG_COLOR)
            self.draw_title("Training Settings")
            
            episodes_input.draw(self.screen)
            model_input.draw(self.screen)
            log_input.draw(self.screen)
            save_input.draw(self.screen)
            back_button.draw(self.screen)
            train_button.draw(self.screen)
            
            pygame.display.update()
            self.clock.tick(60)
    
    def run(self):
        """Main menu loop."""
        while self.running:
            if self.current_screen == "main":
                self.main_screen()
            elif self.current_screen == "game_settings":
                self.game_settings_screen()
            elif self.current_screen == "train_settings":
                self.train_settings_screen()
        
        pygame.quit()


if __name__ == "__main__":
    menu = Menu(WIDTH, HEIGHT)
    menu.run()
