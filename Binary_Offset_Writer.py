import tkinter as tk
from tkinter import filedialog, messagebox
import os
import struct
import subprocess
import sys

class OffsetWriterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary Offset Writer")

        self.binary_path = None
        self.offset_map = {}
        self.selected_option = tk.StringVar()

        self.create_widgets()
        self.center_window(400, 120)
        self.load_binary_file()

    def create_widgets(self):
        self.option_menu = tk.OptionMenu(self.root, self.selected_option, ())
        self.option_menu.grid(row=0, column=0, padx=10, pady=10)

        self.write_button = tk.Button(self.root, text="Write data to offset", command=self.write_data_to_offset)
        self.write_button.grid(row=0, column=1, padx=10, pady=10)

        self.open_button = tk.Button(self.root, text="Open Binary File", command=self.open_binary_file)
        self.open_button.grid(row=1, column=0, padx=10, pady=5)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.grid(row=1, column=1, padx=10, pady=5)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def load_binary_file(self):
        filetypes = [("Binary files", "*.so *.bin"), ("All files", "*.*")]
        self.binary_path = filedialog.askopenfilename(title="Select binary file", filetypes=filetypes)

        if not self.binary_path:
            self.root.quit()
            return

        offset_path = os.path.splitext(self.binary_path)[0] + ".txt"
        if not os.path.exists(offset_path):
            offset_path = filedialog.askopenfilename(title="Select offset map file", filetypes=[("Text files", "*.txt")])
            if not offset_path:
                messagebox.showerror("Error", "Offset map file not selected.")
                self.root.quit()
                return

        self.parse_offset_file(offset_path)

    def parse_offset_file(self, path):
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or '|' not in line:
                    continue
                parts = line.split('|')
                name = parts[0].strip()
                offsets = [int(x, 16) for x in parts[1].split(',')]
                length = int(parts[2], 16)
                self.offset_map[name] = (offsets, length)

        if self.offset_map:
            self.selected_option.set(next(iter(self.offset_map)))
            menu = self.option_menu["menu"]
            menu.delete(0, "end")
            for key in self.offset_map:
                menu.add_command(label=key, command=tk._setit(self.selected_option, key))

    def write_data_to_offset(self):
        if not self.binary_path or not self.selected_option.get():
            return

        name = self.selected_option.get()
        offsets, length = self.offset_map[name]

        # Check for file with same name in binary directory
        bin_dir = os.path.dirname(self.binary_path)
        default_data_path = os.path.join(bin_dir, name + ".bin")

        if not os.path.exists(default_data_path):
            default_data_path = filedialog.askopenfilename(title=f"Select data file for {name}", filetypes=[("Binary files", "*.bin"), ("All files", "*.*")])
            if not default_data_path:
                messagebox.showwarning("Cancelled", "Data file not selected.")
                return

        with open(default_data_path, 'rb') as df:
            data = df.read()
            if data.startswith(b"\x82\x00\x00\x00"):
                data = data[4:]

        if len(data) < length:
            messagebox.showerror("Error", f"Data length ({len(data)}) is shorter than required length ({length})")
            return

        with open(self.binary_path, 'r+b') as bf:
            for offset in offsets:
                bf.seek(offset)
                bf.write(data[:length])

        messagebox.showinfo("Success", f"Data written to {len(offsets)} offset(s).")

    def open_binary_file(self):
        if not self.binary_path:
            messagebox.showwarning("No file", "Binary file not loaded.")
            return

        try:
            if sys.platform.startswith('darwin'):
                subprocess.call(('open', self.binary_path))
            elif os.name == 'nt':
                os.startfile(self.binary_path)
            elif os.name == 'posix':
                subprocess.call(('xdg-open', self.binary_path))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = OffsetWriterApp(root)
    root.mainloop()
