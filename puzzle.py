from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    #A is either Knave or Knight, but cannot be both (exclusive OR)
    Or (And (AKnave, Not (AKnight)), And (Not (AKnave), AKnight)),  
    
    #If A's statement that he is both Knave & Knight is false, then A is a Knave
    Implication(Not(And(AKnave, AKnight)),AKnave) 
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    #A is either Knave or Knight, but cannot be both (exclusive OR)
    Or (And (AKnave, Not (AKnight)), And (Not (AKnave), AKnight)),  
    
    #B is either Knave or Knight, but cannot be both (exclusive OR)
    Or (And (BKnave, Not (BKnight)), And (Not (BKnave), BKnight)),  
    
    #If A is Knave (i.e. He is dishonest), then his statement that both A and B is Knave is false
    Implication (AKnave, Not(And(AKnave, BKnave))),
    
    #If A is a Knight (i.e. He is telling the truth), then it implies that A is a Knave and B is a Knave
    Implication (AKnight, And (AKnave, BKnave))
    
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    #A is either Knave or Knight, but cannot be both (exclusive OR)
    Or (And (AKnave, Not (AKnight)), And (Not (AKnave), AKnight)),  
    
    #B is either Knave or Knight, but cannot be both (exclusive OR)
    Or (And (BKnave, Not (BKnight)), And (Not (BKnave), BKnight)),  
    
    #If A is a Knight then the statement that both are same kind is true i.e both are Knight or both are Knave
    Implication (AKnight, Or (And (AKnave, BKnave), And (AKnight, BKnight))),
    
    #If A is a Knave then the statement that both are same kind is false
    # i.e. either A is Knight and B is Knave or A is Knave and B is Knight
    Implication (AKnave, Or (And(AKnave, BKnight), And (AKnight, BKnave))),
    
    #If B is Knight, then B's statement that both are different kind is true
    # i.e. either A is Knight and B is Knave or A is Knave and B is Knight
    Implication (BKnight, Or (And (AKnave, BKnight), And (AKnight, BKnave))),
    
    #If B is Knave, then B's statement that both are different is false, i.e. both are Knight or both are Knave
    Implication (BKnave, Or (And(AKnave, BKnight), And (AKnight, BKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    #A is either Knave or Knight, but cannot be both (exclusive OR)
    Or (And (AKnave, Not (AKnight)), And (Not (AKnave), AKnight)),  
    
    #B is either Knave or Knight, but cannot be both (exclusive OR)
    Or (And (BKnave, Not (BKnight)), And (Not (BKnave), BKnight)),  
    
    #C is either Knave or Knight, but cannot be both (exclusive OR)
    Or (And (CKnave, Not (CKnight)), And (Not (CKnave), CKnight)),  
    
    #If A is a Knight then A's statement that either A is a Knight or A is a Knave is true
    Implication (AKnight, Or (And (AKnave, Not (AKnight)), And (Not (AKnave), AKnight))),
    
    #If A is a Knave then A's statement that either A is a Knight or A is a Knave is false
    Implication (AKnave, Not(Or (And (AKnave, Not (AKnight)), And (Not (AKnave), AKnight)))),
    
    #If B is a knight then B's statement that "A said 'I am a knave'" is true
    # However if A is a Knight, then his statement that I am a knave is true i.e. A is Knave
    # And if A is a Knave then his statement that "I am a knave" is false i.e. A is Knight
    Implication (BKnight, And(Implication (AKnight, AKnave), Implication (AKnave, AKnight))),
    
    #If B is a Knight, his statement that C is a Knave is true
    Implication (BKnight, CKnave),
    
    #If B is a Knave, his statement that C is a Knave is false
    Implication (BKnave, CKnight),
    
    #If C is a Knight then the statement "A is a knight" is true
    Implication (CKnight, AKnight),
    
    #If C is a Knave then the statement "A is a knight" is false i.e. A is a knave
    Implication (CKnave, AKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
