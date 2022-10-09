import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        for var in self.domains:
            length = var.length
            
            for word in self.domains[var].copy():
                if len(word) != length:
                    self.domains[var].remove(word)
        

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        neighbours_x = self.crossword.neighbors(x)
        
        revised = False
        
        if y not in neighbours_x:
            return revised
        
        overlap_x_y = self.crossword.overlaps[(x, y)]
        
        domain_x = self.domains[x]
        domain_y = self.domains[y]
        
        revised_x = set()
        
        for word_x in domain_x:
            for word_y in domain_y:
                if word_x[overlap_x_y[0]] == word_y[overlap_x_y[1]]:
                    revised_x.add(word_x)
                    break
                
        if (revised_x < domain_x):
            revised = True
            self.domains[x] = revised_x
    
        return revised
        
        
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        
        queue = list(self.crossword.overlaps)
        
        if (arcs != None):
            queue = arcs
                
        while len(queue) != 0:
            #DEQUEUE (queue)
            (variable_x, variable_y) = queue [0]
            queue = queue[1:]
            
            if self.revise(variable_x, variable_y):
                if len(self.domains[variable_x]) == 0:
                    return False
                for variable_z in self.crossword.neighbors(variable_x) - {variable_y}:
                    #ENQUEUE (queue, (z, x))
                    queue.append((variable_z, variable_x))
        
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        
        if set(assignment) < set (self.crossword.variables):
            return False
        
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        
        variables = set(assignment)
        
        
        for variable_x in variables:
            #Checking for length consistency
            if variable_x.length != len(assignment[variable_x]):
                return False
            
            
            for variable_y in variables - {variable_x}:
                
                word_x = assignment[variable_x]
                word_y = assignment[variable_y]
                
                #Checking for distinct values
                if (word_x == word_y):
                    return False
                
                #Checking for conflicting characters
                if (variable_x, variable_y) in self.crossword.overlaps:
                    
                    overlap_x_y = self.crossword.overlaps[(variable_x, variable_y)]
                    
                    if overlap_x_y != None:
                    
                        if word_x[overlap_x_y[0]] != word_y[overlap_x_y[1]] :
                        
                            return False
                    
        return True
        
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        
        """
        *** IMPORTANT ASSUMPTION: 
                The variable var is an unassigned variable, it SHOULD NOT 
                be part of the dictionary assignment that is being passed here***
        """
        domain_values = self.domains[var]
        
        neighbours = self.crossword.neighbors(var)
        
        #Dictionary that keeps a count of number of neighbouring domain values that 
        # get removed if a given variable is assigned
        rule_out_counter = dict()
        
        
        for word in domain_values:
            
            #Creating a test_assignment with the given word in the domain
            #to check if assignment is consistent
            test_assignment = assignment.copy()
            
            test_assignment[var] = word
            
            #If the adding the current word to assignment makes it inconsistent, then ignore the current word
            if(self.consistent(test_assignment) != True):
                continue
            
            #Initializing the dictionary with counter = 0 for the given word in variable's domains
            rule_out_counter[word] = 0
                        
                
            for neighbour in neighbours:
                
                #If the neighbour has already been assigned a value, ignore it
                if neighbour in assignment:
                    continue 
                
                neighbour_domain = self.domains[neighbour]
                
                for neighbour_word in neighbour_domain : 
                    
                    test_assignment_neighbour = test_assignment.copy()
                    
                    test_assignment_neighbour[neighbour] = neighbour_word
                    
                    #If adding the word from the neighbour's domain makes the assignment 
                    # inconsistent, then increment the number of rule outs from the present
                    # counter by 1
                    if self.consistent(test_assignment_neighbour) != True:
                        
                        rule_out_counter[word] = rule_out_counter[word] + 1
        
        
        sorted_counters = sorted(rule_out_counter.values())
        sorted_domain_values = []
        
        
        for counter in sorted_counters:
            
            for domain_value in list(rule_out_counter):
            
                if (rule_out_counter[domain_value] == counter) and (not domain_value in sorted_domain_values) :
                    
                    sorted_domain_values.append(domain_value)
        
        
        return sorted_domain_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        #The dictionary var_dict_degree is used to add least domain length heuristic
        var_dict_domain_length = dict()
        
        for var in self.crossword.variables:
            if not var in assignment:
                var_dict_domain_length[var] = len(self.domains[var])
        
        min_domain_length = min(var_dict_domain_length.values())
        
        #The dictionary var_dict_degree is used to add degree heuristic
        var_dict_degree = dict()
        
        for var in list(var_dict_domain_length):
                
            if(var_dict_domain_length[var] == min_domain_length):
                var_dict_degree[var] = len(self.crossword.neighbors(var))
        
        max_degree = max(var_dict_degree.values())
        
        #Return the variable with minimum domain length and maximum degree
        for var in list(var_dict_degree):
            if var_dict_degree[var] == max_degree: return var
       

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        if self.assignment_complete(assignment): return assignment
        
        var = self.select_unassigned_variable(assignment)
        
        for value in self.order_domain_values(var, assignment):
            
            assignment[var] = value
            
            if self.consistent(assignment):
                
                result = self.backtrack(assignment)
                
                if result != None:
                    return result
        
            #If the assignment is not consistent or backtrack doesn't give result
            # remove the assignment
            assignment.pop[var]
            
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
