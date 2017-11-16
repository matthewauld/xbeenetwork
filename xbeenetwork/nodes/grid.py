
import time
import search

class Grid(object):
    def __init__(self):
        self.graph = {}
        self.loc_states = {}
        self.current_location = None

    def initalize(self,gridsize):
        self.graph = self.generate_graph(gridsize,gridsize)
        self.move_to = ((0,0))


    def move_to(self,loc):
        self.current_location = loc
        try:
            self.loc_states[loc]['visited'] = True
        except KeyError:
            self.loc_states[loc] = {'visited':True}


    def get_neighbors(self,loc):
        try:
            return self.graph[loc]
        except KeyError:
            self.generate_node(loc)
            return self.graph[loc]

    def generate_node(self,loc):
        self.graph[loc] = []
        possible_neighbors = [(loc[0]+1,loc[1]+1),(loc[0]+1,loc[1]),(loc[0]+1,loc[1]-1),(loc[0]-1,loc[1]+1),(loc[0]-1,loc[1]),(loc[0]-1,loc[1]-1),(loc[0],loc[1]+1),(loc[0],loc[1]-1)]
        for node in possible_neighbors:
            if node in self.graph:
                if loc in self.graph[node]:
                    self.graph[loc].append(node)
            else:
                self.graph[loc].append(node)


    def generate_grid(self, width,length):
        result = []
        for x in range(int(width)):
            for y in range(int(length)):
                result.append((int(-width/2)+x,int(-length/2)+y))
        return result

    def generate_graph(self, width, length):
        grid = self.generate_grid(width, length)
        graph ={}
        for i in grid:
            graph[i] = [(i[0]+1,i[1]+1),(i[0]+1,i[1]),(i[0]+1,i[1]-1),(i[0]-1,i[1]+1),(i[0]-1,i[1]),(i[0]-1,i[1]-1),(i[0],i[1]+1),(i[0],i[1]-1)]
        return graph

    def get_path(self, start, end):
        results = search.a_star(self,start,end)
        return results

    def isolate_node(self,i):
        for node in [(i[0]+1,i[1]+1),(i[0]+1,i[1]),(i[0]+1,i[1]-1),(i[0]-1,i[1]+1),(i[0]-1,i[1]),(i[0]-1,i[1]-1),(i[0],i[1]+1),(i[0],i[1]-1)]:
            try:
                self.graph[node].remove(i)
            except ValueError:
                pass
            










x=Grid()
x.initalize(10)
print(x.get_path((0,0),(1,0)))
