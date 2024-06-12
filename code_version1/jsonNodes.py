from abc import ABC, abstractmethod

class AbstractJsonNode(ABC):
    style = "tree"
    def __init__(self, is_root, is_leaf, icon_family, style_name):
        self.is_root = is_root
        self.is_leaf = is_leaf
        self.style_name = style_name
        self.icon_family = icon_family

    def isLeaf(self):
        return self.is_leaf

    def get_style_name(self):
        return self.style_name
    
    def render(self, param=None):
        if self.is_root:
            return self.render_root(param)
        else:
            return self.render_leaf(param) if self.is_leaf else self.render_container(param)

    @abstractmethod
    def render_leaf(self, param):
        pass
    
    @abstractmethod
    def render_container(self, param):
        pass

    @abstractmethod
    def render_root(self, param):
        pass

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
    
    def getSubnodes(self):
        if not self.isLeaf():
            return self.sub_nodes
        else:
            return []
    
    def get_prefix(self, idx, is_last, with_blank=True):
        prefix = " " if with_blank else ""
        if idx == 0:
            prefix += ("└─" if is_last else "├─")
        else:
            prefix += "  " if is_last else "│ "
        return prefix

    def render_leaf(self, param=None):
        render_result = self.icon_family.get_leaf_icon() + self.key
        render_result += ": " + str(self.value).lower() if self.value is not None else ""
        return [render_result]

    def render_container(self, param=None):
        render_results = []
        render_results.append(self.icon_family.get_inner_icon() + self.key)
        for idx, child in enumerate(self.sub_nodes):
            child_results = [self.get_prefix(i, idx==len(self.sub_nodes)-1) + result for i,result  in enumerate(child.render())]
            render_results.extend(child_results)
        return render_results
            
    def render_root(self, param=None):
        render_results = []
        for idx, child in enumerate(self.sub_nodes):
            child_results = [self.get_prefix(i, idx==len(self.sub_nodes)-1, with_blank=False) + result for i,result  in enumerate(child.render())]
            render_results.extend(child_results)
        return render_results
    
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
    
    def getSubnodes(self):
        if not self.isLeaf():
            return self.sub_nodes
        else:
            return []

    def get_prefix(self, idx, is_last, with_blank=True):
        prefix = " " if with_blank else ""
        if idx == 0:
            prefix += ("┴─" if is_last else "├─")
        else:
            prefix += "│ "
        return prefix
    
    def get_prefix_for_root(self, is_first_container, is_first_in_container, is_last_sentence):
        if is_last_sentence:
            prefix = "└─"
        elif is_first_in_container:
            prefix = "┌─" if is_first_container else "├─"
        else:
            prefix = "│ "
        return prefix

    def render_leaf(self, param=None):
        render_result = self.icon_family.get_leaf_icon() + self.key
        render_result += ": " + str(self.value).lower() if self.value is not None else ""
        return [render_result]

    def render_container(self, param):
        render_results = []
        render_results.append(self.icon_family.get_inner_icon() + self.key)
        for idx, child in enumerate(self.sub_nodes):
            is_last = idx == len(self.sub_nodes) - 1 and param
            child_results = [self.get_prefix(i, is_last and child.isLeaf()) + result for i,result  in enumerate(child.render(is_last))]
            render_results.extend(child_results)
        return render_results

    def render_right(self, render_results):
        target_length = max([len(item) for item in render_results]) + 7
        def add_backfix(is_fist, is_last, item):
            if is_fist:
                return item + "-" * (target_length - len(item)) + "┐"
            elif is_last:
                return item + "-" * (target_length - len(item)) + "┘"
            else:
                return item + "-" * (target_length - len(item)) + "┤"
            
        render_results = [add_backfix(idx ==0, idx==len(render_results)-1, item) \
                            for idx, item in enumerate(render_results)]
        return render_results

    def render_root(self, param=None):
        render_results = []
        for idx, child in enumerate(self.sub_nodes):
            is_last = idx == len(self.sub_nodes)-1
            child_render_result = child.render(is_last)
            child_results = [self.get_prefix_for_root(idx==0, i==0, is_last and i == len(child_render_result)-1) + result for i,result  in enumerate(child_render_result)]
            render_results.extend(child_results)
        return self.render_right(render_results)