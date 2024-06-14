import cv2
import mediapipe as mp
import pyautogui
import pygame
import random
import time
import math

# Initialize Pygame
pygame.init()
pyautogui.FAILSAFE = False

# Screen dimensions
screen_w, screen_h = 1364, 700
screen = pygame.display.set_mode((screen_w, screen_h))

# Game variables
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (75, 75))
enemy1_image = pygame.image.load("enemy.png")
enemy2_image = pygame.image.load("enemy2.png")
bullet_image = pygame.image.load("bullet.png")
background_image = pygame.image.load("Background.png")
pause_button = pygame.image.load("pause_button.png")
pause_button = pygame.transform.scale(pause_button, (75, 75))

# Main menu assets
menu_background = pygame.image.load("Background.png")  # Background for the menu
space_header = pygame.image.load("space_header.png")
game_header = pygame.image.load("game_header.png")
start_button = pygame.image.load("start_button.png")
start_button = pygame.transform.scale(start_button, (250, 80))
map_button = pygame.image.load("map_button.png")
map_button = pygame.transform.scale(map_button, (250, 80))
exit_button = pygame.image.load("exit_button.png")
exit_button = pygame.transform.scale(exit_button, (250, 80))

player_x = screen_w // 2 - 32 + 10
player_y = screen_h - 95

enemy_speed = 3
bullet_speed = 18

bullets = []
enemies = []

score = 0
health = 100
level = 1
paused = False

font = pygame.font.Font(None, 36)

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

sensitivity = 15.0

calibrated = False
calibration_x, calibration_y = 0, 0


def calibrate(landmarks, frame_w, frame_h):
    global calibration_x, calibration_y, calibrated
    left_eye_x = (landmarks[474].x + landmarks[475].x + landmarks[476].x + landmarks[477].x) / 4
    left_eye_y = (landmarks[474].y + landmarks[475].y + landmarks[476].y + landmarks[477].y) / 4
    calibration_x = left_eye_x * frame_w
    calibration_y = left_eye_y * frame_h
    calibrated = True


def is_blinking(left_eye):
    top_bottom_dist = abs(left_eye[0].y - left_eye[1].y)
    return top_bottom_dist < 0.004


def spawn_enemy(enemy_type):
    top_bar_height = 70  # Assuming the top bar height is 100 pixels
    enemy_x = random.randint(0, screen_w - 64)
    enemy_y = random.randint(top_bar_height, top_bar_height + 70)
    enemies.append([enemy_x, enemy_y, enemy_speed, enemy_type])



def shoot_bullet(target_x, target_y):
    bullet_x = player_x + 32
    bullet_y = player_y
    angle = math.atan2(target_y - bullet_y, target_x - bullet_x)
    bullets.append([bullet_x, bullet_y, angle])


def move_bullets():
    for bullet in bullets:
        bullet[0] += bullet_speed * math.cos(bullet[2])
        bullet[1] += bullet_speed * math.sin(bullet[2])
        if bullet[1] < 0 or bullet[1] > screen_h or bullet[0] < 0 or bullet[0] > screen_w:
            bullets.remove(bullet)


def move_enemies(pixels):
    global enemy_speed
    for enemy in enemies:
        enemy[0] += enemy[2]
        if enemy[0] < 0 or enemy[0] > screen_w - 64:
            enemy[2] = random.choice([-enemy_speed, enemy_speed])
            enemy[1] += pixels
            if enemy[0] < 0:
                enemy[0] = 0
            elif enemy[0] > screen_w - 64:
                enemy[0] = screen_w - 64


def check_collision():
    global score, health, enemy_speed , level
    for enemy in enemies:
        for bullet in bullets:
            if (bullet[0] > enemy[0] and bullet[0] < enemy[0] + 64) and (
                    bullet[1] > enemy[1] and bullet[1] < enemy[1] + 64):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1
                if score <= 20:
                    spawn_enemy(enemy1_image)
                    break
                elif 20 < score < 50:
                    spawn_enemy(enemy1_image)
                    spawn_enemy(enemy1_image)
                    break
                else:
                    spawn_enemy(enemy1_image)
                    break

    if not enemies:
        for _ in range(10):
            spawn_enemy(enemy1_image)

    if score >= 50:
        enemy_speed = 8
        level = 2
    elif score >= 20:
        enemy_speed = 5
    elif score >= 100:
        enemy_speed = 10
        level = 3
    for i in range(len(enemies)):
        if enemies[i][1] > screen_h - 110:
            health -= 1
            enemies.pop(i)  # Remove the enemy at index i
            break  # Break the loop to avoid skipping enemies

    if health <= 0:
        print("Game Over")
        main_menu_loop()


def draw_health():
    health_text = font.render(f"Health: {health}", True, white)
    screen.blit(health_text, (10, 40))

def draw_level():
    # Create a font object with a larger size
    large_font = pygame.font.Font(None, 56)  # Change 36 to your desired font size

    # Render the text using the larger font
    level_text = large_font.render(f"Level: {level}" , True , white)

    # Calculate the position
    text_width, text_height = level_text.get_size()
    x = (screen_w - text_width) // 2  # Center horizontally
    y = 30  # Position vertically

    # Blit the text onto the screen
    screen.blit(level_text, (x, y))

def draw_score():
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))


def draw_base_line():
    pygame.draw.line(screen, red, (0, screen_h - 110), (screen_w, screen_h - 100), 5)

def draw_pause():
    # Draw the pause button
    pause_button_rect = pause_button.get_rect(topright=screen.get_rect().topright)
    screen.blit(pause_button, pause_button_rect)
    return pause_button_rect


def pause_menu():
    global paused
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = False

        screen.fill(black)
        resume_text = font.render("Resume", True, white)
        sound_text = font.render("Sound", True, white)
        music_text = font.render("Music", True, white)
        exit_text = font.render("Exit to Main Menu", True, white)

        resume_rect = resume_text.get_rect(center=(screen_w // 2, screen_h // 2 - 50))
        sound_rect = sound_text.get_rect(center=(screen_w // 2, screen_h // 2))
        music_rect = music_text.get_rect(center=(screen_w // 2, screen_h // 2 + 50))
        exit_rect = exit_text.get_rect(center=(screen_w // 2, screen_h // 2 + 100))

        screen.blit(resume_text, resume_rect)
        screen.blit(sound_text, sound_rect)
        screen.blit(music_text, music_rect)
        screen.blit(exit_text, exit_rect)

        mouse_pos = pygame.mouse.get_pos()
        if resume_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            paused = False
        elif exit_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            main_menu_loop()
            return

        pygame.display.flip()
        time.clock.tick(30)


def main_game_loop():
    global running, player_x, player_y , paused
    running = True
    clock = pygame.time.Clock()

    while running:
        ret, frame = cam.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmarks_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused  # Toggle pause state
                    if paused:
                        pause_menu()
        if landmarks_points:
            landmarks = landmarks_points[0].landmark

            if not calibrated:
                cv2.putText(frame, "Look at the red dot for calibration",
                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                center_x, center_y = frame_w // 2, frame_h // 2
                cv2.circle(frame, (center_x, center_y), 10, (0, 0, 255), -1)
                cv2.imshow('Eye Controlled Mouse', frame)
                cv2.waitKey(1)
                time.sleep(3)
                calibrate(landmarks, frame_w, frame_h)
            else:
                left_eye_x = (landmarks[474].x + landmarks[475].x + landmarks[476].x + landmarks[477].x) / 4
                left_eye_y = (landmarks[474].y + landmarks[475].y + landmarks[476].y + landmarks[477].y) / 4

                delta_x = (left_eye_x * frame_w - calibration_x) * sensitivity
                delta_y = (left_eye_y * frame_h - calibration_y) * sensitivity

                screen_x = screen_w / 2 + delta_x
                screen_y = screen_h / 2 + delta_y

                screen_x = min(max(screen_x, 0), 1366)
                screen_y = min(max(screen_y, 0), screen_h - 1)

                pyautogui.moveTo(screen_x, screen_y)
                print(f"Cursor Position: ({screen_x}, {screen_y})")

                left_eye = [landmarks[145], landmarks[159]]
                if is_blinking(left_eye):
                    shoot_bullet(screen_x, screen_y)
                    print('Click triggered by left eye blink')

            for i in range(474, 478):
                x = int(landmarks[i].x * frame_w)
                y = int(landmarks[i].y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

            left_eye = [landmarks[145], landmarks[159]]
            for landmark in left_eye:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)

        screen.fill(black)
        screen.blit(background_image, (0, 0))
        screen.blit(player_image, (player_x, player_y))

        move_bullets()
        for bullet in bullets:
            screen.blit(bullet_image, (bullet[0], bullet[1]))

        move_enemies(100)
        for enemy in enemies:
            screen.blit(enemy1_image, (enemy[0], enemy[1]))
            screen.blit(enemy2_image, (enemy[0], enemy[1]))

        check_collision()
        draw_score()
        draw_health()
        draw_level()
        draw_pause()
        draw_base_line()

        pygame.display.flip()
        clock.tick(30)

        cv2.imshow('Eye Controlled Mouse', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    pygame.quit()


def main_menu_loop():
    global calibrated
    menu_running = True
    clock = pygame.time.Clock()

    # Calculate the positions of the buttons with a 5-pixel gap
    start_button_rect = start_button.get_rect(center=(screen_w // 2, screen_h // 2))
    map_button_rect = map_button.get_rect(
        center=(screen_w // 2, start_button_rect.bottom + 5 + map_button.get_height() // 2))
    exit_button_rect = exit_button.get_rect(
        center=(screen_w // 2, map_button_rect.bottom + 5 + exit_button.get_height() // 2))

    while menu_running:
        ret, frame = cam.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmarks_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False

        screen.blit(menu_background, (0, 0))

        # Display header images
        screen.blit(space_header, (screen_w // 2 - space_header.get_width() // 2, 50))
        screen.blit(game_header, (screen_w // 2 - game_header.get_width() // 2, 145))

        # Display buttons with a 5-pixel gap between them
        screen.blit(start_button, start_button_rect)
        screen.blit(map_button, map_button_rect)
        screen.blit(exit_button, exit_button_rect)

        # Check if the cursor is hovering over any button
        mouse_pos = pygame.mouse.get_pos()
        if (start_button_rect.collidepoint(mouse_pos) or
                map_button_rect.collidepoint(mouse_pos) or
                exit_button_rect.collidepoint(mouse_pos)):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()

        if landmarks_points:
            landmarks = landmarks_points[0].landmark

            if not calibrated:
                cv2.putText(frame, "Look at the red dot for calibration",
                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                center_x, center_y = frame_w // 2, frame_h // 2
                cv2.circle(frame, (center_x, center_y), 10, (0, 0, 255), -1)
                cv2.imshow('Eye Controlled Mouse', frame)
                cv2.waitKey(1)
                time.sleep(3)
                calibrate(landmarks, frame_w, frame_h)
            else:
                left_eye_x = (landmarks[474].x + landmarks[475].x + landmarks[476].x + landmarks[477].x) / 4
                left_eye_y = (landmarks[474].y + landmarks[475].y + landmarks[476].y + landmarks[477].y) / 4

                delta_x = (left_eye_x * frame_w - calibration_x) * sensitivity
                delta_y = (left_eye_y * frame_h - calibration_y) * sensitivity

                screen_x = screen_w / 2 + delta_x
                screen_y = screen_h / 2 + delta_y

                screen_x = min(max(screen_x, 0), 1366)
                screen_y = min(max(screen_y, 0), screen_h - 1)

                pyautogui.moveTo(screen_x, screen_y)
                print(f"Cursor Position: ({screen_x}, {screen_y})")

                left_eye = [landmarks[145], landmarks[159]]
                if is_blinking(left_eye):
                    if start_button_rect.collidepoint(screen_x, screen_y):
                        menu_running = False
                        main_game_loop()

        clock.tick(30)
        cv2.imshow('Eye Controlled Mouse', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    pygame.quit()


if __name__ == "__main__":
    main_menu_loop()
