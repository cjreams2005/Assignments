class StyleChecker:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lines = []
        self.report = []

    def read_file(self):
        with open(self.file_path, 'r') as file:
            self.lines = file.readlines()

    def analyze(self):
        self.read_file()
        self.report.append(f"Analyzing {self.file_path}\n")
        self.report.append(f"Total Lines: {len(self.lines)}\n")
        self.report.append("Imports:\n")
        self.report.append(self._get_imports())
        self.report.append("\nClasses:\n")
        self.report.append(self._get_classes())
        self.report.append("\nFunctions:\n")
        self.report.append(self._get_functions())
        self.report.append("\nDocStrings:\n")
        self.report.append(self._get_docstrings())
        self.report.append("\nType Annotation Check:\n")
        self.report.append(self._check_type_annotations())
        self.report.append("\nNaming Convention Check:\n")
        self.report.append(self._check_naming_conventions())

    def _get_imports(self):
        imports = [line.strip() for line in self.lines if line.startswith('import') or line.startswith('from')]
        return '\n'.join(imports) if imports else "No imports found."

    def _get_classes(self):
        classes = [line.split()[1].split('(')[0] for line in self.lines if line.strip().startswith('class ')]
        return '\n'.join(classes) if classes else "No classes found."

    def _get_functions(self):
        functions = [line.split()[1].split('(')[0] for line in self.lines if line.strip().startswith('def ')]
        return '\n'.join(functions) if functions else "No functions found."

    def _get_docstrings(self):
        docstrings = []
        in_docstring = False
        docstring = ''
        current_entity = None

        for line in self.lines:
            line_strip = line.strip()
            if line_strip.startswith('class '):
                if current_entity:
                    docstrings.append(f"{current_entity}: DocString not found\n")
                current_entity = line_strip.split()[1].split('(')[0]
                in_docstring = False
            elif line_strip.startswith('def '):
                if current_entity:
                    docstrings.append(f"{current_entity}: DocString not found\n")
                current_entity = line_strip.split()[1].split('(')[0]
                in_docstring = False
            elif '"""' in line_strip or "'''" in line_strip:
                if not in_docstring:
                    in_docstring = True
                    docstring = line_strip.strip('"""').strip("'''")
                else:
                    in_docstring = False
                    docstring += ' ' + line_strip.strip('"""').strip("'''")
                    docstrings.append(f"{current_entity}: {docstring}\n")
                    current_entity = None
                    docstring = ''
            elif in_docstring:
                docstring += ' ' + line_strip

        if current_entity:
            docstrings.append(f"{current_entity}: DocString not found\n")

        return '\n'.join(docstrings)

    def _check_type_annotations(self):
        functions = [line.split()[1].split('(')[0] for line in self.lines if line.strip().startswith('def ')]
        unannotated_funcs = [func for func in functions if not (':' in func or '->' in func)]
        if unannotated_funcs:
            return '\n'.join(unannotated_funcs)
        return "All functions and methods use type annotations."

    def _check_naming_conventions(self):
        incorrect_names = []
        for line in self.lines:
            if line.strip().startswith('class '):
                class_name = line.split()[1].split('(')[0]
                if not class_name[0].isupper():
                    incorrect_names.append(f"Class {class_name} does not use CamelCase.")
            if line.strip().startswith('def '):
                func_name = line.split()[1].split('(')[0]
                if '_' not in func_name:
                    incorrect_names.append(f"Function {func_name} does not use lower_case_with_underscores.")
        if not incorrect_names:
            return "All names adhere to the specified naming conventions."
        return '\n'.join(incorrect_names)

    def generate_report(self):
        report_file = f"style_report_{self.file_path.split('/')[-1].split('.')[0]}.txt"
        with open(report_file, 'w') as file:
            file.write('\n'.join(self.report))
        print(f"Report generated: {report_file}")

if __name__ == '__main__':
    checker = StyleChecker('ceaser.py')
    checker.analyze()
    checker.generate_report()