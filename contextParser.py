from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_best_match(input_sentence, sentence_set):
    vectorizer = CountVectorizer().fit_transform([input_sentence] + sentence_set)
    vectors = vectorizer.toarray()
    similarities = cosine_similarity(vectors)

    # Similarities[0] contains the similarity scores between the input sentence and each sentence in the set
    best_match_index = similarities[0][1:].argmax()
    best_match = sentence_set[best_match_index]

    return best_match

