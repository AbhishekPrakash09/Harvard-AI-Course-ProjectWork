import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])
    
    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }
    
    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    
    probability_table_keys = people.keys()
    
    probability_table_values = []
    
    for person in people:
        
        probability_table_values.append(0)
        
    probability_table = dict(zip(probability_table_keys, probability_table_values))
    
    for person in people:
        
        #If the person's both parents are not known
        if (Father (people, person) == None) and (Mother (people, person) == None):
            
            probability_table[person] = probability_if_no_parent_known(person, one_gene, two_genes, have_trait)
        
        #If person's both parents are known    
        elif (Father(people, person) != None) and (Mother(people, person) !=None):
            
            probability_table[person] = probability_if_both_parents_known(people, person, one_gene, two_genes, have_trait)
        
        #If person's only one parent is known
        else :
            
            probability_table[person] = probability_person_one_parent(people, person, one_gene, two_genes, have_trait)
    
    J_Probability = 1
    
    for probability in list (probability_table.values()):
        
        J_Probability = J_Probability * probability
    
    return J_Probability    
    

def probability_if_both_parents_known (people, person, one_gene, two_genes, have_trait):
    """
    Computing the probability of person getting one_gene, or two_genes or no_gene and
    exhibiting (not exhibiting) the trait when both parents are known
    """
    
    father = Father(people, person)
    mother = Mother(people, person)
    
    num_genes, num_father_genes, num_mother_genes = 0, 0, 0
    
    if (person in one_gene):
        num_genes = 1
    elif (person in two_genes):
        num_genes = 2
        
    if (father in one_gene):
        num_father_genes = 1
    elif (father in two_genes):
        num_father_genes = 2
    
    if (mother in one_gene):
        num_mother_genes = 1
    elif (mother in two_genes):
        num_mother_genes = 2    
    
    #computing the probability of getting the gene from each of 
    # the parents given the number of genes present in the parent
    P_Mother = probability_gene_from_parent(mother, num_mother_genes)
    P_Father = probability_gene_from_parent(father, num_father_genes)
    
    has_trait = person in have_trait
    
    #person didn't get genes either from father or mother
    if(num_genes == 0):
        
        return (1- P_Mother) * (1- P_Father) * PROBS["trait"][num_genes][has_trait]
    
    #person got genes either from father and not from mother 
    # or from mother and not from father
    elif (num_genes ==1):
        return ((1-P_Mother) * P_Father + (1-P_Father) * P_Mother)* PROBS["trait"][num_genes][has_trait]
    
    #person got genes from both father and mother
    elif (num_genes == 2):
        return P_Mother * P_Father * PROBS["trait"][num_genes][has_trait]
        

"""
This function calculates the probability of getting the gene from a parent, given the
number of such genes the parent has
"""
def probability_gene_from_parent(parent, num_parent_genes):
    
    if(num_parent_genes == 0):
        return PROBS['mutation']
    elif (num_parent_genes == 1):
        return 0.5
    elif (num_parent_genes == 2):
        return 1 - PROBS['mutation']
    
        
def probability_person_one_parent (people, person, one_gene, two_genes, have_trait):
    
    raise NotImplementedError


def probability_if_no_parent_known (person, one_gene, two_genes, have_trait):
    
    num_genes = 0
    
    if person in one_gene:
        
        num_genes = 1       
    
    elif person in two_genes :
    
        num_genes = 2
        
    has_trait = person in have_trait
    
    return PROBS["gene"][num_genes] * PROBS["trait"][num_genes][has_trait]
                    

#returns the name of father, None if there's none
def Father (people, person):
    
    return people[person]['father']

#returns the name of mother, None if there's none
def Mother (people, person):
    
    return people [person]['mother']

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    
    names = set(probabilities)
    
    for name in names:
        
        #Update the 'gene' distributions
        if name in one_gene:
            probabilities[name]['gene'][1] = probabilities[name]['gene'][1] + p
        elif name in two_genes:
            probabilities[name]['gene'][2] = probabilities[name]['gene'][2]+ p
        else:
            probabilities[name]['gene'][0] = probabilities[name]['gene'][0] + p
        
        
        if name in have_trait:
            probabilities[name]['trait'][True] = probabilities[name]['trait'][True] + p 
            
        else:
            probabilities[name]['trait'][False] = probabilities[name]['trait'][False] + p 
    


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    names = set(probabilities)
    
    for name in names:
        
        p_one_gene = probabilities[name]['gene'][1]
        p_two_genes = probabilities[name]['gene'][2]
        p_no_genes = probabilities[name]['gene'][0]
        
        sum_probability = p_one_gene + p_two_genes + p_no_genes
        
        probabilities[name]['gene'][1] = p_one_gene / sum_probability
        probabilities[name]['gene'][2] = p_two_genes / sum_probability
        probabilities[name]['gene'][0] = p_no_genes / sum_probability
        
        p_has_trait = probabilities[name]['trait'][True]
        p_no_trait = probabilities[name]['trait'][False]
        
        sum_probability = p_has_trait + p_no_trait
        probabilities[name]['trait'][True] = p_has_trait / sum_probability
        probabilities[name]['trait'][False] = p_no_trait / sum_probability
    


if __name__ == "__main__":
    main()
