import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    pages = []
    probabilities = []
    
    total_num_pages = len(corpus)
    
    linked_pages = corpus.get(page)
    
    num_linked_pages = len(linked_pages)
    
    """
    If the current page does not have any link, all pages in the
    corpus should have equal probability. By setting the damping_factor 
    to 0, page_probability will be 1 / total_num_pages with each page
    having equal probability and total probability will be equal to 1
    """
    if(num_linked_pages == 0):
        
        damping_factor = 0
    
    for corpus_page in corpus :
        pages.append(corpus_page)
        
        page_probability = (1-damping_factor)/total_num_pages
        
        if corpus_page in linked_pages:
            
            page_probability = page_probability +  damping_factor / num_linked_pages
        
        probabilities.append(page_probability)
        
    probability_distribution = dict(zip(pages, probabilities))
    
    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    pages = []
    count = []
    
    #Putting the pages in a list for accessing through numbers
    for page in corpus:
        pages.append(page)
        count.append(0)
    
    page_rank = dict(zip(pages, count))
        
    random_starting_page_number = random.randint(0, len(corpus) -1)
    
    starting_page = pages[random_starting_page_number]
    
    model = transition_model(corpus, starting_page, damping_factor)
    
    for i in range(n):
        pages = list(model)
        probabilities = list(model.values())
        
        """
        Based on the probabilities, random.choices gives a list of pages
        In this case, the list will have have only one page as getting
        multiple pages requires one more parameter in random.choices
        function
        """
        random_pages_list = random.choices(pages, probabilities)
        
        random_page = random_pages_list[0]
        
        count = page_rank[random_page]
        
        count = count+1
        
        page_rank[random_page] = count
        
        model = transition_model(corpus, random_page, damping_factor)
    
    
    for page in page_rank:
        count = page_rank[page]
        probability = count / n
        page_rank[page] = probability
    
    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = []
    probabilities = []
    
    N = len(corpus)
    
    #Putting the pages in a list for accessing through numbers
    for page in corpus:
        pages.append(page)
        probabilities.append(1/N)
    
    page_rank_dictionary = dict(zip(pages, probabilities))
    
    """
    Loop until the difference between old rank values and new rank values <= 0.001
    """
    while(True):
        
        old_page_rank_dictionary = page_rank_dictionary.copy()
        
        #Computing updated page_rank_value for each page
        for page_i in pages:
        
            page_rank = (1-damping_factor)/N
        
            for page_j in pages:
            
                pages_linked_from_j = corpus[page_j]
            
                num_links_from_j = len(pages_linked_from_j)
            
                if page_i in pages_linked_from_j:
                
                    page_rank = page_rank + damping_factor * old_page_rank_dictionary[page_j] / num_links_from_j  
            
        
            page_rank_dictionary[page_i] = page_rank
    
        return_flag = True
        
        for page in pages:
            
            old_probability = old_page_rank_dictionary[page]
            new_probability = page_rank_dictionary[page]
            
            if abs (old_probability - new_probability) > 0.001 :
                return_flag = False
    
        """
        If the difference between page_rank_values in successive iterations
        is <= 0.001 then return the page_rank_dictionary
        """
        if return_flag == True:
            
            return page_rank_dictionary


if __name__ == "__main__":
    main()
