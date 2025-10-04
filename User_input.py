from rich.console import Console
from getpass import getpass

console = Console()

class UserProfile:
    def __init__(self, first_name, last_name, age, gender, interests, bio, number, email, password, profile_pic):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.interests = interests
        self.bio = bio
        self.number = number
        self.email = email
        self.password = "*" * len(password)  # masked
        self.profile_pic = profile_pic

    def display(self):
        console.print("\n[bold yellow]=== Your Dating Profile ===[/bold yellow]")
        console.print(f"[cyan]Name[/cyan]: [magenta]{self.first_name} {self.last_name}[/magenta]")
        console.print(f"[cyan]Age[/cyan]: [magenta]{self.age}[/magenta]")
        console.print(f"[cyan]Gender[/cyan]: [magenta]{self.gender}[/magenta]")
        console.print(f"[cyan]Interests[/cyan]: [magenta]{', '.join(self.interests)}[/magenta]")
        console.print(f"[cyan]Bio[/cyan]: [magenta]{self.bio}[/magenta]")
        console.print(f"[cyan]Phone Number[/cyan]: [magenta]{self.number}[/magenta]")
        console.print(f"[cyan]Email[/cyan]: [magenta]{self.email}[/magenta]")
        console.print(f"[cyan]Password[/cyan]: [magenta]{self.password}[/magenta]")
        console.print(f"[cyan]Profile Picture[/cyan]: [magenta]{self.profile_pic}[/magenta]")

def is_valid_email(email):
    if "@" not in email or email.count("@") != 1:
        return False
    local, domain = email.split("@")
    if "." not in domain:
        return False
    if " " in email:
        return False
    return True

def create_profile():
    console.print("[bold cyan]=== Dating Profile Setup ===[/bold cyan]")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")

    # Age validation
    age = int(input("Age: "))
    while age < 18:
        console.print("[red]You must be at least 18 to use this service.[/red]")
        age = int(input("Age: "))

    gender = input("Gender: ")
    interests = input("Enter your interests (comma separated): ").split(",")
    bio = input("Write a short bio: ")

    # Phone number validation
    number = input("Enter your Phone Number (10 digits): ")
    while len(number) != 10 or not number.isdigit():
        console.print("[red]Your number should be exactly 10 digits.[/red]")
        number = input("Enter your Phone Number (10 digits): ")

    # Email validation
    email = input("Enter your Email: ")
    while not is_valid_email(email):
        console.print("[red]Invalid email format. Please enter a valid email.[/red]")
        email = input("Enter your Email: ")

    password = getpass("Enter your Password: ")
    profile_pic = input("Upload a jpeg picture: ")

    # Create UserProfile object
    user = UserProfile(first_name, last_name, age, gender, [i.strip() for i in interests],
                       bio, number, email, password, profile_pic)
    return user

def main():
    user = create_profile()
    user.display()


main()
