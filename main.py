import sqlite3
import PySimpleGUI as sg

# Connect to the SQLite database
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# Create a table to store user data
cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT,
                    email TEXT,
                    tgl_lahir TEXT,
                    telepon TEXT
                )''')
conn.commit()

layout = [
    [sg.Text("Nama:")],
    [sg.Input(key="nama")],
    [sg.Text("Email:")],
    [sg.Input(key="email")],
    [sg.Text("Tanggal Lahir:")],
    [sg.Input(key="tgl_lahir")],
    [sg.Text("Nomor Telepon:")],
    [sg.Input(key="telepon")],
    [sg.Button("Submit")],
    [sg.Table(values=[], headings=['ID', 'Nama', 'Email', 'Tanggal Lahir', 'Nomor Telepon'],
              auto_size_columns=True, key='table')]
]

window = sg.Window("Data ankos", layout)

while True:
    event, values = window.read()
    if event == "Submit" or event == sg.WINDOW_CLOSED or event == "Enter":
        # Insert user data into the database
        cursor.execute("INSERT INTO user (nama, email, tgl_lahir, telepon) VALUES (?, ?, ?, ?)",
                       (values['nama'], values['email'], values['tgl_lahir'], values['telepon']))
        conn.commit()

        table_values = []
        cursor.execute('SELECT id, nama, email, tgl_lahir, telepon FROM user')
        rows = cursor.fetchall()
        for row in rows:
            table_values.append(list(row))

        window['table'].update(values=table_values)

    if event == sg.WINDOW_CLOSED:
        break

window.close()

# Close the database connection
conn.close()

# Rest of your code...