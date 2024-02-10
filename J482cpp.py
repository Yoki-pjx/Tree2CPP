import re

def convert_to_cpp_with_correct_structure(lines):
    cpp_code = []
    current_indent = 0
    indent_unit = '    '  # 使用4个空格进行缩进

    for line in lines:
        indent_level = line.count('|')  # 计算缩进级别
        line_content = line.strip('| \n')
        # cpp_code.append(f"{indent_level}\n")

        while current_indent > indent_level:
            current_indent -= 1
            cpp_code.append(f"{indent_unit * (current_indent)}}}\n")
            
            

        # 判断这一行是条件还是决策
        if ':' in line_content:
            # 分离条件判断和决策部分
            condition, decision_part = line_content.split(':')
            condition = condition.strip()
            
            # 进一步分离决策值和注释
            decision, comment = decision_part.strip().split(' ', 1)
            comment = comment.strip('() ')  # 去除括号和多余的空格

            # 处理if或else语句
            if '<=' in condition:
                cpp_code.append(f"{indent_unit * indent_level}if ({condition}) {{\n")
                cpp_code.append(f"{indent_unit * (indent_level + 1)}return {decision}; /* ({comment}) */\n")
                cpp_code.append(f"{indent_unit * indent_level}}}\n")
            elif '>' in condition:
                # cpp_code.append(f"{indent_unit * indent_level}}}\n")
                cpp_code.append(f"{indent_unit * indent_level}else {{\n")
                cpp_code.append(f"{indent_unit * (indent_level + 1)}return {decision}; /* ({comment}) */\n")
                cpp_code.append(f"{indent_unit * indent_level}}}\n")
            current_indent = indent_level
            # cpp_code.append(f"{current_indent}\n")

        else:
            # 为普通条件添加if或else语句
            condition = line_content
            if '<=' in condition:
                cpp_code.append(f"{indent_unit * indent_level}if ({condition}) {{\n")
                current_indent = indent_level
            elif '>' in condition:
                cpp_code.append(f"{indent_unit * indent_level}else {{\n")
                current_indent = indent_level

    # 关闭任何剩余的未闭合块
    while current_indent > 0:
        current_indent -= 1
        cpp_code.append(f"{indent_unit * current_indent}}}\n")

    return "".join(cpp_code)


def ensure_float_literals(cpp_code):
    # 正则表达式用于确保浮点数后面跟有 'f' 后缀
    float_literals_regex = re.compile(r'(?<!\w)(\d+\.\d+)(?![f\d])')
    float_literals_with_f = re.sub(float_literals_regex, r'\1f', cpp_code)
    return float_literals_with_f

# 从文件中读取决策树
file_path = './Corridor/J48.txt'
with open(file_path, 'r') as file:
    lines = file.readlines()

# 将决策树转换为C++的if-else语句，并具有正确的结构
cpp_code = convert_to_cpp_with_correct_structure(lines)

#确保所有浮点数后面正确加上 'f' 后缀
cpp_code_with_floats = ensure_float_literals(cpp_code)

#将C++代码保存到文件中
output_file_path = './Corridor/convertedj48.cpp'
with open(output_file_path, 'w') as cpp_file:
    cpp_file.write(cpp_code_with_floats)

print("转换完成。C++代码已保存到", output_file_path)