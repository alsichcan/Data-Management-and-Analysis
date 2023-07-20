import os.path
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, NUMERIC

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


schema = Schema(docID=NUMERIC(stored=True), contents=TEXT)
index_dir = "index"

if not os.path.exists(index_dir):
    os.makedirs(index_dir)

ix = create_in(index_dir, schema)
writer = ix.writer()
lm = WordNetLemmatizer()
with open('doc/document.txt', 'r') as f:
    text = f.read()
    docs = text.split('   /\n')[:-1]
    for doc in docs:
        br = doc.find('\n')
        docID = int(doc[:br])
        doc_text = doc[br+1:]
        tagged_list = pos_tag(word_tokenize(doc_text))
        new_doc_text = ''
        for (word, tag) in tagged_list:
            if not is_important_tag(tag):
                new_doc_text += '/////' + ' '
                continue
            word = lm.lemmatize(word, pos=tag2pos(tag))
            if '-' in word:
                for w in word.split('-'):
                    new_doc_text += w + ' '
            else: new_doc_text += word + ' '
        # print(new_doc_text, '\n')
        writer.add_document(docID=docID, contents=new_doc_text)

writer.commit()