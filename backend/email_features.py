import tkinter as tk
from tkinter import ttk, filedialog

class ComposeEmail:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user

    def setup(self):
        # Compose form
        form = ttk.Frame(self.parent)
        form.pack(padx=20, pady=20, fill="both", expand=True)

        ttk.Label(form, text="To:").grid(row=0, column=0, sticky="w")
        ttk.Entry(form).grid(row=0, column=1, sticky="ew")

        ttk.Label(form, text="Subject:").grid(row=1, column=0, sticky="w")
        ttk.Entry(form).grid(row=1, column=1, sticky="ew")

        # Rich text editor
        text_frame = ttk.Frame(form)
        text_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        
        toolbar = ttk.Frame(text_frame)
        toolbar.pack(fill="x")
        
        ttk.Button(toolbar, text="📎 Attach").pack(side="left")
        ttk.Button(toolbar, text="B", width=2).pack(side="left")
        ttk.Button(toolbar, text="I", width=2).pack(side="left")
        ttk.Button(toolbar, text="U", width=2).pack(side="left")
        
        text = tk.Text(text_frame, height=10)
        text.pack(fill="both", expand=True)

        # Action buttons
        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=3, column=0, columnspan=2)
        
        ttk.Button(btn_frame, text="Send").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Save Draft").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel").pack(side="left", padx=5)

class EmailInbox:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user

    def setup(self):
        # Toolbar
        toolbar = ttk.Frame(self.parent)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(toolbar, text="🔄 Refresh").pack(side="left", padx=2)
        ttk.Button(toolbar, text="📝 Compose").pack(side="left", padx=2)
        ttk.Button(toolbar, text="🗑️ Delete").pack(side="left", padx=2)
        ttk.Button(toolbar, text="⭐ Star").pack(side="left", padx=2)
        ttk.Button(toolbar, text="📁 Move to").pack(side="left", padx=2)

        # Email list with pagination
        list_frame = ttk.Frame(self.parent)
        list_frame.pack(fill="both", expand=True)
        
        columns = ("From", "Subject", "Date")
        tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(fill="both", expand=True)
        
        # Pagination
        page_frame = ttk.Frame(self.parent)
        page_frame.pack(fill="x", pady=5)
        
        ttk.Button(page_frame, text="◀").pack(side="left", padx=5)
        ttk.Label(page_frame, text="Page 1 of 5").pack(side="left", padx=5)
        ttk.Button(page_frame, text="▶").pack(side="left", padx=5)
