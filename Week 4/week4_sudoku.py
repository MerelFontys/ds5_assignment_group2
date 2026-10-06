import tkinter as tk


'''Maak een eigen datatype aan genaamd Sudoku'''
class Sudoku:

    def __init__(self, grid): 
        self.grid = grid  # Maakt een 9x9 lege grid 


    '''Check of een waarde op een bepaalde positie geldig is.'''
    def is_valid_move(self, row, col, value):
        '''Checkt of een waarde in die rij mag'''
        if value in self.grid[row]: #staat bepaalde waarde al in die rij
            return False #Zo ja geef error als er op check geduwd wordt 

        '''Checkt of die waarde in die kolom mag'''
        for r in range(9):
            if self.grid[r][col] == value: #staat bepaalde waarde al in kolom 
                return False #geef error als er op check geklikt word 

        '''Checkt of die waarde in de subgrid (het kleine 3x3 vierkantje) mag'''

        start_row = (row // 3) * 3 #// deelt en kapt af dus zo maak je 3 blokken die hetzelfde antwoord geven, 0,1,2 geven als antwoord 0. Floats zijn hier nutteloos daarom ints 
        start_col = (col // 3) * 3
        for r in range(start_row, start_row + 3): #Loopt over alle rijen heen 
            for c in range(start_col, start_col + 3): #Loopt over alle kolommen 
                #komt 9x aan met (0,0)(0,1)(0,2)(1,0)(1,1)(1,2)(2,0)(2,1)(2,2)
                if self.grid[r][c] == value: #Als bepaalde waarde al in die 3x3 staat dan werkt dit if statement
                    return False

        return True

    def is_complete(self):
        '''Checken of er nog ergens lege waardes staan'''
        for row in range(9):
            for col in range(9): 
                #komt hier dus 81 keer aan en checkt voor elk vakje of die 0 is
                if self.grid[row][col] == 0:
                    return False
        return True
    
    '''Check of de volledige sudoku volledig correct is'''

    def is_correct_solution(self):
        
        '''Checkt of een volledige rij klopt'''
        for row in range(9):
            if sorted(self.grid[row]) != list(range(1, 10)): #sorted(self.grid[row]) geeft als het goed is een lijst met waardes van 1tm9 en als die dus niet gelijk is aan die lijst dan gaat er iets fout
                return False

        '''Checkt of een volledige kolom klopt'''
        for col in range(9):
            column = [self.grid[row][col] for row in range(9)] #Maakt list aan van alle nummers die in dezelfde kolom staan 
            if sorted(column) != list(range(1, 10)):#zelfde als bij rijen
                return False

        '''Checkt of een 3x3 blok volledig klopt'''
        for block_row in range(0, 9, 3): 
            for block_col in range(0, 9, 3):
                block = []
                for r in range(block_row, block_row + 3): #doet bv in de 1e keer 0, 1 en 2 en de tweede keer doet het 3, 4 en 5. Dit zorgt ervoor dat het juiste blok gekozen wordt 
                    for c in range(block_col, block_col + 3): #Hetzelfde als hierboven maar dan voor de kolommen
                        block.append(self.grid[r][c]) #Vult de lijst "block" met de waardes uit het 3x3 block
                if sorted(block) != list(range(1, 10)): #Hetzelfde als bij rijen en kolommen hierboven
                    return False

        return True #Als uit alle 3 (rijen, kolommen of 3x3 blokken) geen False komt dan is de oplossing correct 

    '''Functie aanmaken om een hint te geven'''
    def find_hint(self):
        '''Zoek een cel waar maar één waarde mogelijk is.'''
        for row in range(9):
            for col in range(9): #gaat over alle 81 vakjes heen 
                if self.grid[row][col] == 0: #gaat alleen kijken waar de waardes nog niet ingevuld zijn of een daarvan ingevuld kan worden 
                    possible = [v for v in range(1, 10) if self.is_valid_move(row, col, v)] #Gebruikt de functie is_valid_move om te kijken of iets een valid move is en test dit voor alle mogelijke waardes 
                    if len(possible) == 1: #Alleen als er maar één waarde mogelijk is (dan pas kun je iets verzekeren te kloppen)
                        return row, col, possible[0] #De functie moet geven de plek waar het getal moet komen en welke waarde (de 0de index van de lijst genaamd 'possible')
        return None #geen hint gevonden, als er een startpositie is met één unieke oplosing betekent dit dat er eerder een fout gemaakt is 

    def solve(self):
        '''Als Sudoku af is een test of deze correct is ingevuld'''
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    for value in range(1, 10): 
                        if self.is_valid_move(row, col, value):
                            self.grid[row][col] = value #gaat voor elke rij, kolom en 3x3 af of deze kloppen
                            if self.solve():
                                return True
                            self.grid[row][col] = 0
                    return False
        return True


'''Popupje voor Sudoku op te lossen'''

class SudokuGUI:
    

    def __init__(self, root, puzzle):
        self.root = root
        self.root.title("Sudoku")
        self.sudoku = Sudoku(puzzle)

        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.build_grid()
        self.build_buttons()

    def build_grid(self):
        """Maak het 9x9 invoerveld."""
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(self.root, width=2, font=("Arial", 18), justify="center")
                entry.grid(row=row, column=col, padx=2, pady=2)

                if self.sudoku.grid[row][col] != 0:
                    entry.insert(0, str(self.sudoku.grid[row][col]))
                    entry.config(state="disabled")

                self.cells[row][col] = entry

    def build_buttons(self):
        """Knoppen voor hint, solve en check."""
        hint_btn = tk.Button(self.root, text="Hint", command=self.give_hint)
        hint_btn.grid(row=10, column=0, columnspan=3, pady=10)

        solve_btn = tk.Button(self.root, text="Solve", command=self.solve_puzzle)
        solve_btn.grid(row=10, column=3, columnspan=3, pady=10)

        check_btn = tk.Button(self.root, text="Check", command=self.check_solution)
        check_btn.grid(row=10, column=6, columnspan=3, pady=10)

    def give_hint(self):
        """Laat een hint zien."""
        hint = self.sudoku.find_hint()
        if hint is None:
            tk.messagebox.showinfo("Hint", "Geen hints beschikbaar.")
            return

        row, col, value = hint
        self.cells[row][col].delete(0, tk.END)
        self.cells[row][col].insert(0, str(value))
        self.sudoku.grid[row][col] = value

    def solve_puzzle(self):
        """Los de puzzel op en update de GUI."""
        if self.sudoku.solve():
            for row in range(9):
                for col in range(9):
                    self.cells[row][col].delete(0, tk.END)
                    self.cells[row][col].insert(0, str(self.sudoku.grid[row][col]))
        else:
            tk.messagebox.showerror("Fout", "Puzzel kan niet worden opgelost.")

    def check_solution(self):
        """Controleer of de Sudoku correct is ingevuld."""

        # Update model vanuit GUI
        for row in range(9): #Voor elke rij testen  
            for col in range(9): # Voor elke kolom testen 
                value = self.cells[row][col].get()
                if value.isdigit():
                    self.sudoku.grid[row][col] = int(value)
                else:
                    self.sudoku.grid[row][col] = 0
        '''Tekst die displayed als sudoku correct/incorrect is '''
        if self.sudoku.is_correct_solution():
            tk.messagebox.showinfo("Sudoku", "Sudoku correct opgelost!")
        else:
            tk.messagebox.showerror("Sudoku", "De Sudoku is nog niet correct.")




if __name__ == "__main__":
    # Puzzel die opgelost moet worden elke 0 is een leeg vakje 
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    root = tk.Tk()
    app = SudokuGUI(root, puzzle)
    root.mainloop()

