from abc import ABC, abstractmethod
from iconFamilies import iconFamily
import inspect
import importlib
from iconFamilies import open_json_file

class RenderRegistery:
    def __init__(self):
        self.renders = {}
        self.scan_renders()

    def scan_renders(self, module_name="renders"):
        module = importlib.import_module(module_name)
        all_classes = inspect.getmembers(module, inspect.isclass)
        module_classes = [cls for name, cls in all_classes if cls.__module__ == module_name]
        for cls in module_classes:
            self.renders[cls.style] = cls
    
    def register(self, render):
        self.renders[render.style] = render

    def get_render(self, style):
        return self.renders[style]

class AbstractRender(ABC):
    def render(self, node, param=None):
        if node.is_root:
            return self.render_root(node, param)
        else:
            return self.render_leaf(node, param) if node.is_leaf else self.render_container(node,param)
    
    @abstractmethod
    def render_root(self, node, param=None):
        pass

    @abstractmethod
    def render_leaf(self, node, param=None):
        pass

    @abstractmethod
    def render_container(self, node, param=None):
        pass

class JsonNodeFactoryRegistry:
    def __init__(self):
        self.factories = {}
        self.scan_factories()

    def scan_factories(self, module_name="jsonNodeFactories"):
        module = importlib.import_module(module_name)
        all_classes = inspect.getmembers(module, inspect.isclass)
        module_classes = [cls for name, cls in all_classes if cls.__module__ == module_name]
        for cls in module_classes:
            if not cls == AbstractJsonFactory:
                self.factories[cls.node_style] = cls
    
    def register(self, factory):
        self.factories[factory.node_style] = factory

    def get_factory(self, node_style):
        return self.factories[node_style]

class AbstractJsonFactory(ABC):
    icon_family = None
    result = None

    def build_icon(self, icon_family_name="default"):
        self.icon_family = iconFamily(icon_family_name)
    
    def build_json_nodes(self, file_name):
        if self.icon_family is None:
            self.build_icon()
        data = open_json_file(file_name)
        self.result = self.create_recursively("root", data, 0, True)
    
    def create_recursively(self, key, value, level, is_last):
        is_root = True if key == "root" else  False
        is_leaf = False if isinstance(value, dict)  else True
        content = [key]
        if is_leaf:
            content.append(value)
        else:
            sub_nodes = []
            for idx, (k, v) in enumerate(value.items()):
                is_last = idx == len(value.items()) - 1
                sub_nodes.append(self.create_recursively(k, v, level + 1, is_last))
            content.append(sub_nodes)
        return self.node_class(is_root, is_leaf, self.icon_family, level, is_last, content)
    
    def get_result(self):
        return self.result
    
