import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        
        """
        If the number of cells is equal to the count of the mines,
        then all cells are mines. 
        
        Else, we do not have information of which cells are mines. 
        Hence this should return an empty set if number of cells is 
        not equal to count of mines
        """
        
        if len(self.cells) == self.count:
            return self.cells.copy()
        
        return {}
            

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        
        """
        If the number of mines is equal to zero, then we know that all cells
        in the sentence are safe
        
        Else, we do not have a definitive information and we should return
        an empty set
        """
        
        if self.count == 0:
            return self.cells.copy()
        
        
        return {}

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        
        """
        As per specification, if cell is one of the cells in the sentence
        mark mine should remove the mine and also do something to logically 
        represent the information.
        
        So if I am removing the cell, I should also remove the count of mines
        represented by the sentence
        
        The function should do nothing if cell is not a part of the sentence
        """
        
        if(cell in self.cells):
            self.cells.remove(cell)
            self.count = self.count -1
            
            

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        
        """
        As per specification, if the given cell is one of the cells in the 
        sentence mark mine should remove the mine and also do something to 
        logically represent the information.
        
        So if I am removing the cell, the count of mines in the sentence
        should remain the same because the cell does not have a mine
        
        The function should do nothing if cell is not part of the sentence
        """
        if(cell in self.cells):
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        
        """
        Mark the cell as a move that has been made
        Fulfills requirement #1 for this function
        """
        self.moves_made.add(cell)
        
        """
        Marks the cell as safe in the set safes as well as 
            updates all sentences in the knowledge base
        Fulfills requirement #2 for this function
        """
        self.mark_safe(cell)
        
        """
        #Create a new knowledge piece based on the neighbours of the
        given cell and the count of the mines in the neighbourhood
        Fulfills requirement #3 for this function
        """
        
        neighbours = self.find_cell_neighbours(cell)
        
        sentence = Sentence(neighbours, count)
        self.knowledge.append(sentence)
        
        """
        Make appropriate inferences (mines & safes) that can be concluded from AI's knowledge base
        Fulfills requirement #4 for this function
        """
        self.make_primary_reductions()
        
        """
        Create new sentences based on inferences from existing sentences in AI's knowledge base
        Fulfills requirement #5 for this function
        """
        self.make_secondary_deductions()
        
        #self.print_knowledge()
    
    def make_secondary_deductions(self):
        
        deduced_knowledge = []
        
        # Compare sentences in pairs find compute information
        for sentence_1 in self.knowledge:
            for sentence_2 in self.knowledge:
                
                """
                If sentence_1 is a subset of sentence_2 then create a new_sentence
                where the new_sentence is the difference between the two
                also, count of mines will also be the difference of the two
                """
                if sentence_1.cells < sentence_2.cells :
                    new_cells = sentence_2.cells.difference(sentence_1.cells)
                    new_count = sentence_2.count - sentence_1.count
                    new_sentence = Sentence(new_cells, new_count)
                    deduced_knowledge.append(new_sentence)
            
        for sentence_1 in deduced_knowledge:
            addflag = True
            for sentence_2 in self.knowledge:
                """
                Ensuring that no duplicate sentence is added to knowledge
                """
                if(sentence_2.cells.difference(sentence_1.cells) == set()):
                    addflag = False
            if addflag == True :
                self.knowledge.append(sentence_1)
        
        
            
        #If we were able to add new knowledge through deduction
        # make basic reductions   
        if not deduced_knowledge == []:
            self.make_primary_reductions()
    
    def make_primary_reductions(self):
        """
        Function to make primary reductions on knowledge
        """
        
        remove_list = []
        
        for sentence in self.knowledge:
            """ 
            if the cells in the sentence do not have any mine
            mark all cells as safe and since the sentence is now empty
            mark the sentence to be removed 
            
            else if the cells in the sentence are all mines
            mark all cells as mines and since the sentence is now empty
            mark the sentence to be removed 
            """
            if sentence.count == 0 :
                remove_list.append(sentence)
                temp_safe_set = sentence.known_safes()
                for cell in temp_safe_set :
                    self.mark_safe(cell)
            
            elif len(sentence.cells) == sentence.count:
                remove_list.append(sentence)
                temp_mine_set = sentence.known_mines()
                for cell in temp_mine_set:
                    self.mark_mine(cell)       
            
            """
            Eliminate the known safes from the sentence
            """
            for cell in self.safes:
                sentence.mark_safe (cell)
            
            """
            Eliminate known mines from the sentence
            """
            for cell in self.mines:
                sentence.mark_mine(cell)
        
        """
        Remove sentences which are empty
        """
        for sentence in remove_list:
            self.knowledge.remove(sentence)
            
        
    def print_knowledge(self):
        
        for sentence in self.knowledge:
            print(f"{sentence.cells} = {sentence.count}")
        
        print(f"Known safes = {self.safes}")
        print(f"Known mines = {self.mines}")
    
    
    def find_cell_neighbours(self, cell):
        """
        Function to find all the neighbours of the cell
        """
        
        neighbours = set()
        
        i = cell[0]
        j = cell [1]
        
        neighbourRows = set()
        neighbourColumns = set()
        
        if i == 0:
            neighbourRows.add(i)
            neighbourRows.add(i+1)
        elif i == self.height-1 :
            neighbourRows.add(i-1)
            neighbourRows.add(i)
        else :
            neighbourRows.add(i-1)
            neighbourRows.add(i)
            neighbourRows.add(i+1)
        
        if j == 0:
            neighbourColumns.add(j)
            neighbourColumns.add(j+1)
        elif j == self.width-1 :
            neighbourColumns.add(j-1)
            neighbourColumns.add(j)
        else :
            neighbourColumns.add(j-1)
            neighbourColumns.add(j)
            neighbourColumns.add(j+1)
        
        for row in neighbourRows :
            for column in neighbourColumns :
                neighbour = (row, column)
                if neighbour == cell :
                    continue
        
                neighbours.add(neighbour)
                
        return neighbours
        

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        
        for move in self.safes:
            if not move in self.moves_made:
                return move
            
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
        moves = set()
        for i in range(self.height):
            for j in range(self.width):
                moves.add((i, j))
        
        moves = moves.difference(self.moves_made)   
        moves = moves.difference(self.mines)
        
        movesList = []     
        
        for move in moves:
            movesList.append(move)
        
        if movesList == []:
            return None
        
        randomMoveNumber = random.randint(0, len(movesList) -1)
        
        return movesList[randomMoveNumber]
