import random

from bs4 import BeautifulSoup
import os


def create_data():
    documents = []
    for file in os.listdir("data/"):
        if file.endswith(".sgm"):

            # for each sgm file, read it
            filename = os.path.join("data", file)
            f = open(filename, 'r', encoding='utf-8', errors='ignore')
            dataFile = f.read()

            # pass it to BeautifulSoup
            soup = BeautifulSoup(dataFile, 'html.parser')
            contents = soup.findAll('body')

            # for each body tag, extract it's text
            acc = 0
            for content in contents:
                acc += 1
                f = open("data/reut2-" + str(acc) + ".txt", 'w', encoding='utf-8')
                f.write('\n'.join(content))


def load_data(cnt=-1):
    documents = []
    for file in os.listdir("data/"):
        if file.endswith(".txt"):
            filename = os.path.join("data", file)
            f = open(filename, 'r', encoding='utf-8', errors='ignore')
            dataFile = f.read()
            documents.append((file, dataFile))
            if cnt == len(documents):
                return documents
    return documents


def load_doc(id):
    f = open(f"data/reut2-{id}.txt", 'r', encoding='utf-8', errors='ignore')
    return f.read()


if __name__ == "__main__":
    create_data()
