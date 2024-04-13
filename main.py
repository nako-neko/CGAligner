import os
import json
from PIL import Image


def overlay_diff_images(base_image, diff_path, coordinate):
    """
    将差分图片叠加到基准图片上，并返回结果图片对象。
    """
    # 打开差分图片
    try:
        diff_image = Image.open(diff_path)
    except FileNotFoundError:
        print(f"错误：未找到差分图片 {diff_path}")
        return base_image  # 返回原始图片

    # 将差分图片叠加到基准图片上，忽略 alpha 通道
    base_image.paste(diff_image, coordinate, diff_image)

    return base_image


def process_images(base_image_path, json_path):
    """
    处理图片并保存结果。
    """
    # 打开基准图片
    try:
        base_image = Image.open(base_image_path)
    except FileNotFoundError:
        print(f"错误：未找到基准图片 {base_image_path}")
        return  # 直接返回，不再进行处理

    # 打开 JSON 文件并解析内容
    try:
        with open(json_path, 'r') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        print(f"错误：未找到 JSON 文件 {json_path}")
        return  # 直接返回，不再进行处理

    # 创建结果保存目录
    result_dir = "result"
    os.makedirs(result_dir, exist_ok=True)

    # 示例数据
    base_image_dir = os.path.dirname(base_image_path)

    # 创建结果子目录
    result_subdir = os.path.join(result_dir, os.path.basename(base_image_dir))
    os.makedirs(result_subdir, exist_ok=True)

    # 保存 base 图片
    # base_result_image_path = os.path.join(result_subdir, os.path.basename(base_image_path))
    # base_image.save(base_result_image_path)

    # 处理差分图片
    for layer in json_data['layers']:
        # 检查是否为基准图片
        # if layer.get('name') == os.path.splitext(os.path.basename(base_image_path))[0]:
        #     continue

        # 构造差分图片完整的路径
        diff_image_name = f"{layer['layer_id']}.png"
        diff_image_path = os.path.join(base_image_dir, diff_image_name)

        # 处理图片
        result_image = overlay_diff_images(base_image.copy(), diff_image_path, (layer['left'], layer['top']))

        # 构造结果图片文件名
        # result_image_name = f"{os.path.splitext(os.path.basename(base_image_path))[0]}+{os.path.splitext(diff_image_name)[0]}.png" # 保存为"base+diff"的形式
        result_image_name = f"{os.path.splitext(diff_image_name)[0]}.png" # 保存为差分图片的文件名
        result_image_path = os.path.join(result_subdir, result_image_name)

        # 保存结果图片时指定压缩质量为 100（最高质量）
        result_image.save(result_image_path, quality=100)

        # 输出完成信息
        print(f"完成处理图片 {diff_image_name}，结果保存在 {result_image_path}")

    # 输出总体完成信息
    print("所有差分图片处理完成！")


def get_base_image_and_json_path(folder_name, base_image_name):
    """
    根据文件夹名称和基准图片名称，返回基准图片路径和 JSON 文件路径。
    """
    base_image_path = os.path.join("source", folder_name, base_image_name)
    json_path = os.path.join("source", f"{folder_name}.json")

    # 检查基准图片路径和 JSON 文件路径是否存在
    if not os.path.exists(base_image_path):
        print(f"错误：未找到基准图片 {base_image_path}")
        return None, None
    if not os.path.exists(json_path):
        print(f"错误：未找到 JSON 文件 {json_path}")
        return None, None

    return base_image_path, json_path

# # 示例数据
# folder_name = "ev703a"
# base_image_name = "2.png"

# # 获取基准图片路径和 JSON 文件路径
# base_image_path, json_path = get_base_image_and_json_path(folder_name, base_image_name)

# # 处理图片并保存结果
# process_images(base_image_path, json_path)

def get_folder_name():
    """
    获取文件夹名称，根据用户输入返回完整的文件夹名称。
    """
    default_folder_prefix = "ev"
    default_folder_suffix = "a"

    folder_input = input("请输入文件夹名称或编号：")
    try:
        if folder_input.isdigit() and len(folder_input) == 3:
            folder_name = f"{default_folder_prefix}{folder_input}{default_folder_suffix}"
        else:
            folder_name = folder_input

        if not os.path.exists(os.path.join("source", folder_name)):
            raise ValueError("错误：未找到对应文件夹！")
    except ValueError as ve:
        print(ve)
        return None

    return folder_name


def get_base_image_name():
    """
    获取基准图片名称，根据用户输入返回完整的基准图片名称。
    """
    default_base_image_name = "2.png"

    base_image_input = input("请输入基准图片编号（只需输入数字或带后缀的文件名，默认为\"2.png\"）：")
    try:
        if base_image_input.isdigit():
            base_image_name = f"{base_image_input}.png"
        elif base_image_input.endswith(".png"):
            base_image_name = base_image_input
        elif not base_image_input:
            base_image_name = default_base_image_name
        else:
            raise ValueError("错误：输入的基准图片编号格式不正确！")
    except ValueError as ve:
        print(ve)
        return None

    return base_image_name


def main():
    """
    主函数，用于处理图片。
    """
    folder_name = get_folder_name()
    if not folder_name:
        return

    base_image_name = get_base_image_name()
    if not base_image_name:
        return

    base_image_path, json_path = get_base_image_and_json_path(folder_name, base_image_name)
    if base_image_path and json_path:
        process_images(base_image_path, json_path)


if __name__ == "__main__":
    main()
