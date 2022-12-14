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
        candidate_pairs = dict()
        for band in buckets:
            for slot in band:
                if len(slot) > 1:
                    for c in itertools.combinations(slot, 2):
                        c_frozen = frozenset(c)
                        if c_frozen in candidate_pairs:
                            candidate_pairs[c_frozen] += 1
                        else:
                            candidate_pairs[c_frozen] = 1

        return candidate_pairs

    def lsh(self, signature, band_cnt, similarity, bucket_cnt=1_000):
        # get candidate pairs
        candidate_pairs = self.get_candidate_pairs(signature, band_cnt, bucket_cnt)
        # similarity threshold
        row_cnt = signature.shape[1] // band_cnt
        print(f"LSH tuned for {round((1 / band_cnt) ** (1 / row_cnt) * 100, 1)}% similarity")
        res = []
        comparator = CompareSignatures()
        for pair in candidate_pairs:
            p = list(pair)
            if comparator.compare(signature[p[0]], signature[p[1]]) > similarity:
                res.append(p)
        return res


def filter_results(data, similarities, threshold):
    filtered = filter(lambda x: x[0] > threshold, similarities)
    sorted_sim = sorted(filtered, key=lambda x: x[0])
    return [(data[k[1][0]][0], data[k[1][1]][0]) for k in sorted_sim]


def naive_similarity(threshold, shingle_len):
    data = load_data(-1)
    shingler = Shingling(shingle_len)
    data_shingles = [shingler.get_shingles(doc[1]) for doc in data]
    similarities = []
    for i, doc_i in enumerate(data_shingles):
        for o, doc_o in enumerate(data_shingles):
            if i > o:
                similarities.append((CompareSets().jaccard_similarity(doc_i, doc_o), (i, o)))
    return filter_results(data, similarities, threshold)


def minhash_similarity(threshold, shingle_len, hasher_cnt):
    data = load_data(-1)
    shingler = Shingling(shingle_len)
    similarities = []
    data_shingles = [shingler.get_shingles(doc[1]) for doc in data]
    # print("shingled")
    minhash = MinHashing(hasher_cnt)
    signature = minhash.minhash(data_shingles)
    for i, val_i in enumerate(signature):
        for o, val_o in enumerate(signature):
            if i > o:
                similarities.append((CompareSignatures().compare(val_i, val_o), (i, o)))
    return filter_results(data, similarities, threshold)


def lsh(threshold, shingle_len, hasher_cnt):
    data = load_data()
    shingler = Shingling(shingle_len)
    similarities = []
    data_shingles = [shingler.get_shingles(doc[1]) for doc in data]
    # print("shingled")
    minhash = MinHashing(hasher_cnt)
    signature = minhash.minhash(data_shingles)
    res = LSH().lsh(signature, 10, threshold)
    return [(data[r[0]][0], data[r[1]][0]) for r in res]


if __name__ == "__main__":
    sim = 0.80
    shing = 3
    hashers = 100
    print(naive_similarity(sim, shing))
    print(minhash_similarity(sim, shing, 100))
    print(lsh(sim, shing, 100))
