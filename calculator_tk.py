import tkinter as tk
from tkinter import ttk, messagebox
import ast
import re

BLUE = '#0d6efd'
BLUE_DARK = '#0b5ed7'
BG = '#ffffff'
TEXT = '#0b2545'


def safe_eval(expr: str):
    """Evaluate a math expression after validating characters.

    Uses a strict regex to allow only digits, operators, parentheses, dots and spaces,
    then evaluates with restricted globals for simplicity and reliability.
    """
    expr = expr.replace('×', '*').replace('÷', '/').replace('−', '-')
    expr = expr.strip()

    if expr == '':
        raise ValueError('Empty expression')

    # allow digits, whitespace, parentheses, decimal point and these operators
    if not re.fullmatch(r'[0-9\s+\-*/().%]+', expr):
        raise ValueError('Expression contains invalid characters')

    try:
        # evaluate with no builtins and no globals for safety
        res = eval(expr, {"__builtins__": None}, {})
    except Exception as e:
        raise
    return res


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Calculator — White & Blue Theme')
        self.configure(bg=BG)

        # don't force a large fixed width — let the window size to content
        self.resizable(False, False)

        self.memory = 0.0
        self.history = []

        self._build_ui()
        self.bind_keys()

        # size window to required content width/height and center precisely
        self.update_idletasks()
        req_w = self.winfo_reqwidth()
        req_h = self.winfo_reqheight()
        # use exact required width to avoid extra right-side space, add tiny margin
        win_w = req_w + 6
        win_h = req_h + 6
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w - win_w) // 2
        y = (screen_h - win_h) // 2
        self.geometry(f'{win_w}x{win_h}+{x}+{y}')

    def _build_ui(self):
        # Use a plain tk.Frame to control spacing precisely for a modern look
        # card with subtle shadow (reduced outer padding to avoid extra empty space)
        shadow = tk.Frame(self, bg='#dfeeff')
        shadow.grid(padx=4, pady=4)
        frm = tk.Frame(shadow, bg=BG)
        frm.grid(padx=3, pady=3)

        # Display (Label gives a cleaner flat look)
        self.display_var = tk.StringVar(value='0')
        display = tk.Label(frm, textvariable=self.display_var, anchor='e', font=('Segoe UI', 26, 'bold'), bg='#f1f7ff', fg=TEXT)
        display.grid(row=0, column=0, columnspan=4, sticky='we', pady=(0, 8), ipady=12, ipadx=12)
        display.configure(relief='flat')

        # Buttons frame with tight grid (buttons touch each other)
        # btn_frame background is the separator color; we'll grid buttons with 1px gaps to show separators
        btn_frame = tk.Frame(frm, bg='#e6eefc')
        btn_frame.grid(row=1, column=0, sticky='nsew')

        # prefer plain arrow for backspace to avoid font substitution issues
        buttons = [
            ('MC', self.mem_clear), ('MR', self.mem_recall), ('M+', self.mem_add), ('M-', self.mem_sub),
            ('C', self.clear), ('←', self.backspace), ('%', self.percent), ('÷', lambda: self.append(' / ')),
            ('7', lambda: self.append('7')), ('8', lambda: self.append('8')), ('9', lambda: self.append('9')), ('×', lambda: self.append(' * ')),
            ('4', lambda: self.append('4')), ('5', lambda: self.append('5')), ('6', lambda: self.append('6')), ('−', lambda: self.append(' - ')),
            ('1', lambda: self.append('1')), ('2', lambda: self.append('2')), ('3', lambda: self.append('3')), ('+', lambda: self.append(' + ')),
            ('H', self.show_history), ('0', lambda: self.append('0')), ('.', lambda: self.append('.')), ('=', self.equals),
        ]

        # create buttons in a 5x4 grid without gaps so edges touch
        r = 0
        c = 0
        for (txt, cmd) in buttons:
            # adjust fonts: numbers larger, operators bold
            if txt.isdigit() or txt == '0':
                btn_font = ('Segoe UI', 16)
            elif txt in ('=',):
                btn_font = ('Segoe UI', 15, 'bold')
            elif txt in ('÷', '×', '−', '+'):
                btn_font = ('Segoe UI', 14, 'bold')
            else:
                btn_font = ('Segoe UI', 13)

            btn = tk.Button(btn_frame, text=txt, command=cmd, font=btn_font, bd=0, relief='flat', cursor='hand2')
            # Visual styles and hover colors
            if txt == '=':
                normal_bg = BLUE_DARK
                hover_bg = '#0a4db0'
                fg = 'white'
            elif txt in ('÷', '×', '−', '+'):
                normal_bg = BLUE
                hover_bg = BLUE_DARK
                fg = 'white'
            elif txt in ('C', '⌫', '%', 'MC', 'MR', 'M+', 'M-', 'H'):
                normal_bg = '#e9f2ff'
                hover_bg = '#d7e9ff'
                fg = BLUE_DARK
            else:
                normal_bg = 'white'
                hover_bg = '#f7f9fc'
                fg = TEXT

            btn.configure(bg=normal_bg, fg=fg, activebackground=hover_bg)
            btn.configure(width=6)

            # hover handlers to visually change background
            def on_enter(e, b=btn, hb=hover_bg):
                b.configure(bg=hb)

            def on_leave(e, b=btn, nb=normal_bg):
                b.configure(bg=nb)

            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)

            btn.grid(row=r, column=c, sticky='nsew', padx=1, pady=1)
            # give a bit of internal vertical size so height is comfortable
            btn.configure(height=2)

            c += 1
            if c > 3:
                c = 0
                r += 1

        # Remove external gaps by setting grid weights and zero padding
        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)
        for i in range(5):
            btn_frame.rowconfigure(i, weight=1)

    def append(self, s):
        cur = self.display_var.get()
        if cur == '0' and s.strip() not in ('.',):
            cur = ''
        self.display_var.set(cur + s)

    def clear(self):
        self.display_var.set('0')

    def backspace(self):
        cur = self.display_var.get()
        if len(cur) <= 1:
            self.display_var.set('0')
        else:
            self.display_var.set(cur[:-1])

    def percent(self):
        try:
            val = safe_eval(self.display_var.get())
            res = val / 100.0
            self.display_var.set(str(res))
            self._push_history(self.display_var.get())
        except Exception as e:
            messagebox.showerror('Error', f'Invalid expression: {e}')

    def equals(self):
        expr = self.display_var.get()
        try:
            res = safe_eval(expr)
            self.display_var.set(str(res))
            self._push_history(f'{expr} = {res}')
        except Exception as e:
            messagebox.showerror('Error', f'Invalid expression: {e}')

    # Memory functions
    def mem_clear(self):
        self.memory = 0.0

    def mem_recall(self):
        self.display_var.set(str(self.memory))

    def mem_add(self):
        try:
            self.memory += float(safe_eval(self.display_var.get()))
        except Exception:
            messagebox.showerror('Error', 'Invalid value for memory')

    def mem_sub(self):
        try:
            self.memory -= float(safe_eval(self.display_var.get()))
        except Exception:
            messagebox.showerror('Error', 'Invalid value for memory')

    # History
    def _push_history(self, item):
        self.history.insert(0, item)
        if len(self.history) > 50:
            self.history.pop()

    def show_history(self):
        win = tk.Toplevel(self)
        win.title('History')
        win.geometry('300x400')
        lb = tk.Listbox(win, font=('Segoe UI', 11))
        lb.pack(fill='both', expand=True, padx=8, pady=8)
        for item in self.history:
            lb.insert('end', item)

        def use_selected():
            sel = lb.curselection()
            if not sel:
                return
            val = lb.get(sel[0])
            if '=' in val:
                val = val.split('=')[-1].strip()
            self.display_var.set(val)
            win.destroy()

        btn = tk.Button(win, text='Use', command=use_selected, bg=BLUE, fg='white')
        btn.pack(pady=(0, 8))

    # Keyboard bindings
    def bind_keys(self):
        def on_key(e):
            k = e.keysym
            if k in ('Return', 'KP_Enter'):
                self.equals()
                return 'break'
            if k == 'Escape':
                self.clear()
                return 'break'
            if k == 'BackSpace':
                self.backspace()
                return 'break'
            if k.lower() == 'h':
                self.show_history()
                return 'break'
            char = e.char
            if char in '0123456789.+-*/()%':
                self.append(char)
                return 'break'

        self.bind_all('<Key>', on_key)


if __name__ == '__main__':
    app = Calculator()
    app.mainloop()