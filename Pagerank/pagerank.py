import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    print(len(sys.argv))
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
    
    #Put all pages in a list
    
    probabilities = dict()
    
    
    for a_page in corpus[page]:
        probabilities[a_page] = 0
    
    if len(corpus[page]) > 0:
        prob_click = damping_factor / len(corpus[page])
        prob_random = (1-damping_factor) / len(corpus)
        
        for a_page in corpus[page]:
            probabilities[a_page] = prob_click + prob_random
        
        # add to the main page
        probabilities[page] = prob_random
    else:
        prob_random_page = 1 / len(corpus)
        for a_page in corpus:
            probabilities[a_page] = prob_random_page
    
    return probabilities
    
    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.

    """
    total_count = 0
    
    
    page_rank = dict()
    
    page_rank = {key: 0 for key in corpus}
    
    # first page is random 
    
    current_page = random.choice(list(corpus.keys()))
    
    # add count and page count to the random first page
    
    total_count += 1
    
    page_rank[current_page] += 1
    
    # probability of second page
    
    for i in range(n-1):
    # get transition model
        probabilities = transition_model(corpus, current_page, damping_factor)
    
    # pick random based on weights
        current_page = random.choices(list(probabilities.keys()), weights = probabilities.values(), k=1)[0]
        
        # add 1 count to the current pages value
        page_rank[current_page] += 1
        total_count += 1
    
    for page in page_rank:
        page_rank[page] = page_rank[page]/total_count
    
    return page_rank
    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    posibilities = dict()
    
    n = len(corpus)
    
    for page in corpus:
        posibilities[page] = 1/n
    
    
    
    running = True
    
    while running:
        count_margin = 0
        new_ranks = {}
        
        for p in posibilities:
            summation = 0
            
            
            old_PR = posibilities[p]
            
            for page in corpus:
                if p in corpus[page]:
                    num_links = len(corpus[page])
                    summation += posibilities[page]/num_links
                elif not corpus[page]:
                    summation += posibilities[page] / n
                    
            new_rank= (1 - damping_factor) / n + damping_factor * summation
            new_ranks[p] = new_rank
            
            if abs(posibilities[p]- new_rank) < 0.001:
                count_margin += 1
        
        posibilities = new_ranks
        
        if count_margin == len(corpus):
            running = False
        
    return posibilities
    


if __name__ == "__main__":
    main()
