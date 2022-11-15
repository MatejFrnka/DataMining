import time
from itertools import combinations


class Apriori:
    @staticmethod
    def get_combinations_l_1(data):
        res = set()
        for basket in data:
            for item in basket:
                res.add(frozenset({item}))
        return res

    @staticmethod
    def get_combinations(l1_sets, lk_sets):
        res = set()
        for item in lk_sets:
            for singleton in l1_sets:
                if not singleton.issubset(item):
                    res.add(frozenset.union(singleton, item))
        return res

    @staticmethod
    def filter(subsets, s, k, data):
        subset_cnt = {subset: 0 for subset in subsets}
        for item in data:
            for comb in combinations(item, k):
                if frozenset(comb) in subset_cnt:
                    subset_cnt[frozenset(comb)] += 1
        threshold_cnt = len(data) * s
        return [subset for subset, val in subset_cnt.items() if val > threshold_cnt]

    @staticmethod
    def compute(s, k, data):
        assert k > 0
        assert s >= 0
        assert s <= 1
        t = time.time()
        l_1 = Apriori.get_combinations_l_1(data)
        l_1 = Apriori.filter(l_1, s, 1, data)
        print(time.time() - t)
        l_prev = l_1
        for i in range(2, k + 1):
            t = time.time()
            l_curr = Apriori.get_combinations(l_1, l_prev)
            l_curr = Apriori.filter(l_curr, s, i, data)
            print(time.time() - t)
            l_prev = l_curr
        return l_prev


class DataLoader:
    res = []

    @staticmethod
    def load(path):
        res = []
        with open(path) as file:
            for line in file:
                res.append(frozenset([int(x) for x in line.split(" ") if x.isdigit()]))
        return res


# d = {frozenset([1, 2, 3]), frozenset([1, 2]), frozenset([5, 6, 7, 8, 9]), frozenset([1, 2, 3, 4, 5, 6])}
d = DataLoader.load("data/T10I4D100K.dat")
print(Apriori().compute(0.01, 4, d))
