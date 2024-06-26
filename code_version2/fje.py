import argparse
from builder import JsonNodeFactoryRegistry, RenderRegistery

def parse():
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description="Process JSON file with given style and icon family.")
    # 添加参数
    parser.add_argument('-f', '--file', default="./data.json", type=str, help="Path to the JSON file")
    parser.add_argument('-s', '--style', default="tree", type=str, help="Style to be applied")
    parser.add_argument('-i', '--icon', default="default", type=str, help="Icon family to use")
    # 解析参数
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    parse_args = parse()
    jsonNodeFactoryRegistry = JsonNodeFactoryRegistry()
    factory = jsonNodeFactoryRegistry.get_factory(parse_args.style)()
    factory.build_icon(parse_args.icon)
    factory.build_json_nodes(parse_args.file)
    json_nodes = factory.get_result()
    renderRegistery = RenderRegistery()
    render = renderRegistery.get_render(json_nodes.get_style_name())()
    for sentence in render.render(json_nodes):
        print(sentence)
        print()
