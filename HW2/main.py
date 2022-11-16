import time
from itertools import combinations


class Apriori:
    @staticmethod
    def get_combinations_l_1(data):
        """
        :param data: Array of sets - each set containing the row in the dataset
        :return: Returns a set of frozen sets of size 1. Contains all items from data
        """
        res = set()
        for row in data:
            for item in row:
                # Add item to result
                res.add(frozenset({item}))
        return res

    @staticmethod
    def get_combinations(l1_sets, lk_sets):
        """

        :param l1_sets: set of frozen sets returned from get_combinations_l_1 function.
        :param lk_sets: set of frozen sets of k - 1 size
        :return: sets of frozen sets of length k created by combining elements from l1_sets and lk_sets
         where the intersection in an empty set.
        """
        res = set()
        for item in lk_sets:
            for val in l1_sets:
                # check if val is not a subset of item
                # no need to check the other way because size of item is always larger or equal than val
                if not val.issubset(item):
                    res.add(frozenset.union(val, item))
        return res

    @staticmethod
    def check(candidate_subsets, support, k, data):
        """
        This function counts all occurrences of candidate_subsets in data and check if their
        count is above the given threshold s
        :param candidate_subsets: array of subsets to filter out the non-frequent items
        :param support: support
        :param k: size of sets in the subsets
        :param data: the dataset
        :return: filtered array of candidate subsets
        """
        subset_cnt = {subset: 0 for subset in candidate_subsets}
        for item in data:
            for comb in combinations(item, k):
                # if comb is in candidate subsets, increase its count by 1
                if frozenset(comb) in subset_cnt:
                    subset_cnt[frozenset(comb)] += 1
        # only return subsets that are frequent enough
        threshold_cnt = len(data) * support
        return [subset for subset, val in subset_cnt.items() if val > threshold_cnt]

    @staticmethod
    def find_frequent(support, k, data):
        """
        This function uses the A-priori pruning principle - if there is any item-set that is infrequent,
        its superset is also not frequent. The function starts with generating subsets of size 1 and then increases
        their size until they are of size k
        :param support: support, must be in range (0,1]
        :param k: find frequent sets of size k, must be an integer greater than 0
        :param data: array of sets representing the dataset
        :return: array of frozen sets with frequency above the support
        """
        assert k > 0
        assert support >= 0
        assert support <= 1
        t = time.time()

        # generate subsets of size 1
        l_1 = Apriori.get_combinations_l_1(data)

        # filter out the infrequent subsets
        l_1 = Apriori.check(l_1, support, 1, data)
        print(time.time() - t)
        l_prev = l_1
        for i in range(2, k + 1):
            t = time.time()

            # generate subsets of size i
            l_curr = Apriori.get_combinations(l_1, l_prev)

            # filter out the infrequent subsets
            l_curr = Apriori.check(l_curr, support, i, data)

            print(time.time() - t)
            l_prev = l_curr
        return l_prev

    @staticmethod
    def find_associated(support, confidence, data):
        ...

class DataLoader:
    res = []

    @staticmethod
    def load(path):
        """
        Loads space seperated numbers in specified file.
        :param path: File path
        :return: Array of frozen sets
        """
        res = []
        with open(path) as file:
            for line in file:
                res.append(frozenset([int(x) for x in line.split(" ") if x.isdigit()]))
        return res


# d = {frozenset([1, 2, 3]), frozenset([1, 2]), frozenset([5, 6, 7, 8, 9]), frozenset([1, 2, 3, 4, 5, 6])}
d = DataLoader.load("data/T10I4D100K.dat")
print(Apriori().find_frequent(0.01, 4, d))
