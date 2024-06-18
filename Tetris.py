from tkinter import * # bibliothèque graphique
import random
import pygame

# Initialiser la table de mixage dans pygame pour jouer de la musique de fond
pygame.mixer.init()
pygame.mixer.music.load("Desktop\pyton\\tetris.mp3")
#pygame.mixer.music.load("tetris.mp3")
pygame.mixer.music.play(-1)  # Joue la musique en boucle

# Définir la taille des cellules et les dimensions de la grille
cell_size = 30 # taille des cellules
cols = 10 # colones
rows = 20 # lignes

# Créer la fenêtre principale de l'application
root = Tk() # Tool Kit. permet de créer l'interface graphique. 
root.title("Tetris")


# Créer un canevas pour dessiner le jeu Tetris
canvas = Canvas(root, width=cell_size*cols, height=cell_size*rows) # fenêtre globale
canvas.pack()

class Tetris:
    # Définir les formes des pièces de Tetris
    shapes = [
        [[1, 1, 1, 1]],  # Forme I 
        [[1, 1], [1, 1]],  # Forme O 
        [[0, 1, 0], [1, 1, 1]],  # Forme T 
        [[1, 0, 0], [1, 1, 1]],  # Forme L 
        [[0, 0, 1], [1, 1, 1]],  # Forme J 
        [[0, 1, 1], [1, 1, 0]],  # Forme S 
        [[1, 1, 0], [0, 1, 1]]  # Forme Z 
    ]
    
    def __init__(self):
        self.canvas = canvas  # Initialiser la grille
        self.grid = [[0] * cols for _ in range(rows)]  # Créer une grille pour représenter l'état du jeu
        self.bind_keys()  # Lier les touches du clavier aux commandes du jeu
        self.create_new_piece()  # Créer la première pièce de Tetris
        self.game_running = True  # Booléen pour vérifier si le jeu est en cours d'exécution
        self.drop_speed = 500  # Vitesse de chute des pièces
        self.run_game()  # Démarrer la boucle du jeu
        
    def bind_keys(self):
        # Liez les touches fléchées et la touche 'r' pour contrôler les pièces de Tetris.
        root.bind("<Left>", self.move_left)
        root.bind("<Right>", self.move_right)
        root.bind("<Down>", self.move_down)
        root.bind("r", self.rotate_piece)
        
    def move_left(self, event):
        # Déplacer la pièce actuelle vers la gauche
        self.current_x -= 1
        if self.check_collision():
            self.current_x += 1  # Revenir sur le mouvement s'il provoque une collision
        self.update()
        
    def move_right(self, event):
        # Déplacer la pièce actuelle vers la droite
        self.current_x += 1
        if self.check_collision():
            self.current_x -= 1  # Revenir sur le mouvement s'il provoque une collision
        self.update()
        
    def move_down(self, event):
        # Accélérer la tombée de spièces
        self.move_piece_down()
        self.update()
        
    def rotate_piece(self, event):
        # Rotation de la pièce en cours
        self.current_piece = [list(reversed(col)) for col in zip(*self.current_piece)]
        if self.check_collision():
            self.current_piece = [list(col) for col in zip(*reversed(self.current_piece))]  # Inverser la rotation si elle provoque une collision
        self.update()
        
    def create_new_piece(self):
        # Créer une nouvelle pièce aléatoire de Tetris
        self.current_piece = random.choice(self.shapes)
        self.current_x = cols // 2 - len(self.current_piece[0]) // 2
        self.current_y = 0
        if self.check_collision():
            self.game_running = False  # Stopper le mouvement des pièces lorsqu'il y a collision
            self.show_game_over()
            
    def run_game(self):
        # Boucle principale du jeu
        if self.game_running:
            self.update()
            root.after(self.drop_speed, self.run_game)  # Répéter la boucle après 'drop_speed' millisecondes
            
    def check_collision(self):
        # Vérifier si la pièce en cours entre en collision avec le fond ou d'autres pièces
        for i, row in enumerate(self.current_piece):
            for j, val in enumerate(row):
                if val:
                    if (self.current_y + i >= rows or self.current_x + j < 0 or
                        self.current_x + j >= cols or self.grid[self.current_y + i][self.current_x + j]):
                        return True
        return False
    
    def add_piece_to_grid(self):
        # Ajouter la pièce actuelle à la grille
        for i, row in enumerate(self.current_piece):
            for j, val in enumerate(row):
                if val:
                    self.grid[self.current_y + i][self.current_x + j] = 1
                    
    def check_lines(self):
        # Vérifier et supprimer les lignes pleines de la grille
        new_grid = [row for row in self.grid if not all(cell for cell in row)]
        lines_cleared = rows - len(new_grid)
        self.grid = [[0] * cols for _ in range(lines_cleared)] + new_grid
        
    def move_piece_down(self):
        # Déplacer la pièce actuelle vers le bas
        self.current_y += 1
        if self.check_collision():
            self.current_y -= 1
            self.add_piece_to_grid()
            self.check_lines()
            self.create_new_piece()
            if self.check_collision():
                self.game_running = False  # Mettre fin à la partie si la nouvelle pièce entre immédiatement en collision.
                self.show_game_over()
                
    def draw_grid(self):
        # Dessinez la grille et les pièces verrouillées
        for i in range(rows):
            for j in range(cols):
                x1 = j * cell_size
                y1 = i * cell_size
                color = "blue" if self.grid[i][j] else "white"
                self.canvas.create_rectangle(x1, y1, x1 + cell_size, y1 + cell_size, fill=color, outline="gray")
                
    def draw_piece(self):
        # Dessinez la pièce tombante actuelle
        for i, row in enumerate(self.current_piece):
            for j, val in enumerate(row):
                if val:
                    x, y = (self.current_x + j) * cell_size, (self.current_y + i) * cell_size
                    self.canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill="blue", outline="gray")
                    
    def update(self):
        # Mettre à jour le canevas avec l'état actuel du jeu
        self.canvas.delete("all")
        self.draw_grid()
        self.draw_piece()
        self.move_piece_down()
        
    def show_game_over(self):
        # Affichage du message "Game Over
        self.canvas.create_text(cell_size*cols//2, cell_size*rows//2, text="Game Over", fill="red", font=("Helvetica", 24))
        
        
# Instanciation et démarrage de la boucle de jeu
game = Tetris()
root.mainloop()