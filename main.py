#pokemon
#there won't be different types (water, fire, lightning), for now
#only two pokemon: pikachu (user), charizard (cpu)
#one attack per turn, as soon as you attack, end turn
#tip: split up into multiple files if necessary
#get size of screen (curses.LINES - 1), (curses.COLS - 1))

#problems:
#if you press enter more than once before your turn has ended, it saves it for next turn
#a lot of code is sloppy, unorganized, inefficient

import curses, random, time
from curses import wrapper
from curses.textpad import rectangle

pikachu_text = ["", "          __", "  |\\__/| / /", " (>'.'<) \\ \\", '("")_("")/ /']
pikachu_text_inv = ["", "__          ", "\\ \\ |\\__/| ", "/ / (>'.'<) ", '\\ \\("")_("")']
charizard_text = ["   ___", "   \\\"\\     *", "/\\_| |_/\\ /|", " ( (__) )/ /  ", "  \"'  '\"/_/", "  \"'  '\""]
user_attack_text = ["-\\", " -\\", " -/", "-/"]
cpu_attack_text = [" /-", "/-", "\\-", " \\-"]

class Main:
	def __init__(self):
		self.end = False
		self.user = User()
		self.cpu = CPU()
		self.text_win = curses.newwin(3, 63, 9, 2)
		self.attack_win = curses.newwin(4, 9, 2, 41)

	def display_main_text(self, text):
		self.text_win.clear()
		self.text_win.addstr(1, 1, text)
		self.text_win.border()
		self.text_win.refresh()

	def display_hp(self):
		self.user.display_hp()
		self.cpu.display_hp()

	def display_start(self):
		self.user.display_menu()
		self.user.display_pokemon()
		self.cpu.display_pokemon()

	def display_user_attack(self):
		x = 0
		for num in range(6):
			self.attack_win.clear()
			for count, string in enumerate(user_attack_text):
				self.attack_win.addstr(count, x, string)
			x += 1
			self.attack_win.refresh()
			time.sleep(0.3)
		self.attack_win.clear()
		self.attack_win.refresh()

	def display_cpu_attack(self):
		x = 5
		for num in range(6):
			self.attack_win.clear()
			for count, string in enumerate(cpu_attack_text):
				self.attack_win.addstr(count, x, string)
			x -= 1
			self.attack_win.refresh()
			time.sleep(0.3)
		self.attack_win.clear()
		self.attack_win.refresh()

	def user_turn(self):
		self.display_hp()
		self.display_main_text("Choose your attack...")
		self.user.choose()
		self.display_main_text(self.user.get_action_text())
		self.display_user_attack()
		string = "You did " + str(self.user.current_attack[1]) + " damage to Charizard"
		self.display_main_text(string)
		self.cpu.pokemon.health -= self.user.current_attack[1]
		self.display_hp()
		time.sleep(2)

	def cpu_turn(self):
		self.display_hp()
		self.cpu.choose()
		self.display_main_text(self.cpu.get_action_text())
		self.display_cpu_attack()
		string = "Charizard did " + str(self.cpu.current_attack[1]) + " damage to Pikachu"
		self.display_main_text(string)
		self.user.pokemon.health -= self.cpu.current_attack[1]
		self.display_hp()
		time.sleep(2)

	def check_end(self):
		if self.user.pokemon.health <= 0:
			self.display_main_text("You Lose!")
			self.end = True
			time.sleep(2)
		elif self.cpu.pokemon.health <= 0:
			self.display_main_text("You Win!")
			self.end = True
			time.sleep(2)

class User:
	def __init__(self):
		self.pokemon = Pikachu()
		#(amount of lines, amount of chars, starting line, starting char)
		self.choice_win = curses.newwin(len(self.pokemon.attacks) + 1, 2, 2, 0)
		self.choice_win.keypad(True)
		self.moveset_win = curses.newwin(len(self.pokemon.attacks) + 2, 20, 1, 2)
		self.pokemon_win = curses.newwin(6, 15, 1, 25)
		self.pokemon_hp_win = curses.newwin(1, 15, 7, 25)
		self.current_attack = None
		self.cursor_line = 0

	def choose(self):
		key = None
		while key != '\n':
			self.display_choice()
			key = self.choice_win.getkey()
			if key == "KEY_UP" and self.cursor_line != 0:
				self.cursor_line -= 1
			elif key == "KEY_DOWN" and self.cursor_line != len(self.pokemon.attacks) - 1:
				self.cursor_line += 1
		self.current_attack = self.pokemon.attacks[self.cursor_line]

	def display_choice(self):
		self.choice_win.clear()
		self.choice_win.addstr(self.cursor_line, 0, "->", curses.A_BOLD)
		self.choice_win.refresh()

	def display_menu(self):
		self.moveset_win.clear()
		for count, attack in enumerate(self.pokemon.attacks, 1):
			self.moveset_win.addstr(count, 1, attack[0])
		self.moveset_win.border()
		self.moveset_win.refresh()

	def display_pokemon(self):
		self.pokemon_win.clear()
		for count, string in enumerate(pikachu_text_inv):
			self.pokemon_win.addstr(count, 2, string, YELLOW | curses.A_BOLD)
		self.pokemon_win.border(0, 0, 0, 0, "+", "+", "+", "+")
		self.pokemon_win.refresh()

	def display_hp(self):
		self.pokemon_hp_win.clear()
		string = "HP: " + str(self.pokemon.health)
		self.pokemon_hp_win.addstr(string)
		self.pokemon_hp_win.refresh()

	def get_action_text(self):
		return "You chose " + self.current_attack[0]

class CPU:
	def __init__(self):
		self.pokemon = Charizard()
		self.pokemon_win = curses.newwin(6, 15, 1, 50)
		self.pokemon_hp_win = curses.newwin(1, 15, 7, 50)

	def choose(self):
		choice_index = random.randint(0, len(self.pokemon.attacks) - 1)
		self.current_attack = self.pokemon.attacks[choice_index]

	def evaluate(self):
		pass

	def display_pokemon(self):
		self.pokemon_win.clear()
		for count, string in enumerate(charizard_text):
			self.pokemon_win.addstr(count, 1, string, RED | curses.A_BOLD)
		self.pokemon_win.border(0, 0, 0, 0, "+", "+", "+", "+")
		self.pokemon_win.refresh()

	def display_hp(self):
		self.pokemon_hp_win.clear()
		string = "HP: " + str(self.pokemon.health)
		self.pokemon_hp_win.addstr(string)
		self.pokemon_hp_win.refresh()

	def get_action_text(self):
		return "CPU chose " + self.current_attack[0]

class Pikachu:
	def __init__(self):
		self.health = 30
		#each attack will be (name, damage)
		self.attacks = (("Thunder Strike", 10), ("Lightning Smash", 7), ("Bite", 1), ("Pound", 1))
		
class Charizard:
	def __init__(self):
		self.health = 100
		self.attacks = (("Fire Spin", 5), ("Immolation", 10), ("Charge", 3), ("Scratch", 1))

def main_func(stdscr):
	curses.curs_set(0)

	global YELLOW
	global RED
	curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	YELLOW = curses.color_pair(1)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	RED = curses.color_pair(2)
	
	main = Main()

	main.display_start()
	while main.end == False:
		main.user_turn()
		main.check_end()
		if main.end == True:
			break
		main.cpu_turn()
		main.check_end()

wrapper(main_func)