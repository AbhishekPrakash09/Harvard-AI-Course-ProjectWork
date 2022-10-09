import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    
    files_contents_dict = dict()
    
    for filename in os.listdir(directory):
        
        filepath = os.path.join(directory, filename)
        
        file = open(filepath, 'r', encoding="utf8",)
        file_content = file.read()
        file.close
        
        files_contents_dict[filename] = file_content
    
    return files_contents_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    
    document = document.lower()
    
    document = document.translate(str.maketrans('','', string.punctuation))
    
    words = nltk.word_tokenize(document)
    
    stop_words = nltk.corpus.stopwords.words("english")
    
    pruned_words = [word for word in words if word not in stop_words]
    
    return pruned_words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    
    total_documents = len(documents)
    words_idfs = dict()
    
    for document in documents:
        words = documents[document]
        
        for word in words:
            
            if not word in words_idfs:
                
                num_docs_containing_word = 0
                
                for document_1 in documents:
                    
                    if word in documents[document_1]:
                        num_docs_containing_word += 1
                    
                words_idfs[word] = math.log(total_documents / num_docs_containing_word) 
            
    return words_idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    
    #Dictionary to hold the sum tf-idf score of each filename
    score_dict = dict()
    
    #Initializing dicitonary with all the filenames 
    for filename in files: 
        
        score_dict[filename] = 0
    
    for word in query:
        
        for filename in files:
            
            tf = (files[filename]).count(word)
            if(tf != 0):
                idf = idfs[word]
                tf_idf = tf * idf
                score_dict[filename] = score_dict[filename] + tf_idf
            
    sorted_list_filenames = []
    
    #sorting the dictionary by values (increasing order)
    score_dict = dict(sorted(score_dict.items(), key = lambda item: item[1]))
    
    list_filenames = list(score_dict.keys())
    
    list_filenames.reverse() 
    
    return list_filenames[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    #Dictionary to hold the sum tf-idf score of each filename
    score_dict = dict()
    
    #Initializing dicitonary with all the filenames 
    for sentence_name in sentences: 
        
        score_dict[sentence_name] = 0
    
    for word in query:
        
        for sentence_name in sentences:
            
            tf = (sentences[sentence_name]).count(word)
            
            if(tf != 0):
                
                idf = idfs[word]
                score_dict[sentence_name] = score_dict[sentence_name] + idf
            
    
    #sorting the dictionary by values (increasing order)
    score_dict = dict(sorted(score_dict.items(), key = lambda item: item[1]))
    
    list_sentence_names = list(score_dict.keys())
    list_sentence_names.reverse() 
    
    """
    This list_sentence_names is sorted as per sum of idf's
    The code below further sorts them in order of term density in case there is a tie
    """
    
    new_list_sentence_names = []
    
    #initializing sentence score to an arbitrary high (infinite) value
    #this sentence score holds the idf value
    sentence_score = 10000
    
    #This dictionary contains sentence_name along with its query term density
    temp_dict_sentences = dict()
    
    for sentence_name in list_sentence_names:
        
        if score_dict[sentence_name] < sentence_score:
            
            #setting the sentence score to the idf value of current sentence
            sentence_score = score_dict[sentence_name]
            
            """
            If the dictionary is empty, then populate it with the current sentence name 
            and its query term density, else clean up the dictionary by adding its keys
            to the new_list_sentence_names sorted as per decreasing order of its query
            term density and then populate the dictionary with current sentence and its
            query term density
            """
            if temp_dict_sentences == dict():
                
                temp_dict_sentences[sentence_name] = query_term_density(query, sentences[sentence_name])
            
            else:
                temp_dict_sentences = dict(sorted(temp_dict_sentences.items(), key = lambda item: item[1]))
                temp_list_sentence_names = list(temp_dict_sentences.keys())
                temp_list_sentence_names.reverse()
                new_list_sentence_names.extend(temp_list_sentence_names)
                
                temp_dict_sentences = dict()
                temp_dict_sentences[sentence_name] = query_term_density(query, sentences[sentence_name])
        else: 
            """
            If the idf_score of current sentence is same as idf_score of previous sentence(s)
            then add the current sentence and its query term density to temp_dict_sentences
            This will later be appended to new_list_sentence_names in decreasing order of
            query_term_density
            """
            temp_dict_sentences[sentence_name] = query_term_density(query, sentences[sentence_name])
    
    """
    If after the interation, there are still some sentences left in the dictionary,
    sort them according to their query term density and add them to the new_list_sentence_names
    """
    if not temp_dict_sentences == dict():
        
        temp_dict_sentences = dict(sorted(temp_dict_sentences.items(), key = lambda item: item[1]))
        temp_list_sentence_names = list(temp_dict_sentences.keys())
        temp_list_sentence_names.reverse()
        new_list_sentence_names.extend(temp_list_sentence_names)
                
    
    return new_list_sentence_names[:n]


def query_term_density(query, sentence):
    
    term_count = 0
    
    for word in query:
        if word in sentence:
            term_count += 1
    
    term_density = term_count/len(sentence)
        
    return term_density

if __name__ == "__main__":
    main()
