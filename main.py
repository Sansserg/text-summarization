"""
Слова через дефис



Что происходит там?

"""

import re
import tkinter.messagebox as mb
import tkinter as tk
from tkinter import filedialog

import nltk
import pyperclip
from gensim import corpora
from gensim.models import Word2Vec
from gensim.similarities import WordEmbeddingSimilarityIndex, SparseTermSimilarityMatrix
from nltk.corpus import stopwords


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.save_button = tk.Button(self, text="Сохранить", command=self.click_save)
        self.copy_button = tk.Button(self, text="Копировать", command=self.click_copy)
        self.label = tk.Label(text="Выберите что сделать с скоращенным текстом")
        self.save_button.grid(row=2, column=0, padx=10, pady=10)
        self.copy_button.grid(row=2, column=2, padx=10, pady=10)
        self.label.grid(row=0, column=1,)

    def click_save(self):
        path_to_save_directory = filedialog.askdirectory()
        with open(f"{path_to_save_directory}/Answer_text.txt", "w") as f:
            f.write(end_text)
        show_info_about('Ваш файл был сохранён в указанную папку')


    def click_copy(self):
        def write(name):
            pyperclip.copy(name)  # Копирует в буфер обмена информацию
            pyperclip.paste()
        write(end_text)
        show_info_about('текст успешно скопирован!')



path_to_file = filedialog.  askopenfilename()


def show_info_about(msg):
    mb.showinfo("Информация", msg)


# Read the file
with open(path_to_file, "r") as f:
    article_text = f.read()

# Cleaning the text
processed_article = re.sub('[^a-zA-Z]', ' ', article_text.lower())
processed_article = re.sub(r'\s+', ' ', processed_article)

# Tokenize sentences and words
all_sentences = nltk.sent_tokenize(processed_article)
all_words = [nltk.word_tokenize(sent) for sent in all_sentences]

# Removing stop words
stop_words_eng = set(stopwords.words('english'))
stop_words = set(stopwords.words('russian'))

for i in range(len(all_words)):
    all_words[i] = [w for w in all_words[i] if w not in stop_words_eng]

# Train Word2Vec model
try:
    word2vec = Word2Vec.load("word2vec.model")
    word2vec.train(all_words, min_count=0)
except:
    word2vec = Word2Vec(all_words, min_count=0)

# Create a dictionary of sentences with vectors
all_sentences_with_vector = {}
sentence_for_vect = (re.sub(r'\s+', ' ', article_text)).split(".")

for i in range(len(sentence_for_vect)):
    sentence_for_vect[i] = sentence_for_vect[i].strip()

for j in range(len(sentence_for_vect)):
    all_sentences_with_vector[sentence_for_vect[j]] = 0
    for i in all_words[0]:
        if i in word2vec.wv:
            all_sentences_with_vector[sentence_for_vect[j]] += word2vec.wv.get_vector(i)

# Normalize the vectors
for i in all_sentences_with_vector.keys():
    all_sentences_with_vector[i] = all_sentences_with_vector[i] / len(i)

past2 = sentence_for_vect.copy()

# Prepare the documents for the similarity matrix
documents = [sentence.split() for sentence in sentence_for_vect]

# Create a dictionary and a corpus
dictionary = corpora.Dictionary(documents)

# Prepare the similarity matrix
similarity_index = WordEmbeddingSimilarityIndex(word2vec.wv)
similarity_matrix = SparseTermSimilarityMatrix(similarity_index, dictionary)

# Convert the sentences into bag-of-words vectors
sentence_for_vect_bow = [dictionary.doc2bow(sentence.split()) for sentence in sentence_for_vect]

# Compute soft cosine similarity
dict_for_max_sim = {}
for i in range(len(sentence_for_vect) - 1):
    dict_for_max_sim[sentence_for_vect[i]] = 0
    for j in range(1, len(sentence_for_vect)):
        sent_1 = sentence_for_vect_bow[i]
        sent_2 = sentence_for_vect_bow[j]
        dict_for_max_sim[sentence_for_vect[i]] += similarity_matrix.inner_product(sent_1, sent_2)

# Sort the sentences by similarity score
prozent = int(input("% = "))
count_sentences = (len(sentence_for_vect) * prozent) // 100

text_sorted = []
for _ in range(count_sentences):
    maxx_val = max(dict_for_max_sim.values())
    for j in dict_for_max_sim.keys():
        if dict_for_max_sim[j] == maxx_val:
            text_sorted.append(j)
            dict_for_max_sim[j] = 0

end_text = ""

for j in past2:
    if j in text_sorted:
        end_text += j + "\n"

app = App()
app.mainloop()

word2vec.save("word2vec.model")
