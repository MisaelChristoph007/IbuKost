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

def insert_data(values):
    # Insert user data into the database
    cursor.execute("INSERT INTO user (nama, email, tgl_lahir, telepon) VALUES (?, ?, ?, ?)",
                   (values['nama'], values['email'], values['tgl_lahir'], values['telepon']))
    conn.commit()

def update_data(values):
    # Update user data in the database
    cursor.execute("UPDATE user SET nama = ?, email = ?, tgl_lahir = ?, telepon = ? WHERE id = ?",
                   (values['nama'], values['email'], values['tgl_lahir'], values['telepon'], values['id']))
    conn.commit()

def delete_data(id):
    # Delete user data from the database
    cursor.execute("DELETE FROM user WHERE id = ?", (id,))
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
              auto_size_columns=True, key='table')],
    [sg.Input(key="edit_id", visible=False)],
    [sg.Button("Edit", key='edit_btn', visible=False)],
    [sg.Button("Hapus", key='hapus_btn', visible=False)]
]

window = sg.Window("Data ankos", layout)

while True:
    event, values = window.read()
    if event == "Submit" or event == sg.WINDOW_CLOSED or event == "Enter":
        if values["edit_id"]:
            update_data(values)
            window['edit_id'].update('')
            window['edit_btn'].update(visible=False)
            window['hapus_btn'].update(visible=False)
        else:
            insert_data(values)

        table_values = []
        cursor.execute('SELECT id, nama, email, tgl_lahir, telepon FROM user')
        rows = cursor.fetchall()
        for row in rows:
            table_values.append(list(row))

        window['table'].update(values=table_values)
        window['nama'].update('')
        window['email'].update('')
        window['tgl_lahir'].update('')
        window['telepon'].update('')

    elif event == "table":
        selected_row = values["table"][0]
        selected_data = table_values[selected_row]
        window['nama'].update(selected_data[1])
        window['email'].update(selected_data[2])
        window['tgl_lahir'].update(selected_data[3])
        window['telepon'].update(selected_data[4])
        window['edit_id'].update(selected_data[0])
        window['edit_btn'].update(visible=True)
        window['hapus_btn'].update(visible=True)

    elif event == "hapus_btn":
        selected_row = values["table"][0]
        selected_data = table_values[selected_row]
        delete_data(selected_data[0])
        window['edit_id'].update('')
        window['edit_btn'].update(visible=False)
        window['hapus_btn'].update(visible=False)

        table_values = []
        cursor.execute('SELECT id, nama, email, tgl_lahir, telepon FROM user')
        rows = cursor.fetchall()
        for row in rows:
            table_values.append(list(row))

        window['table'].update(values=table_values)
        window['nama'].update('')
        window['email'].update('')
        window['tgl_lahir'].update('')
        window['telepon'].update('')

    elif event == sg.WINDOW_CLOSED:
        break

window.close()

# Close the database connection
conn.close()

# Rest of your code...