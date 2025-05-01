#!/usr/bin/env python3
# Java zu JavaScript Konverter
# Ein Parser, der grundlegenden Java-Code in JavaScript umwandelt

import re
import sys
import os


class JavaToJSConverter:
    def __init__(self):
        # Hinzufügen von speziellen Mustern für Java-Sprachkonstrukte
        self.patterns = {
            # Klassendefinitionen
            "class_definition": (
                r"public\s+class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([\w,\s]+))?\s*{",
                self._convert_class
            ),
            # Methoden
            "method": (
                r"(public|private|protected)?\s*(static)?\s*(\w+)\s+(\w+)\s*\((.*?)\)\s*{",
                self._convert_method
            ),
            # Datentypen in Deklarationen
            "variable_declaration": (
                r"(int|boolean|String|double|float|long|char|byte|short)\s+(\w+)\s*=\s*(.*?);",
                self._convert_variable
            ),
            # For-Schleifen
            "for_loop": (
                r"for\s*\(\s*(int\s+)?(\w+)\s*=\s*(.+?)\s*;\s*(.+?)\s*;\s*(.+?)\s*\)",
                self._convert_for_loop
            ),
            # System.out.println
            "print": (
                r"System\.out\.println\((.*?)\);",
                self._convert_print
            ),
            # Import-Anweisungen entfernen
            "import": (
                r"import\s+[\w\.]+;",
                lambda match: "// " + match.group(0)
            ),
            # Arrays
            "array_declaration": (
                r"(\w+)\[\]\s+(\w+)\s*=\s*new\s+\w+\[(\d+)\];",
                self._convert_array
            ),
            # ArrayList
            "arraylist": (
                r"ArrayList<(\w+)>\s+(\w+)\s*=\s*new\s+ArrayList<\w*>\(\);",
                self._convert_arraylist
            ),
            # main-Methode
            "main_method": (
                r"public\s+static\s+void\s+main\s*\(\s*String\s*\[\]\s*\w+\s*\)",
                lambda match: "function main()"
            ),
            # Getter und Setter
            "getter": (
                r"public\s+(\w+)\s+get(\w+)\(\)\s*{[\s\n]*return\s+this\.(\w+);[\s\n]*}",
                self._convert_getter
            ),
            "setter": (
                r"public\s+void\s+set(\w+)\((\w+)\s+(\w+)\)\s*{[\s\n]*this\.(\w+)\s*=\s*\w+;[\s\n]*}",
                self._convert_setter
            ),
            # Type Cast
            "typecast": (
                r"\(\s*(\w+)\s*\)\s*(\w+)",
                lambda match: match.group(2)  # Einfach den Cast entfernen
            ),
            # Interface-Definitionen
            "interface": (
                r"public\s+interface\s+(\w+)\s*{",
                self._convert_interface
            ),
        }

    def _convert_class(self, match):
        class_name = match.group(1)
        parent = match.group(2)
        interfaces = match.group(3)
        
        result = f"class {class_name} "
        if parent:
            result += f"extends {parent} "
        
        result += "{"
        return result

    def _convert_method(self, match):
        access = match.group(1) or ""
        static = match.group(2) or ""
        return_type = match.group(3)
        method_name = match.group(4)
        params = match.group(5)
        
        # Entferne Datentypen aus Parametern
        params_js = []
        if params.strip():
            for param in params.split(","):
                parts = param.strip().split()
                if len(parts) > 1:
                    params_js.append(parts[-1])  # Nimm nur den Namen, nicht den Typ
                else:
                    params_js.append(parts[0])
                    
        params_str = ", ".join(params_js)
        
        if static:
            return f"static {method_name}({params_str}) {{"
        else:
            return f"{method_name}({params_str}) {{"

    def _convert_variable(self, match):
        data_type = match.group(1)
        var_name = match.group(2)
        value = match.group(3)
        
        # Boolean-Werte anpassen
        if value == "true" or value == "false":
            pass  # Diese sind in JS gleich
        # String-Handhabung ist in beiden Sprachen ähnlich
        
        return f"let {var_name} = {value};"

    def _convert_for_loop(self, match):
        has_type = match.group(1) is not None
        var = match.group(2)
        init = match.group(3)
        condition = match.group(4)
        increment = match.group(5)
        
        if has_type:
            return f"for (let {var} = {init}; {condition}; {increment})"
        else:
            return f"for ({var} = {init}; {condition}; {increment})"

    def _convert_print(self, match):
        content = match.group(1)
        return f"console.log({content});"

    def _convert_array(self, match):
        type_name = match.group(1)
        var_name = match.group(2)
        size = match.group(3)
        
        return f"let {var_name} = new Array({size});"

    def _convert_arraylist(self, match):
        type_name = match.group(1)
        var_name = match.group(2)
        
        return f"let {var_name} = [];"

    def _convert_getter(self, match):
        return_type = match.group(1)
        prop_name = match.group(2)
        prop_name = prop_name[0].lower() + prop_name[1:]  # camelCase
        internal_prop = match.group(3)
        
        return f"get {prop_name}() {{ return this.{internal_prop}; }}"

    def _convert_setter(self, match):
        prop_name = match.group(1)
        prop_name = prop_name[0].lower() + prop_name[1:]  # camelCase
        param_type = match.group(2)
        param_name = match.group(3)
        internal_prop = match.group(4)
        
        return f"set {prop_name}({param_name}) {{ this.{internal_prop} = {param_name}; }}"

    def _convert_interface(self, match):
        interface_name = match.group(1)
        return f"// Interface {interface_name} converted to class\nclass {interface_name} {{"

    def convert_file(self, input_file, output_file=None):
        """Konvertiert eine Java-Datei in JavaScript."""
        if not os.path.exists(input_file):
            print(f"Fehler: Die Datei {input_file} existiert nicht.")
            return False, "Datei existiert nicht"

        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                java_code = f.read()
        except Exception as e:
            print(f"Fehler beim Lesen der Datei: {e}")
            return False, f"Fehler beim Lesen: {e}"

        js_code = self.convert_code(java_code)

        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(js_code)
                print(f"JavaScript-Code wurde in {output_file} gespeichert.")
            except Exception as e:
                print(f"Fehler beim Schreiben der Datei: {e}")
                return False, f"Fehler beim Schreiben: {e}"
        else:
            print(js_code)
        
        return True, js_code

    def convert_code(self, java_code):
        """Konvertiert Java-Code-String in JavaScript-Code."""
        js_code = java_code
        
        # Ersetzt Standard-Java-Konstrukte durch JavaScript-Äquivalente
        for pattern_name, (pattern, replacement_func) in self.patterns.items():
            js_code = re.sub(pattern, replacement_func, js_code)
        
        # Zusätzliche häufige Ersetzungen
        replacements = [
            # Primitive Typen in Deklarationen entfernen
            (r"(int|boolean|String|double|float|long|char)\s+(\w+)\s*;", r"let \2;"),
            # Öffentliche Klassenvariablen
            (r"public\s+(int|boolean|String|double|float|long|char)\s+(\w+)\s*;", r"\2;"),
            # Private Klassenvariablen 
            (r"private\s+(int|boolean|String|double|float|long|char)\s+(\w+)\s*;", r"#\2;"),
            # Methoden mit Rückgabetyp void
            (r"public\s+void\s+(\w+)\s*\((.*?)\)", r"function \1(\2)"),
            # .length für Arrays
            (r"(\w+)\.length", r"\1.length"),
            # this.variable in Klassen
            (r"this\.(\w+)", r"this.\1"),
            # Konstruktordefinition
            (r"public\s+(\w+)\s*\((.*?)\)\s*{", r"constructor(\2) {"),
            # Entferne package-Deklarationen
            (r"package\s+[\w\.]+;", r"// Package information removed"),
            # Umwandlung von Java-Schlüsselwörtern
            (r"\bnew\s+(\w+)\s*\((.*?)\)", r"new \1(\2)"),
            # Java-Ausnahmebehandlung
            (r"try\s*{", r"try {"),
            (r"catch\s*\(\s*(\w+)\s+(\w+)\s*\)\s*{", r"catch(error) {"),
            (r"finally\s*{", r"finally {"),
            # Primitive Typ-Konvertierungen
            (r"Integer\.parseInt\((.*?)\)", r"parseInt(\1)"),
            (r"Double\.parseDouble\((.*?)\)", r"parseFloat(\1)"),
            (r"Float\.parseFloat\((.*?)\)", r"parseFloat(\1)"),
            (r"Boolean\.parseBoolean\((.*?)\)", r"Boolean(\1)"),
            # String-Methoden
            (r"\.equals\((.*?)\)", r" === \1"),
            (r"\.equalsIgnoreCase\((.*?)\)", r".toLowerCase() === \1.toLowerCase()"),
            (r"\.charAt\((.*?)\)", r".charAt(\1)"),
            (r"\.substring\((.*?)\)", r".substring(\1)"),
            # Entferne final-Schlüsselwort
            (r"\bfinal\s+", r""),
            # Static Initializer
            (r"static\s*{", r"static {"),
        ]
        
        for pattern, replacement in replacements:
            js_code = re.sub(pattern, replacement, js_code)
        
        # Füge Kommentar zur automatischen Konvertierung hinzu
        js_code = "// Automatisch konvertiert von Java zu JavaScript\n\n" + js_code
        
        return js_code


# Hauptfunktion für die Kommandozeilennutzung (falls die Datei direkt ausgeführt wird)
if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        
        converter = JavaToJSConverter()
        success, result = converter.convert_file(input_file, output_file)
        
        if not success:
            print(f"Fehler: {result}")
            sys.exit(1)
        
        sys.exit(0)
    else:
        print("Verwendung: java_to_js_converter.py input.java [output.js]")
        sys.exit(1)