#!/usr/bin/env python3
# Java zu JavaScript Konverter GUI
# Die Benutzeroberfläche für den Java zu JavaScript Konverter

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sys
import os

# Importieren der Konverterlogik aus separater Datei
from java_to_js_converter import JavaToJSConverter


class JavaToJSApp:
    def __init__(self, root):
        self.root = root
        self.converter = JavaToJSConverter()
        self.setup_ui()
        
    def setup_ui(self):
        """Erstellt die GUI-Elemente"""
        self.root.title("Java zu JavaScript Konverter")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Hauptframe für alle Inhalte
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titelleiste
        title_label = ttk.Label(main_frame, text="Java zu JavaScript Konverter", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Eingabe- und Ausgabebereiche in Paned Window
        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Linke Seite - Java Code
        left_frame = ttk.LabelFrame(paned_window, text="Java Code")
        paned_window.add(left_frame, weight=1)
        
        # Editor für Java Code
        self.java_editor = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, font=("Courier", 12))
        self.java_editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Rechte Seite - JavaScript Code
        right_frame = ttk.LabelFrame(paned_window, text="JavaScript Code")
        paned_window.add(right_frame, weight=1)
        
        # Editor für JavaScript Code
        self.js_editor = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, font=("Courier", 12))
        self.js_editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame für Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Buttons
        convert_button = ttk.Button(button_frame, text="Konvertieren", command=self.convert_code)
        convert_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(button_frame, text="Löschen", command=self.clear_editors)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        load_button = ttk.Button(button_frame, text="Java-Datei laden", command=self.load_java_file)
        load_button.pack(side=tk.LEFT, padx=5)
        
        save_button = ttk.Button(button_frame, text="JavaScript speichern", command=self.save_js_file)
        save_button.pack(side=tk.LEFT, padx=5)
        
        # Beispiel-Button
        example_button = ttk.Button(button_frame, text="Beispiel laden", command=self.load_example)
        example_button.pack(side=tk.RIGHT, padx=5)
        
        # Status-Leiste
        self.status_var = tk.StringVar()
        self.status_var.set("Bereit")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(5, 0))
        
        # Erstelle Beispielcode
        self.example_java_code = """public class HelloWorld {
    private String message;
    
    public HelloWorld(String message) {
        this.message = message;
    }
    
    public void sayHello() {
        System.out.println(message);
    }
    
    public String getMessage() {
        return this.message;
    }
    
    public void setMessage(String newMessage) {
        this.message = newMessage;
    }
    
    public static void main(String[] args) {
        HelloWorld hello = new HelloWorld("Hallo Welt!");
        hello.sayHello();
        
        for(int i = 0; i < 5; i++) {
            System.out.println("Zähler: " + i);
        }
        
        int[] numbers = new int[3];
        numbers[0] = 1;
        numbers[1] = 2;
        numbers[2] = 3;
    }
}"""
    
    def convert_code(self):
        """Konvertiert den Java-Code zu JavaScript"""
        java_code = self.java_editor.get("1.0", tk.END)
        if not java_code.strip():
            messagebox.showwarning("Warnung", "Bitte gib zuerst Java-Code ein!")
            return
            
        try:
            js_code = self.converter.convert_code(java_code)
            self.js_editor.delete("1.0", tk.END)
            self.js_editor.insert("1.0", js_code)
            self.status_var.set("Konvertierung erfolgreich!")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Konvertierung: {str(e)}")
            self.status_var.set("Fehler bei der Konvertierung!")
    
    def clear_editors(self):
        """Löscht den Inhalt beider Editoren"""
        self.java_editor.delete("1.0", tk.END)
        self.js_editor.delete("1.0", tk.END)
        self.status_var.set("Editoren geleert")
    
    def load_java_file(self):
        """Lädt eine Java-Datei in den Editor"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Java Dateien", "*.java"), ("Alle Dateien", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                self.java_editor.delete("1.0", tk.END)
                self.java_editor.insert("1.0", content)
                self.status_var.set(f"Datei geladen: {file_path}")
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Laden der Datei: {str(e)}")
    
    def save_js_file(self):
        """Speichert den konvertierten JavaScript-Code in eine Datei"""
        js_code = self.js_editor.get("1.0", tk.END)
        if not js_code.strip():
            messagebox.showwarning("Warnung", "Es gibt keinen JavaScript-Code zum Speichern!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".js",
            filetypes=[("JavaScript Dateien", "*.js"), ("Alle Dateien", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(js_code)
                self.status_var.set(f"JavaScript gespeichert in: {file_path}")
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Speichern der Datei: {str(e)}")
    
    def load_example(self):
        """Lädt den Beispielcode in den Java-Editor"""
        self.java_editor.delete("1.0", tk.END)
        self.java_editor.insert("1.0", self.example_java_code)
        self.status_var.set("Beispielcode geladen")


# Hauptfunktion zum Starten der GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = JavaToJSApp(root)
    root.mainloop()