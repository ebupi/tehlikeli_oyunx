import pgzrun  # Pygame Zero kutuphanesini ice aktar
from random import randint  # Rastgele sayi uretmek icin randint fonksiyonunu ice aktar
from pygame import Rect  # dikdortgen olusturmak icin Rect sinifini ice aktar
import time  # Zaman islemleri icin time modulunu ice aktar

# Oyun ayarlari
WIDTH = 800  # oyun penceresinin genisligi
HEIGHT = 600  # oyun penceresinin yuksekligi
TILE_SIZE = 40  # karakterlerin boyutu (kare seklinde)
PLAYER_SPEED = 3  # oyuncunun hareket hizi
ENEMY_SPEED = 2  # dusmanlarin hareket hizi
NUM_ENEMIES = 5  # dusman sayisi

# dusman sayisini ve hiz ifadelerini 
# ayarlamalı olarak baslangic ekraninda verebiliriz
# carpisinca dusmanlari yiyelim ya da yok edelim
# bu da baska bir oyna benzer 
# Oguzcum Ataya saygilarlaa --Tehlikeli Oyunlar--

# Oyun durumu
game_over = False  # oyunun bitip bitmedigini kontrol etmek icin
show_welcome = True  # hosgeldin ekranini gosterir
game_over_time = 0  # Game Over oldugunda zamani kaydetmek icin tanimli
score = 0  # oyuncunun skoru
start_time = time.time()  # oyunun baslangic zamani

# Buton sinifi
class Button:
    """
    Buton sinifi, tiklanabilir butonlari temsil eder.
    """

    def __init__(self, x, y, width, height, text, color, hover_color):
        """
        Buton sinifinin yapici metodu.
        """
        self.rect = Rect(x, y, width, height)  # Butonun dikdortgen alani
        self.text = text  # Buton metni
        self.color = color  # Buton rengi
        self.hover_color = hover_color  # Butonun uzerine gelindigindeki rengi
        self.is_hovered = False  # Butonun uzerine gelindi mi?

    def draw(self):
        """
        Butonu ekrana cizer.
        """
        # buton rengini belirle (uzerine gelindiginde hover rengi kullan)
        color = self.hover_color if self.is_hovered else self.color
        screen.draw.filled_rect(self.rect, color)  # butonun arka planini ciz
        screen.draw.text(
            self.text,
            center=self.rect.center,  # metni butonun ortasina yerlestir
            fontsize=40,
            color="white"
        )

    def check_hover(self, mouse_pos):
        """
        Fare butonun uzerinde mi kontrol eder.
        """
        self.is_hovered = self.rect.collidepoint(mouse_pos)  # fare butonun uzerinde mi?

    def is_clicked(self, mouse_pos):
        """
        Butona tiklandi mi kontrol eder.

        Args:
            mouse_pos (tuple): Farenin (x, y) koordinatlari.

        Returns:
            bool: Butona tiklandiysa True, aksi halde False.
        """
        return self.rect.collidepoint(mouse_pos)  # fare butonun uzerinde ve tiklandi mi?

# buton ornekleri
start_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100, "Basla", "blue", "lightblue")  # basla butonu
restart_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 100, "Yeniden Başla", "green", "lightgreen") # yeniden basla butonu
exit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 100, "Çıkış", "red", "pink") # cikis butonu

# karakter sinifi
class Character:
    """
    Karakter sinifi, oyuncu ve dusmanlarin ozelliklerini ve davranislarini tanimlar.
    """

    def __init__(self, x, y, image, speed):
        """
        Karakter sinifinin yapici metodu.
        """
        self.x = x  # karakterin x koordinati
        self.y = y  # karakterin y koordinati
        self.image = image  # karakterin gorseli
        self.speed = speed  # karakterin hareket hizi
        self.direction = "down"  # karakterin baslangic yonu
        self.size = TILE_SIZE  # karakterin boyutu
        self.animation_frame = 0  # animasyon icin frame sayaci

    def move(self, dx, dy):
        """
        Karakteri belirtilen yonde hareket ettirir ve animasyonu gunceller.

        Args:
            dx (int): x eksenindeki hareket yonu (-1: sol, 1: sag).
            dy (int): y eksenindeki hareket yonu (-1: yukari, 1: asagi).
        """
        self.x += dx * self.speed  # x koordinatini guncelle
        self.y += dy * self.speed  # y koordinatini guncelle
        if dx > 0:
            self.direction = "right"  # saga hareket ediyor
        elif dx < 0:
            self.direction = "left"  # sola hareket ediyor
        elif dy > 0:
            self.direction = "down"  # asagi hareket ediyor
        elif dy < 0:
            self.direction = "up"  # yukari hareket ediyor

        self.animation_frame = (self.animation_frame + 1) % 10  # frame sayacini guncelle
        if self.animation_frame < 5:
            self.size = TILE_SIZE + 5  # karakteri buyut
        else:
            self.size = TILE_SIZE  # karakteri kucult

    def draw(self):
        """
        Karakteri ekrana cizer.
        """
        screen.blit(self.image, (self.x, self.y))  # gorseli ekrana ciz

# oyuncu ve dusmanlar
player = Character(400, 300, "player", PLAYER_SPEED)  # oyuncu karakteri olustur
enemies = [Character(randint(0, WIDTH), randint(0, HEIGHT), "enemy", ENEMY_SPEED) for _ in range(NUM_ENEMIES)]  # Dusman karakterleri olustur

# carpisma kontrolu
def check_collision(player, enemy):
    """
    Oyuncu ve dusman arasinda carpisma olup olmadigini kontrol eder.
        player (Character): Oyuncu karakteri.
        enemy (Character): Dusman karakteri.

    Returns:
        bool: carpisma varsa True, yoksa False.
    """
    return (player.x < enemy.x + TILE_SIZE and
            player.x + TILE_SIZE > enemy.x and
            player.y < enemy.y + TILE_SIZE and
            player.y + TILE_SIZE > enemy.y)

# oyunu sifirla
def reset_game():
    """
    Oyunu baslangic durumuna sifirlar.
    """
    global game_over, show_welcome, score, start_time, player, enemies
    game_over = False  # oyunu baslat
    show_welcome = False  # hosgeldin ekrnini kapat
    score = 0  # skoru sifirla
    start_time = time.time()  # zamanlayiciyi sifirla
    player = Character(400, 300, "player", PLAYER_SPEED)  # Oyuncuyu yeniden olustur
    enemies = [Character(randint(0, WIDTH), randint(0, HEIGHT), "enemy", ENEMY_SPEED) for _ in range(NUM_ENEMIES)]  # duusmanlari yeniden olustur

# oyun dongusu
def update():
    """
    Oyunun guncelleme mantigini icerir. Her karede bir kez cagrilir.
    """
    global game_over, show_welcome, game_over_time, score

    if game_over:
        return  # oyun bittiyse guncelleme yapma

    if show_welcome:
        return  # hosgeldin ekrani gosteriliyorsa guncelleme yapma

    if keyboard.left:
        player.move(-1, 0)  # oyuncuyu sola hareket ettir
    if keyboard.right:
        player.move(1, 0)  # oyuncuyu saga hareket ettir
    if keyboard.up:
        player.move(0, -1)  # oyuncuyu yukari hareket ettir
    if keyboard.down:
        player.move(0, 1)  # oyuncuyu asagi hareket ettir

    for enemy in enemies:
        enemy.move(randint(-1, 1), randint(-1, 1))  # Dusmani rastgele hareket ettir

        if check_collision(player, enemy):
            game_over = True  # oyunu bitir
            game_over_time = time.time()  # Game Over zamanini kaydet
            sounds.crash.play()  # carpisma sesi

    # skoru guncelle
    score = int(time.time() - start_time)

def draw():
    """
    Oyunun cizim mantigini icerir. Her karede bir kez cagrilir.
    """
    screen.clear()

    if show_welcome:
        screen.blit("background", (0, 0))  # arka plan gorseli
        start_button.draw()  # basla butonunu ciz
    elif game_over:
        screen.blit("background", (0, 0))  # arka plan gorseli
        screen.draw.text(
            "Game Over!",
            center=(WIDTH // 2, HEIGHT // 2 - 100),
            fontsize=60,
            color="red"
        )
        screen.draw.text(
            f"Skorunuz: {score}",
            center=(WIDTH // 2, HEIGHT // 2 - 50),
            fontsize=40,
            color="white"
        )
        restart_button.draw()  # yeniden basla butonunu ciz
        exit_button.draw()  # cikis butonunu ciz
    else:
        screen.blit("background", (0, 0))  # arka plan gorseli
        player.draw()  # oyuncuyu ciz
        for enemy in enemies:
            enemy.draw()  # dusmanlari ciz
        screen.draw.text(
            f"Skor: {score}",
            topleft=(10, 10),
            fontsize=30,
            color="white"
        )

# fare tiklamasini kontrol et
def on_mouse_down(pos):
    """
    Fare tiklamasini isler.

    Args:
        pos (tuple): Farenin (x, y) koordinatlari.
    """
    global show_welcome, game_over

    if show_welcome:
        if start_button.is_clicked(pos):  # basla butonuna tiklandi mi?
            show_welcome = False  # hosgeldin ekranini kapat
            sounds.start.play()  # oyun baslama sesi
    elif game_over:
        if restart_button.is_clicked(pos):  # yeniden basla butonuna tiklandi mi?
            reset_game()  # oyunu sifirla
        elif exit_button.is_clicked(pos):  # cikis butonuna tiklandi mi?
            quit()  # oyunu kapat

# fare hareketini kontrol et
def on_mouse_move(pos):
    """
    Fare hareketini isler.

    Args:
        pos (tuple): Farenin (x, y) koordinatlari.
    """
    if show_welcome:
        start_button.check_hover(pos)  # basla butonunun uzerine gelindi mi?
    elif game_over:
        restart_button.check_hover(pos)  # yeniden basla butonunun uzerine gelindi mi?
        exit_button.check_hover(pos)  # cikis butonunun uzerine gelindi mi?

# oyunu baslat
pgzrun.go()