from nltk import tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import whoosh.index as index
from whoosh.qparser import QueryParser, OrGroup
from whoosh import scoring
import CustomScoring as scoring
from nltk.corpus import stopwords
from nltk.tag import pos_tag

def tag2pos(tag):
    if 'JJ' in tag:
        return 'a'
    elif 'NN' in tag:
        return 'n'
    elif 'VB' in tag:
        return 'v'
    elif 'RB' in tag:
        return 'r'
    else:
        return None

def is_important_tag(tag):
    if 'JJ' in tag:
        return True
    elif 'NN' in tag:
        return True
    elif 'VB' in tag:
        return True
    elif 'RB' in tag:
        if tag == 'WRB':
            return False
        return True
    return False

def is_not_important_word(lemmatized_word):
    if lemmatized_word == "be":
        return True
    if lemmatized_word == "have":
        return True
    if lemmatized_word == "find":
        return True
    return False


def getSearchEngineResult(query_dict):
    result_dict = {}
    ix = index.open_dir("index")
    lm = WordNetLemmatizer()
    scoringFunction = scoring.ScoringFunction(K1=2.5, B=0.7, eps=0.0)

    # with ix.searcher(weighting=scoring.BM25F()) as searcher:
    with ix.searcher(weighting=scoringFunction) as searcher:
        # TODO - Define your own query parser
        parser = QueryParser("contents", schema=ix.schema, group=OrGroup.factory(0))

        for qid, q in query_dict.items():
            new_q = ''
            sentence = q.lower()
            tagged_list = pos_tag(word_tokenize(sentence))
            for (word, tag) in tagged_list:
                if not is_important_tag(tag):
                    continue
                if word in stopwords.words('english'):
                    continue
                word = lm.lemmatize(word, pos=tag2pos(tag))
                if is_not_important_word(word):
                    continue
                if '-' in word:
                    for w in word.split('-'):
                        new_q += w + ' '
                else: new_q += word + ' '
            query = parser.parse(new_q)
            results = searcher.search(query, limit=None)
            result_dict[qid] = [result.fields()['docID'] for result in results]
    return result_dict

