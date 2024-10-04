import tkinter as tk
import hashlib
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename

def get_file():
    filepath = askopenfilename()
    file_path.set(filepath)

def clear_all():
    file_path.set("")
    data_entry.delete("1.0", "end")
    result.configure(foreground="")
    check_result.set("Ready")

def get_hash(file_path, hash_type):
    try:
        hash_obj = hashlib.new(hash_type)
        with open(file_path, "rb") as file:
            for block in iter(lambda: file.read(4096), b""):
                hash_obj.update(block)
        return hash_obj.hexdigest()
    except FileNotFoundError:
        messagebox.showerror("Error", "The specified file could not be found.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    return None

def compare_hashes():
    filepath = file_path.get()
    if not filepath:
        result.configure(foreground="red")
        check_result.set("No file has been selected!")
        return

    user_hash = data_entry.get("1.0", "end").strip()
    if not user_hash:
        result.configure(foreground="red")
        check_result.set("No checksum has been entered!")
        return

    hash_type = hash_type_var.get().lower()
    computed_hash = get_hash(filepath, hash_type)
    if computed_hash is None:
        check_result.set("Error while checking!")
        result.configure(foreground="red")
    elif user_hash == computed_hash:
        result.configure(foreground="green")
        check_result.set("Checksums match!")
    else:
        result.configure(foreground="red")
        check_result.set("The checksums do not match!")

main = tk.Tk()
main.title("Hashr")
main.resizable(width=False, height=False)

check_result = tk.StringVar()
check_result.set("Ready")

file_path = tk.StringVar()
file_path.set("")

data_label = ttk.Label(main, text="The checksum to be checked:")
data_label.pack(padx=5, pady=5)

data_entry = tk.Text(main, width=50, height=3, wrap="char")
data_entry.pack(padx=5, pady=5)

hash_type_var = tk.StringVar(value="SHA256")
hash_types = ["MD5", "SHA1", "SHA256", "SHA512"]
hash_type_label = ttk.Label(main, text="Select checksum type:")
hash_type_label.pack(padx=5, pady=5)
hash_type_combo = ttk.Combobox(main, textvariable=hash_type_var, values=hash_types, state="readonly")
hash_type_combo.pack(padx=5, pady=5)

separator = ttk.Separator(main, orient='horizontal')
separator.pack(fill='x', padx=5, pady=5)

file_label = ttk.Label(main, text="File to be checked:")
file_label.pack(padx=5, pady=5)

file_entry = ttk.Label(main, textvariable=file_path, anchor="center")
file_entry.pack(fill="x", padx=5, pady=5)

button_open = ttk.Button(main, text="Select file", command=get_file)
button_open.pack(padx=5, pady=5)

separator = ttk.Separator(main, orient='horizontal')
separator.pack(fill='x', padx=5, pady=5)

result = ttk.Label(main, textvariable=check_result, anchor="center")
result.pack(fill="x", padx=5, pady=5)

button_check = ttk.Button(main, text="Check", command=compare_hashes)
button_check.pack(padx=5, pady=5)

separator = ttk.Separator(main, orient='horizontal')
separator.pack(fill='x', padx=5, pady=5)

button_clear = ttk.Button(main, text="Clear", command=clear_all)
button_clear.pack(padx=5, pady=5)

button_exit = ttk.Button(main, text="Exit", command=main.destroy)
button_exit.pack(padx=5, pady=5)

main.mainloop()