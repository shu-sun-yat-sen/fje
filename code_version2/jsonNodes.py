from abc import ABC, abstractmethod

class AbstractJsonNode(ABC):
    def __init__(self, is_root, is_leaf, icon_family, style_name):
        self.is_root = is_root
        self.is_leaf = is_leaf
        self.style_name = style_name
        self.icon_family = icon_family

    def isLeaf(self):
        return self.is_leaf
    
    def getIconFamily(self):
        return self.icon_family

    def get_style_name(self):
        return self.style_name

class TreeStyleJsonNode(AbstractJsonNode):
    def __init__(self, is_root, is_leaf, icon_family, level, is_last, content):
        super().__init__(is_root, is_leaf, icon_family, style_name="tree")
        self.level = level
        self.is_last = is_last
        if self.isLeaf():
            self.key, self.value = content
        else:
            self.key, self.sub_nodes = content

    def getKey(self):
        return self.key
    
    def getValue(self):
        return self.value
    
    def getSubnodes(self):
        if not self.isLeaf():
            return self.sub_nodes
        else:
            return []
    
class RectangleStyleJsonNode(AbstractJsonNode):
    def __init__(self, is_root, is_leaf, icon_family, level, is_last, content):
        super().__init__(is_root, is_leaf, icon_family, style_name="rectangle")
        self.level = level
        self.is_last = is_last
        if self.isLeaf():
            self.key, self.value = content
        else:
            self.key, self.sub_nodes = content

    def getKey(self):
        return self.key
    
    def getValue(self):
        return self.value
    
    def getSubnodes(self):
        if not self.isLeaf():
            return self.sub_nodes
        else:
            return []