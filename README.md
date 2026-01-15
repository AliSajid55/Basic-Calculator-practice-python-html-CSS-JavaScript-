# Calculator

Professional, small calculator project containing two independent implementations:

- A browser-based web version (`calculator.html`, `style.css`, `script.js`).
- A native desktop version implemented in Python/Tkinter (`calculator_tk.py`).

**What this repository contains**

- [calculator.html](calculator.html): The web UI entry point. Opens in a browser and uses the files below.
- [style.css](style.css): Styling for the web UI — the white & blue theme, layout and responsive rules.
- [script.js](script.js): Web calculator logic (input handling and evaluation) wired to the buttons in `calculator.html`.
- [calculator_tk.py](calculator_tk.py): A standalone Python/Tkinter desktop calculator with keyboard support, memory buttons (MC/MR/M+/M-), history, and a UI styled to match the web theme.

**Relationship between the web version and the Python version**

- The web files (`calculator.html`, `style.css`, `script.js`) form a single browser-based application and run entirely in the browser. They do not require Python.
- The Python file (`calculator_tk.py`) is a separate, standalone application that reimplements the same functionality for desktop. It does not import or depend on the web files. Both implementations are provided so you can run whichever environment you prefer.

**How to run**

- Run the web version (quick):

  - Double-click `calculator.html` or right-click → Open With → choose your browser.

  - Or serve locally (recommended when editing `script.js`/`style.css`):

    ```powershell
    cd "C:\Users\alisa\OneDrive\Desktop\Ali Sajid"
    python -m http.server 8000
    # then open http://localhost:8000/calculator.html
    ```

- Run the web version with Live Server (VS Code):

  - Install the `Live Server` extension in VS Code.
  - Open `calculator.html` and click `Go Live` in the status bar (or use Command Palette → `Live Server: Open with Live Server`).

- Run the desktop (Tkinter) version:

  ```powershell
  python calculator_tk.py
  ```

  - `calculator_tk.py` uses only the Python standard library (`tkinter`); most Python installers include Tkinter on Windows. If you see an error about missing Tk, install a Python build that includes Tcl/Tk.

**Files — detailed explanation**

- `calculator.html` — Structure and responsibility:
  - Provides the calculator DOM: a display area and a grid of buttons.
  - Uses `data-value` and `data-action` attributes so JavaScript can remain generic and declarative.

- `style.css` — Styling and theme:
  - Implements the white & blue color palette, spacing, and typography.
  - Adds hover and active states for buttons and responsive layout rules.

- `script.js` — Browser logic:
  - Attaches event listeners to the buttons and keyboard.
  - Manages the current input string and executes calculations.
  - Exposes actions: clear, backspace, percent, equals.

- `calculator_tk.py` — Desktop logic and UI:
  - Reimplements the same feature set using Tkinter widgets.
  - Includes keyboard bindings, memory operations, history window, hover effects and a modern tiled layout.
  - Keeps a restricted evaluation step to reduce risk when evaluating text expressions.

**Why two implementations?**

- The web version is ideal for quick sharing, styling iterations, and browser deployment.
- The desktop version is for local use without a browser and demonstrates a native-like UI while keeping the same user experience.

**Development notes & recommendations**

- Keep the visual theme consistent by editing `style.css` for the web UI and updating the color constants at the top of `calculator_tk.py` (`BLUE`, `BLUE_DARK`, `BG`, `TEXT`).
- If you want a single source of truth for evaluation logic, we can extract the evaluator into a small `calc_core.py` module and import it from both the web build process (via a transpilation step) and `calculator_tk.py` — I can scaffold that for you.

**Troubleshooting**

- `ImportError: No module named 'tkinter'`: install a Python distribution that includes Tcl/Tk (the official Windows installer does), or install the appropriate OS package.
- Live Server not showing `Go Live` in VS Code: Reload the window, ensure the extension is enabled, and open `calculator.html` in the active editor.

**Next steps I can help with**

- Add a small launcher script (`launch.py`) that asks whether to open the web or desktop calculator.
- Extract shared evaluation logic into a reusable module.
- Produce a packaged executable for Windows (`pyinstaller`) so you can distribute the desktop app.

If you want any of those, tell me which and I will implement it.
# Calculator

Simple browser calculator with a white and blue color theme.

Usage

Files

Python/Tkinter version
- [calculator_tk.py](calculator_tk.py) — a desktop calculator with keyboard input, memory (MC/MR/M+/M-), and history. Run with:

```powershell
python calculator_tk.py
```

