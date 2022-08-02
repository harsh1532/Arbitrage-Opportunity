import math


class Arbitrage:
    def __init__(self, data, db):
        self.db = db
        self.timestamp = data.pop('_id')
        self.symbols = set(data['data'].keys())
        self.G, self.weight = self.create_graph(data)
        self.get_opportunities()

    def create_graph(self, data):
        G = {'adj': {}}
        weight = {}
        for symbol in data['data']:
            G['adj'][symbol] = set()
            all_symb = list(data['data'][symbol]['rates'].keys())
            for symb in all_symb:
                if symb in self.symbols:
                    weight[(symbol, symb)] = round(
                        math.log2(round(1/data['data'][symbol]['rates'][symb], 6)), 6)
                    G['adj'][symbol].add(symb)

        for i in range(len(self.symbols)):
            for j in range(i+1, len(self.symbols)):
                s1, s2 = self.symbols[i], self.symbols[j]
                if weight[(s1, s2)] <= weight[(s2, s1)]:
                    weight[(s2, s1)] = -weight[(s1, s2)]
                else:
                    weight[(s1, s2)] = -weight[(s2, s1)]

        return G, weight

    def detectNegCycle(self, src, parent):
        node = str(src)
        stack = [node]  # The path from src to other curriences
        visited = set()
        visited.add(src)  # Keeping track of visited nodes
        isOpr = True
        while parent[node] != src:
            node = parent[node]
            if node in stack:  # There exists a negative cycle elsewhere but not from the source node
                isOpr = False
                break
            stack.append(node)
            visited.add(node)

        # Calculating the profit in percentage
        profit = 0
        path = []  # The actual arbitrage path
        if isOpr:
            N = len(stack)
            for i in range(N-1):
                frm, to = stack[i], stack[i+1]
                profit += self.weight[(frm, to)]
                path.append((frm, to, self.weight[(frm, to)]))
            profit += self.weight[(stack[-1], src)]
            path.append(
                (stack[-1], src, self.weight[(stack[-1], src)]))

        return isOpr, profit, path

    def findArbitrage(self, src, cost):
        distance = {}
        parent = {src: ''}
        for node in self.G['adj']:
            distance[node] = math.inf
        distance[src] = 0
        changed = [src]
        # prevDistance = distance.copy()
        V = len(distance)

        for i in range(V):
            newChanges = []
            newDistance = distance.copy()
            # prevDistance = distance.copy()
            for node in changed:
                for nei in self.G['adj'][node]:
                    if (cost[(node, nei)] + distance[node]) < newDistance[nei]:
                        newDistance[nei] = round(
                            cost[(node, nei)] + distance[node], 8)

                        newChanges.append(nei)
                        parent[nei] = node
            changed = newChanges
            distance = newDistance
            if parent[src] != '':
                break

        isOpr, profit, path = self.detectNegCycle(src, parent)

        return isOpr, profit, path

    def get_opportunities(self):
        mdb_store_opp = self.db['historic_opportunities']
        opps = []
        for sym in self.symbols:
            src = sym
            isOpr, profit, path = self.findArbitrage(src, self.G, self.weight)
            if isOpr:
                print(src, ' ', profit, ' ', path)
                opps.append({'src': src, 'profit': profit, 'path': path})
            try:
                mdb_store_opp.insert_one(
                    {'_id': self.timestamp, 'opportunities': opps})
            except:
                mdb_store_opp.delete_one({'_id': self.timestamp})
                mdb_store_opp.insert_one(
                    {'_id': self.timestamp, 'opportunities': opps})
