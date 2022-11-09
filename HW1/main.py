import numpy as np
from data import load_data, load_doc
import itertools

MAX_INT = 2 ** 31 - 1


class Shingling:

    def __init__(self, k):
        self.k = k

    def get_shingles(self, string):
        shingles = set()
        for i in range(len(string) - self.k + 1):
            shingles.add(hash(string[i:i + self.k]))
        return shingles


class CompareSets:

    def jaccard_similarity(self, a, b) -> float:
        return len(a.intersection(b)) / len(a.union(b))


class MinHashing:

    def __init__(self, hasher_cnt):
        self.hasher_cnt = hasher_cnt
        self.multiplier = np.random.randint(1, MAX_INT, size=hasher_cnt)
        self.bias = np.random.randint(0, MAX_INT, size=hasher_cnt)
        self.mod = MAX_INT

    def get_document_matrix(self, shingle_sets):
        all_elements_array = list(set().union(*shingle_sets))
        document_matrix = []
        for i in range(len(shingle_sets)):
            document_matrix.append(
                np.array([k in shingle_sets[i] for k in all_elements_array]))
        return np.array(document_matrix).T

    def apply_hashers(self, val):
        return np.array(
            (np.repeat(val, self.hasher_cnt) * self.multiplier + self.bias) %
            self.mod)

    def get_signature(self, document_matrix):
        res_signature = np.ones(
            (document_matrix.shape[1], self.hasher_cnt)) * MAX_INT
        for i, row in enumerate(document_matrix):
            hashed_i = self.apply_hashers(i)
            for k, col in enumerate(row):
                if col:
                    res_signature[k] = np.minimum(res_signature[k], hashed_i)
        return res_signature

    def minhash(self, shingles_sets):
        document_matrix = self.get_document_matrix(shingles_sets)
        return self.get_signature(document_matrix)


class CompareSignatures:

    def compare(self, a, b):
        return np.sum(a == b) / len(a)


# Locality Sensitive Hashing
class LSH:

    def sep_siganture(self, sig, bands):
        return np.array_split(sig, bands, axis=1)

    def get_candidate_pairs(self, signature, band_cnt, bucket_cnt=10_000):
        bands = self.sep_siganture(signature, band_cnt)

        buckets = [[[] for _ in range(bucket_cnt)] for _ in range(band_cnt)]

        # distribute similarity to buckets
        for i, band in enumerate(bands):
            for k, doc in enumerate(band):
                buckets[i][hash(str(doc)) % bucket_cnt].append(k)

        # get candidate pairs
        candidate_pairs = set()
        for band in buckets:
            for slot in band:
                if len(slot) > 1:
                    for c in itertools.combinations(slot, 2):
                        c_frozen = frozenset(c)
                        candidate_pairs.add(c_frozen)
        return candidate_pairs

    def lsh(self, signature, band_cnt, similarity, bucket_cnt=1_000):
        # get candidate pairs
        candidate_pairs = self.get_candidate_pairs(signature, band_cnt, bucket_cnt)
        res = []
        comparator = CompareSignatures()
        for pair in candidate_pairs:
            p = list(pair)
            if comparator.compare(signature[p[0]], signature[p[1]]) > similarity:
                res.append(p)
        return res


def naive_similarity(doc_cnt, threshold):
    shingler = Shingling(3)
    similarities = []
    for i in range(doc_cnt):
        for o in range(doc_cnt):
            if i > o:
                d1 = load_doc(o)
                d2 = load_doc(i)

                s1 = shingler.get_shingles(d1)
                s2 = shingler.get_shingles(d2)
                similarities.append((CompareSets().jaccard_similarity(s1, s2), f"{i}-{o}"))
        print(i)

    filtered = filter(lambda x: x[0] > threshold, similarities)
    sorted_sim = sorted(filtered, key=lambda x: x[0])
    return sorted_sim


def minhash_similarity(doc_cnt, threshold):
    data = load_data(doc_cnt)
    shingler = Shingling(3)
    similarities = []
    data_shingles = [shingler.get_shingles(doc) for doc in data]
    # print("shingled")
    minhash = MinHashing(100)
    signature = minhash.minhash(data_shingles)
    for i, val_i in enumerate(signature):
        for o, val_o in enumerate(signature):
            if i > o:
                similarities.append((CompareSignatures().compare(val_i, val_o), f"{i}-{o}"))
    filtered = filter(lambda x: x[0] > threshold, similarities)
    sorted_sim = sorted(filtered, key=lambda x: x[0])
    return sorted_sim


if __name__ == "__main__":
    doc_cnt = 199
    threshold = 0.75
    sim = 0.85
    # print(naive_similarity(doc_cnt, sim))
    print(minhash_similarity(doc_cnt, sim))

    data = load_data()
    shingler = Shingling(3)
    similarities = []
    data_shingles = [shingler.get_shingles(doc) for doc in data]
    # print("shingled")
    minhash = MinHashing(100)
    signature = minhash.minhash(data_shingles)
    print(LSH().lsh(signature, 10, sim))
