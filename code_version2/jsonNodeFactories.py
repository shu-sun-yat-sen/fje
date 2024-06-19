from jsonNodes import TreeStyleJsonNode, RectangleStyleJsonNode
from builder import AbstractJsonFactory

class TreeStyleJsonFactory(AbstractJsonFactory):
    node_style = "tree"
    node_class = TreeStyleJsonNode
    
    def __init__(self):
        pass

class RectangleStyleJsonFactory(AbstractJsonFactory):
    node_style = "rectangle"
    node_class = RectangleStyleJsonNode
    def __init__(self):
        pass




    
