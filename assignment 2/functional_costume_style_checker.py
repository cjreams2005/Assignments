import os
import sys

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def get_imports(lines):
    imports = [line.strip() for line in lines if line.startswith('import') or line.startswith('from')]
    return imports if imports else ["No imports found."]

def get_classes(lines):
    classes = [line.split()[1].split('(')[0] for line in lines if line.strip().startswith('class ')]
    return classes if classes else ["No classes found."]

def get_functions(lines):
    functions = [line.split()[1].split('(')[0] for line in lines if line.strip().startswith('def ')]
    return functions if functions else ["No functions found."]

def get_docstrings(lines):
    docstrings = []
    in_docstring = False
    docstring = ''
    current_entity = None

    for line in lines:
        line_strip = line.strip()
        if line_strip.startswith('class '):
            if current_entity:
                docstrings.append(f"{current_entity}: DocString not found")
            current_entity = line_strip.split()[1].split('(')[0]
            in_docstring = False
        elif line_strip.startswith('def '):
            if current_entity:
                docstrings.append(f"{current_entity}: DocString not found")
            current_entity = line_strip.split()[1].split('(')[0]
            in_docstring = False
        elif '"""' in line_strip or "'''" in line_strip:
            if not in_docstring:
                in_docstring = True
                docstring = line_strip.strip('"""').strip("'''")
            else:
                in_docstring = False
                docstring += ' ' + line_strip.strip('"""').strip("'''")
                docstrings.append(f"{current_entity}: {docstring}")
                current_entity = None
                docstring = ''
        elif in_docstring:
            docstring += ' ' + line_strip

    if current_entity:
        docstrings.append(f"{current_entity}: DocString not found")

    return docstrings

def check_type_annotations(lines):
    unannotated_funcs = []
    in_function = False

    for line in lines:
        if line.strip().startswith('def '):
            in_function = True
            function_signature = line.strip()
            if ':' not in function_signature or '->' not in function_signature:
                function_name = function_signature.split('(')[0].split()[1]
                unannotated_funcs.append(f"{function_name} is missing type annotations.")
        elif in_function and (line.strip().endswith(':') or line.strip().startswith('@')):
            continue
        else:
            in_function = False

    return unannotated_funcs if unannotated_funcs else ["All functions and methods use type annotations."]

def check_naming_conventions(lines):
    incorrect_names = []
    for line in lines:
        if line.strip().startswith('class '):
            class_name = line.split()[1].split('(')[0]
            if not class_name[0].isupper():
                incorrect_names.append(f"Class {class_name} does not use CamelCase.")
        if line.strip().startswith('def '):
            func_name = line.split()[1].split('(')[0]
            if '_' not in func_name and not func_name.islower():
                incorrect_names.append(f"Function {func_name} does not use lower_case_with_underscores.")
    return incorrect_names if incorrect_names else ["All names adhere to the specified naming conventions."]

def generate_report(file_path, report):
    report_file = os.path.join(os.path.dirname(file_path), f"style_report_{os.path.basename(file_path).split('.')[0]}.txt")
    with open(report_file, 'w') as file:
        file.write('\n'.join(report))
    print(f"Report generated: {report_file}")

def analyze_file(file_path):
    lines = read_file(file_path)
    report = [
        f"Analyzing {file_path}",
        f"Total Lines: {len(lines)}",
        "Imports:",
        '\n'.join(get_imports(lines)),
        "Classes:",
        '\n'.join(get_classes(lines)),
        "Functions:",
        '\n'.join(get_functions(lines)),
        "DocStrings:",
        '\n'.join(get_docstrings(lines)),
        "Type Annotation Check:",
        '\n'.join(check_type_annotations(lines)),
        "Naming Convention Check:",
        '\n'.join(check_naming_conventions(lines))
    ]
    generate_report(file_path, report)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("Enter the path to the Python source file: ")
    analyze_file(file_path)
