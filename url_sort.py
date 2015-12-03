import routing

def somefun1():
    print "first function"

def somefun2():
    print "second function"

def c1fun():
    print "c1 fun"

class Node(object):

    def __init__(self,fun=None,name=None,isvar=False):
        self.children = {}
        self.fun = fun
        self.isvar = isvar
        self.name = name

    def add_child(self, child=None, node=None):
        self.children[child] = node

    def __repr__(self):
        return self.name

url_path = ['root','c1','{myvar1}','c1c1']
u1 = '/root/c1/{myvar}/c1c1'
u2 = '/root/c1/testing/c1c1'

r = routing.DefaultRouter()
r.add_path(u1,somefun1)
print r.root_node_dict
somedict = {}
myfun = r.return_path_resource(u2,somedict)
myfun()


print somedict
