# подключение pygame
import pygame

# инициализация (включение всех возможностей) pygame
pygame.init()

# создание игрового окна
mw = pygame.display.set_mode((500, 500))
# цвет фона
back = (140, 140, 255)

# Картинка для паузы игры
pause_img = pygame.transform.scale(pygame.image.load("pause.png"), (32, 32))
# Картинка для продолжения игры
play_img = pygame.transform.scale(pygame.image.load("play.png"), (32, 32))
# Картинка для возобновления игры
replay_img = pygame.transform.scale(pygame.image.load("replay.png"), (32, 32))

# Главный класс Picture
# реализует возможность изображения на окне
# картинки как самостоятельного объекта
class Picture():
	# конструктор класса
	# x     - горизонтальная координата места картинки
	# y     - вертикальная координата места картинки
	# png   - имя картинки, которую надо изобразить
	# color - цвет фотна объекта (цвет "хитбокса")
	def __init__(self, x, y, png, color=(140, 140, 255)):
		# поле картинки
		self.image = pygame.image.load(png)
		# "хитбокс" картинки
		self.rect = pygame.Rect(x, y, self.image.get_rect().w, self.image.get_rect().h)
		# поле цвета "хитбокса"
		self.color = color

		# Двигается ли платформа вправо
		self.move_right = False
		# Двигается ли платформа влево
		self.move_left = False
		# Эти поля нужны в конце игры
		# Двигается ли платформа вверх
		self.move_up = False
		# Двигается ли платформа вниз
		self.move_down = False

		# Скорость платформы
		self.step = 6

	# Функция отрисовки
	def draw(self):
		# Рисуем "хитбокс" платформы
		pygame.draw.rect(mw, self.color, self.rect)

		# Изображаем картинку повех "хитбокса"
		mw.blit(self.image, (self.rect.x, self.rect.y))

	# Функция проверки столкновения двух "хитбоксов"
	def colliderect(self, rect):
		return self.rect.colliderect(rect)

	# Установить другой цвет "хитбокса" 
	def set_color(self, color):
		self.color = color

# Функция создания списка монстров на окне
def create_monsters(count):
	# Список монстров, изначально пустой
	res_list = []

	# У нас будет 3 строки монстров
	# В первой 9, во второй 8, в третьей 7

	# п - переменная, отвечающая за количество монстров в текущей строке
	#     начальное значение 9
	n = count
	# Запускаем цикл 3 раза, потому что у нас три строки
	for i in range(3):
		# Вычисляем координату первого монстра в строке
		x, y = (5+i*20, 5+i*50)

		# Запускаем цикл по созданию монстров в i-ой строке (i = 0, 1, 2)
		for j in range(n):
			# Создаём одного монстра в вычисленных ранее координатах x,y
			#     он бует изображаться с картинкой 'enemy.png'
			tmp_monster = Picture(x, y, 'enemy.png')
			
			# Вставляем созданного монстра в список монстров
			res_list.append(tmp_monster)

			# Сдвигаем стартовую позицию следующего в строке монстра
			x += 55

		# Уменьшаем количество монстров в следующей строке
		# Было 9 станет 8, было 8 станет 7
		n -= 1

	# Возвращаем массив созданных монстров
	return res_list


# переменная со всеми монстрами
monsters = create_monsters(9)
# Начальное количество монстров
start_count = len(monsters)

# Мяч
ball = Picture(200, 300, "ball.png")
# Горизонтальная скорость мяча
ball_x_speed = 6
# Вертикальная скорость мяча
ball_y_speed = 6

'''
Можно удалить этот блок
push_up = 0
push_right = 0
push_down = 0
push_left = 0
push_step = 2


def clear_push():
	push_up = 0
	push_right = 0
	push_down = 0
	push_left = 0
	
	ball_x_speed = 6
	ball_y_speed = 6
'''

# Платформа
platform = Picture(200, 425,'platform.png')

# Переменная паузы
# 0 - игра идёт
# 1 - игра завершена (выиграл/програл)
# 2 - игра поставлена на паузу
pause = 0
# Переменная выиграша (выиграл/програл)
win = False

# Работает ли приложение
run = True
# Игровой цикл
while run:
	# Обработка всех событий
	for ev in pygame.event.get():
		# Обработка события закрытия окна
		if ev.type == pygame.QUIT:
			run = False

		# Если нажата кнопка
		if ev.type == pygame.KEYDOWN:
			# Стрелка вправо
			if ev.key == pygame.K_RIGHT:
				platform.move_right = True
			# Стрелка влево
			if ev.key == pygame.K_LEFT:
				platform.move_left = True
			# Стрелка вниз
			if ev.key == pygame.K_UP:
				platform.move_up = True
			# Стрелка вверх
			if ev.key == pygame.K_DOWN:
				platform.move_down = True
			# Конка пробе (пауза)
			if ev.key == pygame.K_SPACE:
				pause = 0 if pause == 2 else 2
			# Кнопка Е (выход из приложения по окончании игры)
			if ev.key == pygame.K_e and pause == 1:
				run = False
			# Кнопка R (перезапустить игру по окончании)
			if ev.key == pygame.K_r and pause == 1:
				# Выставление всех нужных значенией в начальные значения
				pause = 0
				win = False

				monsters = create_monsters(9)
				
				ball.rect.x = 200
				ball.rect.y = 300
				ball_x_speed = 6
				ball_y_speed = 6

				platform.rect.x = 200
				platform.rect.y = 425

				back = (140, 140, 255)
				platform.set_color(back)

		# Если кнопку отжали
		if ev.type == pygame.KEYUP:
			# Стрелка вправо
			if ev.key == pygame.K_RIGHT:
				platform.move_right = False
			# Стрелка влево
			if ev.key == pygame.K_LEFT:
				platform.move_left = False
			# Стрелка вниз
			if ev.key == pygame.K_UP:
				platform.move_up = False
			# Стрелка вверх
			if ev.key == pygame.K_DOWN:
				platform.move_down = False

	# Блок движения платформы
	# Если игра не остановлена и платформа движется вправо
	if platform.move_right and pause != 2:
		# Если платформа не упёрлась в правую стену
		if platform.rect.x < 398:
			# Сдвинуть платформу вправо
			platform.rect.x += platform.step
	# Если игра не остановлена и платформа движется влево
	if platform.move_left and pause != 2:
		# Если платформа не упёрлась в левую стену
		if platform.rect.x > 5:
			# Сдвинуть платформу влево
			platform.rect.x -= platform.step
	# Если игра завершилась и платформа движется вверх
	if pause == 1 and platform.move_up:
		# Если платформа не упёрлась в потолок
		if platform.rect.y > 3:
			# Сдвинуть платформу вверх
			platform.rect.y -= platform.step
	# Если игра завершилась и платформа движется вниз
	if pause == 1 and platform.move_down:
		# Если платформа не упёрлась в пол
		if platform.rect.y < 472:
			# Сдвинуть платформу вниз
			platform.rect.y += platform.step
	
	# Залить цветом фон игры
	mw.fill(back)

	# Если игра не завершена (продолжается или остановлена)
	if pause in [0, 2]:
		# Работа с монстрами
		for m in monsters:
			# Отрисовка каждого монстра
			m.draw()
			
			# Проверка столкновений монстров с мячём
			# Если столкновение произошло
			if m.colliderect(ball.rect):
				# Удалить мостра из списка
				monsters.remove(m)
				'''clear_push()'''
				# Отразить мяч вниз
				ball_y_speed *= -1

		# Если игра продолжается
		if pause == 0:
			# Перемещение мяча по горищонтали
			ball.rect.x += ball_x_speed
			# Перемещение мяча по вертикали
			ball.rect.y += ball_y_speed

			'''
			ball.rect.x += (ball_x_speed + push_step*push_right - push_step*push_left)
			ball.rect.y += (ball_y_speed + push_step*push_down - push_step*push_up)
			'''
			
			# Отражение мяча от левой стены
			if ball.rect.x < 0:
				ball.rect.x = 0
				'''clear_push()'''
				ball_x_speed *= -1
			# Отражение мяча от правой стены
			if ball.rect.x > 450:
				ball.rect.x = 450
				'''clear_push()'''
				ball_x_speed *= -1
			# Отражение мяча от потолка
			if ball.rect.y < 0:
				ball.rect.y = 0
				'''clear_push()'''
				ball_y_speed *= -1
			# Отражение мяча от платформы
			if ball.colliderect(platform.rect):
				ball.rect.y = platform.rect.y - 51
				ball_y_speed *= -1
				'''
				push_up = int(platform.move_up)
				push_right = int(platform.move_right)
				push_down = int(platform.move_down)
				push_left = int(platform.move_left)
				'''

			# Изображение картинки паузы
			mw.blit(pause_img, (450, 450))
		# Если игра остановлена
		# Мяч не будет перемещаться
		else:
			# Изабражение картинки продолжения игры
			mw.blit(play_img, (450, 450))

		# Если мяч вылетел за платформу или закончились все противники игра останавливается
		if ball.rect.y > platform.rect.y or len(monsters) == 0:
			pause = 1
		# Если закончили все противники игра выиграна
		if len(monsters) == 0:
			win = True

		# Отрисовываем мяч
		ball.draw()

		# Счётчик выбитых монстров
		pointer_text = pygame.font.Font(None, 30).render(f"Count: {start_count - len(monsters)}", True, (0, 0, 0))
		# Отрисовка счётчика
		mw.blit(pointer_text, (20, 465))
	# Если игра завершена
	else:
		# Текст в помощь на переигровку
		replay_help = pygame.font.Font(None, 30).render("Press key 'R' to replay", True, (0, 0, 0))
		# Текст в помощь на выход
		exit_text = pygame.font.Font(None, 30).render("Press key 'E' to exit", True, (0, 0, 0))
		# Если игра выиграна
		if win:
			# Финальный текст
			win_text = pygame.font.Font(None, 80).render("You WIN!!!", True, (144, 238, 144))
		else:
			# Финальный текст
			win_text = pygame.font.Font(None, 80).render("You LOSE(", True, (0, 0, 0))
			# Меняем цвет фона на красный
			back = (200, 0, 0)
			# Задаём цвет "хитбокса" платформы тоже красным
			platform.set_color(back)
		# Отрисовка всего текста
		mw.blit(win_text, (125, 215))
		mw.blit(replay_help, (170, 268))
		mw.blit(replay_img, (250, 297))
		mw.blit(exit_text, (170, 350))
	
	# Отрисовка платформы
	platform.draw()
	
	# Обновление игровой сцены
	pygame.display.update()
	pygame.time.delay(40)
