import os
import json
from typing import List, Any, Callable


def read_json_files(directory: str, filename: str = None) -> List[Any]:
    """
    从指定目录读取JSON文件（可指定具体文件），并将内容合并为一个列表返回

    Args:
        directory: 包含JSON文件的目录路径
        filename: 可选参数，指定要读取的具体文件名（含扩展名）。
                  如果为None，则读取目录下所有JSON文件

    Returns:
        所有指定JSON文件内容合并后的列表

    Raises:
        FileNotFoundError: 如果指定目录或文件不存在
        json.JSONDecodeError: 如果JSON文件格式不正确
    """
    res_list = []

    # 检查目录是否存在
    if not os.path.exists(directory):
        raise FileNotFoundError(f"目录不存在: {directory}")

    # 处理指定文件的情况
    if filename:
        if not filename.endswith('.json'):
            print(f"警告: {filename} 不是JSON文件，将尝试读取")

        file_path = os.path.join(directory, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                if isinstance(json_data, list):
                    res_list.extend(json_data)
                else:
                    res_list.append(json_data)
            print(f"成功读取文件: {filename}")
        except json.JSONDecodeError as e:
            print(f"JSON解析错误 in {filename}: {str(e)}")
        except Exception as e:
            print(f"读取文件 {filename} 时出错: {str(e)}")

        return res_list


def write_if_not_exists(
        res_list: List[Any],
        new_data: Any,
        output_file: str,
        exists_checker: Callable[[List[Any], Any], bool] = None
) -> bool:
    """
    检查新数据是否已存在（可通过自定义逻辑），如果不存在则写入到输出文件

    Args:
        res_list: 已有的数据列表
        new_data: 要检查和写入的新数据
        output_file: 用于写入新数据的文件路径
        exists_checker: 可选参数，自定义存在性判断函数。
                        接收参数: (现有数据列表, 新数据)
                        返回值: 布尔值（True表示存在，False表示不存在）
                        如果为None，将使用默认的 'in' 操作符判断

    Returns:
        如果数据被写入则返回True，否则返回False
    """
    # 确定存在性检查函数
    if exists_checker is None:
        # 默认检查逻辑
        def default_checker(existing_list, data):
            return data in existing_list

        exists_checker = default_checker

    # 检查新数据是否已存在于原始数据列表中
    if exists_checker(res_list, new_data):
        print("数据已存在于原始列表中，不进行写入")
        return False

    try:
        # 检查输出文件是否存在，如果存在则读取现有内容
        existing_data = []
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]

        # 检查新数据是否已在输出文件中
        if exists_checker(existing_data, new_data):
            print("数据已在输出文件中，不进行写入")
            return False

        # 将新数据添加到现有数据
        existing_data.append(new_data)

        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, indent=2, ensure_ascii=False)
            file.write('\n')

        print(f"数据已成功写入到 {output_file}")
        return True

    except Exception as e:
        print(f"写入文件时出错: {str(e)}")
        return False
