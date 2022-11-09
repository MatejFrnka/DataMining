import numpy as np
import numpy.random

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
            document_matrix.append(np.array([k in shingle_sets[i] for k in all_elements_array]))
        return np.array(document_matrix).T

    def apply_hashers(self, val):
        return np.array((np.repeat(val, self.hasher_cnt) * self.multiplier + self.bias) % self.mod)

    def get_signature(self, document_matrix):
        res_signature = np.ones((document_matrix.shape[1], self.hasher_cnt)) * MAX_INT
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


class LSH:
    ...


if __name__ == "__main__":
    s = Shingling(2)
    s1 = s.get_shingles("abcdefgh")
    s2 = s.get_shingles("abcdef")
    print(CompareSets().jaccard_similarity(s1, s2))
    minhash = MinHashing(100)
    signature = minhash.minhash([s1, s2])
    print(CompareSignatures().compare(signature[0], signature[1]))
