import re

def convert_to_cpp_with_correct_structure(lines):
    cpp_code = []
    current_indent = 0
    indent_unit = '    '  

    for line in lines:
        indent_level = line.count('|')  
        line_content = line.strip('| \n')
        # cpp_code.append(f"{indent_level}\n")

        while current_indent > indent_level:
            current_indent -= 1
            cpp_code.append(f"{indent_unit * (current_indent)}}}\n")

        if ':' in line_content:
            condition, decision_part = line_content.split(':')
            condition = condition.strip()
            
            decision, comment = decision_part.strip().split(' ', 1)
            comment = comment.strip('() ')  

            if '<' in condition:
                cpp_code.append(f"{indent_unit * indent_level}if ({condition}) {{\n")
                cpp_code.append(f"{indent_unit * (indent_level + 1)}return {decision}; /* ({comment}) */\n")
                cpp_code.append(f"{indent_unit * indent_level}}}\n")
            elif '>=' in condition:
                # cpp_code.append(f"{indent_unit * indent_level}}}\n")
                cpp_code.append(f"{indent_unit * indent_level}else {{\n")
                cpp_code.append(f"{indent_unit * (indent_level + 1)}return {decision}; /* ({comment}) */\n")
                cpp_code.append(f"{indent_unit * indent_level}}}\n")
            current_indent = indent_level
            # cpp_code.append(f"{current_indent}\n")

        else:
            condition = line_content
            if '<' in condition:
                cpp_code.append(f"{indent_unit * indent_level}if ({condition}) {{\n")
                current_indent = indent_level
            elif '>=' in condition:
                cpp_code.append(f"{indent_unit * indent_level}else {{\n")
                current_indent = indent_level

    while current_indent > 0:
        current_indent -= 1
        cpp_code.append(f"{indent_unit * current_indent}}}\n")

    return "".join(cpp_code)


def ensure_float_literals(cpp_code):
    float_literals_regex = re.compile(r'(?<!\w)(\d+\.\d+)(?![f\d])')
    float_literals_with_f = re.sub(float_literals_regex, r'\1f', cpp_code)
    return float_literals_with_f

file_path = './model_REPTree.txt'
with open(file_path, 'r') as file:
    lines = file.readlines()

cpp_code = convert_to_cpp_with_correct_structure(lines)

cpp_code_with_floats = ensure_float_literals(cpp_code)

output_file_path = './ConvertedREPTree.cpp'
with open(output_file_path, 'w') as cpp_file:
    cpp_file.write(cpp_code_with_floats)

print("Completed", output_file_path)
