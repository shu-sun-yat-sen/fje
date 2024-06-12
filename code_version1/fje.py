import argparse
from builder import JsonNodeFactoryRegistry

def parse():
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description="Process JSON file with given style and icon family.")
    # 添加参数
    parser.add_argument('-f', '--file', required=True, type=str, help="Path to the JSON file")
    parser.add_argument('-s', '--style', default="tree", type=str, help="Style to be applied")
    parser.add_argument('-i', '--icon', default="default", type=str, help="Icon family to use")
    # 解析参数
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    parse_args = parse()
    r = JsonNodeFactoryRegistry()
    factory = r.get_factory(parse_args.style)()
    factory.build_icon(parse_args.icon)
    factory.build_json_nodes(parse_args.file)
    json_nodes = factory.get_result()
    for sentence in json_nodes.render():
        print(sentence)
        print()

# poker-face-icon-family