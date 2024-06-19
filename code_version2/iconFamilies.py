import json
def open_json_file(file_name):
    with open(file_name, "r") as f:
        return json.load(f)

class iconFamily():
    def __init__(self, icon_family_name):
        self.icon_families = self.scan_icon()
        self.inner_icon = self.icon_families[icon_family_name]["inner_icon"]
        self.leaf_icon = self.icon_families[icon_family_name]["leaf_icon"]

    def scan_icon(self):
        icon_styles = open_json_file("config.json")["icon_styles"]
        return icon_styles
    
    def get_leaf_icon(self):
        return self.leaf_icon
    
    def get_inner_icon(self):
        return self.inner_icon