from dataclasses import dataclass
from typing import List, Dict, Optional, Callable, Any
import re


@dataclass
class PascalProc:
    name: str
    vars: Dict[str, str]
    body: List[str]
    is_program: bool = False


class SimplePascalTranslator:

    def __init__(self):
        self.type_map = {
            'integer': 'int',
            'real': 'float',
            'boolean': 'bool',
            'char': 'str',
            'string': 'str'
        }
        self.current_indent = "    "

    def translate_type(self, pascal_type):
        t = pascal_type.lower().strip(';').strip()
        return self.type_map.get(t, 'Any')

    def parse_procedure(self, source):
        """
        ожидает чёткую структуру
        program / procedure имя;
        var
          x: integer;
          y: real;
        begin
          ...
        end.
        """
        lines = [line.strip() for line in source.split('\n') if line.strip() and not line.strip().startswith('//')]
        if not lines:
            raise ValueError("Пустой код")

        header = lines[0].lower()
        is_program = header.startswith('program ')
        name_match = re.match(r'(program|procedure)\s+(\w+)', header, re.I)
        if not name_match:
            raise ValueError("Ожидалось program или procedure")

        name = name_match.group(2)
        proc = PascalProc(name=name, vars={}, body=[], is_program=is_program)

        # ищем секцию var
        in_var_section = False
        in_begin = False

        for line in lines[1:]:
            l = line.lower()

            if l.startswith('var'):
                in_var_section = True
                continue

            if l.startswith('begin'):
                in_var_section = False
                in_begin = True
                continue

            if l.startswith('end') and (l.endswith('.') or l.endswith(';')):
                break

            if in_var_section and ':' in line:
                parts = [p.strip() for p in line.split(':')]
                if len(parts) != 2:
                    continue
                var_names = [v.strip() for v in parts[0].split(',')]
                var_type = parts[1].rstrip(';').strip()
                for v in var_names:
                    if v:
                        proc.vars[v] = var_type

            if in_begin:
                proc.body.append(line)

        return proc

    def translate_to_python(self, proc):
        code = []

        # заголовок
        if proc.is_program:
            code.append(f"def main():")
        else:
            code.append(f"def {proc.name}():")

        indent = self.current_indent

        # объявления переменных
        if proc.vars:
            code.append(f"{indent}")
            for var, typ in proc.vars.items():
                py_type = self.translate_type(typ)
                code.append(f"{indent}{var}: {py_type} = 0")

        code.append("")

        for line in proc.body:
            stripped = line.strip()
            if stripped.lower() in ('begin', 'end;', 'end.'):
                continue

            if stripped.lower().startswith('repeat'):
                code.append(f"{indent}while True:")
                indent += self.current_indent
                continue

            if stripped.lower().startswith('until '):
                condition = stripped[6:].rstrip(';').strip()
                py_cond = self._translate_condition(condition)
                code.append(f"{indent.rstrip()}    if {py_cond}:")
                code.append(f"{indent}        break")
                indent = indent[:-len(self.current_indent)]
                continue

            if stripped.lower().startswith('case '):
                expr = stripped[5:].rstrip(' of').strip()
                code.append(f"{indent}match {expr}:")
                indent += self.current_indent
                continue

            if stripped == 'end;':
                indent = indent[:-len(self.current_indent)]
                continue

            if stripped.endswith(':') and stripped.rstrip(':').isdigit():
                case_val = stripped.rstrip(':').strip()
                code.append(f"{indent}    case {case_val}:")
                indent += self.current_indent
                continue

            translated = self._translate_line(stripped)
            if translated:
                code.append(f"{indent}{translated}")

        if proc.is_program:
            code.append("")
            code.append("if __name__ == '__main__':")
            code.append("    main()")

        return "\n".join(code)

    def _translate_condition(self, cond):
        cond = cond.replace('<>', '!=')
        cond = cond.replace('=', '==')
        cond = cond.replace('and', 'and')
        cond = cond.replace('or', 'or')
        cond = cond.replace('not', 'not ')
        return cond

    def _translate_line(self, line):
        if not line:
            return None

        line = line.rstrip(';').strip()

        if line.lower().startswith('writeln'):
            arg = line[7:].strip('()').strip()
            return f"print({arg})"

        if line.lower().startswith('write'):
            arg = line[5:].strip('()').strip()
            return f"print({arg}, end='')"

        if line.lower().startswith('readln'):
            var = line[6:].strip('()').strip()
            return f"{var} = input()"

        if ':=' in line:
            var, expr = [p.strip() for p in line.split(':=', 1)]
            return f"{var} = {expr}"

        return line

    def translate(self, pascal_code):
        proc = self.parse_procedure(pascal_code)
        return self.translate_to_python(proc)


def demo():
    translator = SimplePascalTranslator()

    pascal1 = """
program Example1;
var
  a, b: integer;
  s: string;
begin
  a := 10;
  b := 25;
  writeln('Сумма = ', a + b);
  s := 'Hello';
  writeln(s);
end.
"""

    print("Python:")
    print(translator.translate(pascal1))
    print("\n" + "─"*60)

if __name__ == "__main__":
    demo()
