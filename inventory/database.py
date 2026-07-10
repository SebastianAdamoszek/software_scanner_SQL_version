import sqlite3
from pathlib import Path


DATABASE_PATH = Path("software_scanner.db")


def create_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    return connection


def create_tables():
    connection = create_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    version TEXT,
    publisher TEXT,
    install_date TEXT,
    install_location TEXT,
    uninstall_string TEXT
    )  
        """
    )

    connection.commit()
    connection.close()


def add_program(
    name,
    version,
    publisher,
    install_date,
    install_location,
    uninstall_string,
):

    connection = create_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO programs 
        (name, version, publisher, install_date, install_location, uninstall_string)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            version,
            publisher,
            install_date,
            install_location,
            uninstall_string,
        ),
    )

    connection.commit()
    connection.close() 


def save_programs(programs):
    for program in programs:
        add_program(
            program["name"],
            program["version"],
            program["publisher"],
            program["install_date"],
            program["install_location"],
            program["uninstall_string"],
        )


def get_programs():
    connection = create_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM programs
        """
    )

    programs = cursor.fetchall()

    connection.close()

    return programs

if __name__ == "__main__":
    create_tables()

    add_program(
        "Python",
        "3.12",
        "Python Software Foundation",
        "C:\\Python312",
    )

    print("Program added successfully")

    programs = [
        {
            "name": "Firefox",
            "version": "140",
            "publisher": "Mozilla",
            "install_location": "C:\\Program Files\\Firefox"
        },
        {
            "name": "VS Code",
            "version": "1.102",
            "publisher": "Microsoft",
            "install_location": "C:\\Program Files\\Microsoft VS Code"
        }
    ]

    save_programs(programs)

    print("Programs added to database")

    saved_programs = get_programs()

    for program in saved_programs:
        print(program)    
   