import random
from edge_sample import EdgeSample

class TriestFD:
    def __init__(self,M):
        self._M = M
        self._sample = EdgeSample()
        self._globalT = 0
        self._localT = {}
        self._t = 0

    def sample_edge(self,u,v):
        if self._t <= self._M:
            return True
        elif self.flip_biased_coin():
            u_dash, v_dash = self._sample.remove_random_edge()
            return True
        return False

    def update_counters(self,u,v,op):
        common_neighborhood = self._sample.get_intersection_neighborhood(u,v)
        
        if not common_neighborhood:
            return

        increment_t = max(1, int(((self._t-1)*(self._t-2))/(self._M * (self._M - 1)))) 

        for c in common_neighborhood:

            if op == '+':
                self._globalT += increment_t
                
                if c in self._localT:
                    self._localT[c] += increment_t
                else:
                    self._localT[c] = increment_t

                if u in self._localT:
                    self._localT[u] += increment_t
                else:
                    self._localT[u] = increment_t

                if v in self._localT:
                    self._localT[v] += increment_t
                else:
                    self._localT[v] = increment_t


    def flip_biased_coin(self):
        head_prob = random.random()

        if head_prob <= self._M/self._t:
            return True
        else:
            return False

    def return_counters(self):
        return {'global':self._globalT,'local':self._localT}

    def run(self,u,v):
        self._t += 1
        self.update_counters(u,v,'+')
        if self.sample_edge(u,v):
            self._sample.add_edge(u,v)