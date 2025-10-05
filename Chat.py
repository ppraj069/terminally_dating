import sqlite3
from rich.console import Console
from rich.table import Table
from getpass import getpass

console = Console()
DB_NAME = "messages.db"

# ---------- Initialize Database ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Create Users table
    c.execute('''CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')

    # Create Messages table
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

# ---------- User Registration ----------
def registration():
    console.print("[bold cyan]=== PLEASE REGISTER ===[/bold cyan]")
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

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

# ---------- User Login ----------
def login():
    console.print("[bold cyan]=== PLEASE LOGIN ===[/bold cyan]")
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

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

# ---------- Send Message ----------
def send_message(sender_id):
    receiver = input("Send to (username): ")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id FROM Users WHERE username=?", (receiver,))
    receiver_data = c.fetchone()

    if not receiver_data:
        console.print("[red]User not found.[/red]")
        conn.close()
        return

    content = input("Message: ")
    c.execute("INSERT INTO Messages (sender_id, receiver_id, content) VALUES (?, ?, ?)",
              (sender_id, receiver_data[0], content))
    conn.commit()
    conn.close()
    console.print("[green]Message sent![/green]")

# ---------- View Inbox ----------
def view_inbox(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT U.username, M.content, M.timestamp
        FROM Messages M
        JOIN Users U ON M.sender_id = U.id
        WHERE M.receiver_id = ?
        ORDER BY M.timestamp DESC
    """,(user_id,))
    messages = c.fetchall()
    conn.close()

    if not messages:
        console.print("[yellow]No messages yet.[/yellow]")
        return

    table = Table(title="Inbox", show_lines=True)
    table.add_column("No.", style="cyan")
    table.add_column("From", style="green")
    table.add_column("Message", style="white")
    table.add_column("Time", style="dim")

    for i, msg in enumerate(messages, 1):
        table.add_row(str(i), msg[0], msg[1], str(msg[2]))

    console.print(table)

# ---------- Chat Menu ----------
def chat_menu(user_id, username):
    while True:
        console.print(f"\n[bold magenta]=== Logged in as {username} ===[/bold magenta]")
        console.print("1. View Inbox\n2. Send Message\n3. Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            view_inbox(user_id)
        elif choice == "2":
            send_message(user_id)
        elif choice == "3":
            console.print("[yellow]Logged out.[/yellow]")
            break
        else:
            console.print("[red]Invalid option.[/red]")

# ---------- Main Menu ----------
def main():
    # Initialize database
    init_db()
    running = True  # loop control variable

    while running:
        console.print("\n[bold magenta]=== Terminal Messenger ===[/bold magenta]")
        console.print("1. Register")
        console.print("2. Login")
        console.print("3. Exit")
        
        choice = input("Choose an option: ")

        if choice == "1":
            registration()

        elif choice == "2":
            user_id, username = login()
            if user_id is not None:
                chat_menu(user_id, username)

        elif choice == "3":
            console.print("[bold red]Goodbye![/bold red]")
            running = False  # stops the loop

        else:
            console.print("[red]Invalid option.[/red]")
main()