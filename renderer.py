"""
Nom : Cherkaoui
Prénom : Jawad
Matricule : 576517
"""

# importation des modules :
from pos2d import Pos2D
from grid import Grid
###########################


class GridRenderer:
    def __init__(self, grid: Grid) -> None:
        self.grid = grid.grid
        self.width, self.height = grid.width, grid.height
        self.full_lines, self.line1, self.line2 = '', '', ''
        # bord supérieur de la grille :
        self.draw_border()
        # affichage centrale :
        for y in range(1, self.height):
            for x in range(self.width):
                node = self.grid[x][y]
                if not x:   # bord de gauche
                    self.line1 += f"{'├───' if not node.up else '│   '}"
                else:   # caractères du milieu + bord de droite
                    char = self.detect_character(Pos2D(x, y))
                    if char[1]:
                        self.line1 += (char[0] + f"{'┤' if x == self.width - 1 else ''}")
                    else:
                        self.line1 += (char[0] + f"{'│' if x == self.width - 1 else ''}")
                if 2:   # entre case
                    self.line2 += (f"{'│' if not node.left else ' '}" + "   " + f"{'│' if x == self.width - 1 else ''}")
            self.sum_full_lines()
        # bord inférieur de la grille :
        self.draw_border(1)


    def detect_character(self, pos: Pos2D) -> tuple[str, bool]:
        x, y = pos.x, pos.y
        node, node_ul = self.grid[x][y], self.grid[x - 1][y - 1]
        # (caractères + boolean) -> True = présence de tirets -> False = vide
        if not node.up and not node.left and node_ul.down and node_ul.right:
            return '┌───', True
        elif node.up and not node.left and not node_ul.down and node_ul.right:
            return '┐   ', False
        elif not node.up and node.left and node_ul.down and not node_ul.right:
            return '└───', True
        elif node.up and node.left and not node_ul.down and not node_ul.right:
            return '┘   ', False
        elif not node.up and not node.left and not node_ul.down and node_ul.right:
            return '┬───', True
        elif not node.up and node.left and not node_ul.down and not node_ul.right:
            return '┴───', True
        elif not node.up and not node.left and node_ul.down and not node_ul.right:
            return '├───', True
        elif node.up and not node.left and not node_ul.down and not node_ul.right:
            return '┤   ', False
        elif not node.up and not node.left and not node_ul.down and not node_ul.right:
            return '┼───', True
        elif node.up and node.left and node_ul.down and not node_ul.right:
            return '│   ', False
        elif node.up and not node.left and node_ul.down and node_ul.right:
            return '│   ', False
        elif node.up and not node.left and node_ul.down and not node_ul.right:
            return '│   ', False
        elif not node.up and node.left and not node_ul.down and node_ul.right:
            return '────', True
        elif not node.up and node.left and node_ul.down and node_ul.right:
            return '────', True
        else:
            return '    ', False


    def sum_full_lines(self) -> None:
        self.full_lines += (self.line1 + self.line2)
        self.line1, self.line2 = '', ''


    def draw_border(self, cas: int = 0) -> None:
        item = ('┌', '┬', '┐') if not cas else ('└', '┴', '┘')  # selection des caractères 
        height = 0 if not cas else self.height - 1  # selection d'une ligne (debut ou fin)
        for i in range(self.width):
            node = self.grid[i][height]
            if i == 0:  # coin gauche
                self.line1 += (item[0] + '───')
            else:   # caractères du milieu + coin droit
                self.line1 += (f"{item[1] if not node.left else '─'}" + "───" + f"{item[2] if i == self.width - 1 else ''}")
            if not cas:  # entre case
                self.line2 += (f"{'│' if not node.left else ' '}" + "   " + f"{'│' if i == self.width - 1 else ''}")
        self.sum_full_lines()


    def show(self) -> None:
        i = 0
        char_x, char_y = ((self.width * 5) - (self.width - 1)), ((self.height * 3) - (self.height - 1))
        print()
        for _ in range(char_y):
            for _ in range(char_x):
                print(self.full_lines[i], end='')
                i += 1
            print()