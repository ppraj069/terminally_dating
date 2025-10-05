import curses
from getpass import getpass
import sqlite3
from rich.console import Console
from rich.table import Table

console = Console()
DB_NAME = "messages.db"

# ---------------- Database setup ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS Messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender_id INTEGER NOT NULL,
                    receiver_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (sender_id) REFERENCES Users(id),
                    FOREIGN KEY (receiver_id) REFERENCES Users(id)
                )''')
    conn.commit()
    conn.close()

# ---------------- Functions ----------------
def registration():
    console.print("[bold cyan]=== REGISTER ===[/bold cyan]")
    username = input("Username: ")
    password = getpass("Password: ")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        console.print("[green]Registration complete![/green]")
    except sqlite3.IntegrityError:
        console.print("[red]Username already exists.[/red]")
    finally:
        conn.close()

def login():
    console.print("[bold cyan]=== LOGIN ===[/bold cyan]")
    username = input("Username: ")
    password = getpass("Password: ")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id FROM Users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        console.print(f"[green]Welcome, {username}![/green]")
        return user[0], username
    else:
        console.print("[red]Invalid credentials.[/red]")
        return None, None

# ---------------- Arrow Menu ----------------
def arrow_menu(stdscr, title, options):
    curses.curs_set(0)  # hide cursor
    current = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, title, curses.A_BOLD)
        for idx, option in enumerate(options):
            if idx == current:
                stdscr.addstr(idx+2, 0, f"> {option}", curses.A_REVERSE)
            else:
                stdscr.addstr(idx+2, 0, f"  {option}")
        key = stdscr.getch()
        if key == curses.KEY_UP and current > 0:
            current -= 1
        elif key == curses.KEY_DOWN and current < len(options) - 1:
            current += 1
        elif key in [10, 13]:  # Enter key
            return current

# ---------------- Main Loop ----------------
def main_curses(stdscr):
    init_db()
    while True:
        choice = arrow_menu(stdscr, "=== Terminal Messenger ===", ["Register", "Login", "Exit"])
        if choice == 0:
            registration()
        elif choice == 1:
            user_id, username = login()
            if user_id:
                console.print(f"[yellow]Logged in as {username}[/yellow]")
        elif choice == 2:
            console.print("[red]Goodbye![/red]")
            break

# ---------------- Run ----------------
if __name__ == "__main__":
    curses.wrapper(main_curses)
