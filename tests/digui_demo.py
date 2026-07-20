import time
import uuid


def recursive_replace(data):
    """
    大厂测开标准：递归替换复杂请求体中的动态变量
    """
    # 场景 1：如果这一层是个字典，扫一遍它的 key-value
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                # 如果值还是字典或列表，递归进去继续扫
                recursive_replace(value)
            elif isinstance(value, str):
                # 遇到了字符串，进行精准替换
                if value == "#time#":
                    data[key] = str(int(time.time() * 1000))
                elif value == "#sessionUUID#":
                    data[key] = str(uuid.uuid4())

    # 场景 2：如果这一层是个列表，遍历列表里的每一个元素
    elif isinstance(data, list):
        for index, item in enumerate(data):
            if isinstance(item, (dict, list)):
                # 递归进去
                recursive_replace(item)
            elif isinstance(item, str):
                if item == "#time#":
                    data[index] = str(int(time.time() * 1000))
                elif item == "#sessionUUID#":
                    data[index] = str(uuid.uuid4())

    return data


# ======= 测试这个测开级工具 =======
nested_request_body = {
    "action": "create_order",
    "timestamp": "#time#",  # 第一层
    "order_info": {
        "device_id": "phone_01",
        "meta_data": {
            "trace_id": "#sessionUUID#",  # 第三层嵌套
            "items": [
                {"item_id": 101, "item_time": "#time#"},  # 列表套字典里的第四层
            ]
        }
    }
}

# 运行替换
processed_body = recursive_replace(nested_request_body)
import pprint

pprint.pprint(processed_body)