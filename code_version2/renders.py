from builder import AbstractRender

class TreeStyleRender(AbstractRender):
    style = "tree"
    def __init__(self):
        pass

    def get_prefix(self, idx, is_last, with_blank=True):
        prefix = " " if with_blank else ""
        if idx == 0:
            prefix += ("└─" if is_last else "├─")
        else:
            prefix += "  " if is_last else "│ "
        return prefix

    def render_leaf(self, node, param=None):
        render_result = node.getIconFamily().get_leaf_icon() + node.getKey()
        render_result += ": " + str(node.getValue()).lower() if node.getValue() is not None else ""
        return [render_result]

    def render_container(self, node, param=None):
        render_results = []
        render_results.append(node.getIconFamily().get_inner_icon() + node.getKey())
        for idx, child in enumerate(node.getSubnodes()):
            child_results = [self.get_prefix(i, idx==len(node.getSubnodes())-1) + result for i,result  in enumerate(self.render(child))]
            render_results.extend(child_results)
        return render_results

    def render_root(self, node, param=None):
        render_results = []
        for idx, child in enumerate(node.getSubnodes()):
            child_results = [self.get_prefix(i, idx==len(node.getSubnodes())-1, with_blank=False) + result for i,result  in enumerate(self.render(child))]
            render_results.extend(child_results)
        return render_results

class RectangleStyleRender(AbstractRender):
    style = "rectangle"
    def __init__(self):
        pass

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
    
    def render_leaf(self, node, param=None):
        render_result = node.getIconFamily().get_leaf_icon() + node.getKey()
        render_result += ": " + str(node.getValue()).lower() if node.getValue() is not None else ""
        return [render_result]

    def render_container(self, node,  param):
        render_results = []
        render_results.append(node.icon_family.get_inner_icon() + node.getKey())
        for idx, child in enumerate(node.getSubnodes()):
            is_last = idx == len(node.getSubnodes()) - 1 and param
            child_results = [self.get_prefix(i, is_last and child.isLeaf()) + result for i,result  in enumerate(self.render(child, is_last))]
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
    
    def render_root(self, node, param=None):
        render_results = []
        for idx, child in enumerate(node.getSubnodes()):
            is_last = idx == len(node.getSubnodes())-1
            child_render_result = self.render(child, is_last)
            child_results = [self.get_prefix_for_root(idx==0, i==0, is_last and i == len(child_render_result)-1) + result for i,result  in enumerate(child_render_result)]
            render_results.extend(child_results)
        return self.render_right(render_results)
