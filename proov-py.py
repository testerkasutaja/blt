class node(object):
    def __init__(self):
        self.name=None
        self.node=[]
        self.otherInfo = None
        self.prev=None
    def nex(self,child):
        "Gets a node by number"
        return self.node[child]
    def prev(self):
        return self.prev
    def goto(self,data):
        "Gets the node by name"
        for child in range(0,len(self.node)):
            if(self.node[child].name==data):
                return self.node[child]
    def add(self):
        node1=node()
        self.node.append(node1)
        node1.prev=self
        return node1

tree=node()  #create a node
tree.name="root" #name it root
tree.otherInfo="blue" #or what ever 
tree=tree.add() #add a node to the root
tree.name="node1" #name it


tree=tree.add()
tree.name="grandchild1"


tree=tree.prev()
tree=tree.add()
tree.name="gchild2"


tree=tree.prev()
tree=tree.prev()
tree=tree.add()
tree=tree.name="child2"



