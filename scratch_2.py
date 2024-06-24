import sqlite3


def create_tables():
    conn = sqlite3.connect('daily_activity.db')
    cursor = conn.cursor()

    # Create states table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS states (
            id INTEGER PRIMARY KEY,
            state TEXT NOT NULL,
            is_initial INTEGER NOT NULL DEFAULT 0,
            feedback TEXT
        )
    ''')

    # Create locations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY,
            state TEXT NOT NULL,
            location TEXT NOT NULL
        )
    ''')

    # Create activities table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY,
            activity TEXT NOT NULL
        )
    ''')

    # Create daily status table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_status (
            id INTEGER PRIMARY KEY,
            day_end INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY,
            activity TEXT NOT NULL,
            feedback TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def insert_initial_data():
    conn = sqlite3.connect('daily_activity.db')
    cursor = conn.cursor()

    # Insert initial state
    cursor.execute("INSERT INTO states (state, is_initial) VALUES ('state_1', 1)")

    # Insert initial location
    cursor.execute("INSERT INTO locations (state, location) VALUES ('state_1', 'location_1')")

    # Insert activities
    activities = [
        ('work',),
        ('exercise',),
        ('relax',),
        ('study',)
    ]
    cursor.executemany("INSERT INTO activities (activity) VALUES (?)", activities)

    # Insert daily status
    cursor.execute("INSERT INTO daily_status (day_end) VALUES (0)")

    # Insert feedback
    feedback = [
        ('work', 'positive'),
        ('exercise', 'positive'),
        ('relax', 'negative'),
        ('study', 'negative')
    ]
    cursor.executemany("INSERT INTO feedback (activity, feedback) VALUES (?, ?)", feedback)

    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_tables()
    insert_initial_data()
