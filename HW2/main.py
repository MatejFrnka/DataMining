import time
from itertools import combinations


class Apriori:
    @staticmethod
    def get_combinations_l_0(data):
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
        :return: filtered dictionary with candidate sets as keys and their counts as values
        """
        subset_cnt = {subset: 0 for subset in candidate_subsets}
        for item in data:
            for comb in combinations(item, k):
                # if comb is in candidate subsets, increase its count by 1
                if frozenset(comb) in subset_cnt:
                    subset_cnt[frozenset(comb)] += 1
        # only return subsets that are frequent enough
        threshold_cnt = len(data) * support
        return {subset: val for subset, val in subset_cnt.items() if val > threshold_cnt}

    @staticmethod
    def find_frequent(support, data):
        """
        This function uses the A-priori pruning principle - if there is any item-set that is infrequent,
        its superset is also not frequent. The function starts with generating subsets of size 1 and then increases
        their size until they are of size k
        :param support: support, must be in range (0,1]
        :param k: find frequent sets of size k, must be an integer greater than 0
        :param data: array of sets representing the dataset
        :return: array of frozen sets with frequency above the support
        """
        assert support >= 0
        assert support <= 1

        l = list()

        # generate subsets of size 1
        t = time.time()
        l_1 = Apriori.get_combinations_l_0(data)
        # filter out the infrequent subsets
        l_1_dict = Apriori.check(l_1, support, 1, data)
        print(time.time() - t)
        if len(l_1_dict) == 0:
            return l

        l.append(l_1_dict)
        k = 2
        while True:
            t = time.time()

            # generate subsets of size i
            l_k = Apriori.get_combinations(l_1_dict.keys(), l[-1])

            # filter out the infrequent subsets
            l_k_dict = Apriori.check(l_k, support, k, data)

            print(time.time() - t)
            if len(l_k_dict) == 0:
                return l
            l.append(l_k_dict)
            k += 1

    @staticmethod
    def find_associated(support, confidence, data):
        frequent_array = Apriori.find_frequent(support, data)
        # get all combinations
        comb = set()
        for frequent in frequent_array:
            for frequent_set, frequent_count in frequent.items():
                for i in range(1, len(frequent_set)):
                    for frequent_subset in combinations(frequent_set, i):
                        frequent_subset = frozenset(frequent_subset)
                        subset_count = frequent_array[i - 1][frequent_subset]
                        c = frequent_count / subset_count
                        if c > confidence:
                            comb.add((frequent_subset, frequent_set - frequent_subset))
        return comb


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


if __name__ == "__main__":
    # d = {frozenset([1, 2, 3]), frozenset([1, 2]), frozenset([5, 6, 7, 8, 9]), frozenset([1, 2, 3, 4, 5, 6])}
    # d = {frozenset(['m', 'c', 'b']),
    #      frozenset(['m', 'p', 'j']),
    #      frozenset(['m', 'c', 'b', 'n']),
    #      frozenset(['c', 'j']),
    #      frozenset(['m', 'p', 'b']),
    #      frozenset(['m', 'c', 'b', 'j']),
    #      frozenset(['c', 'b', 'j']),
    #      frozenset(['b', 'c']),
    #      }
    d = DataLoader.load("data/T10I4D100K.dat")
    asoc = Apriori.find_associated(0.01, 0.5, d)
    print("adsf")
