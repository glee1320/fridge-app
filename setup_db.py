import sqlite3

# Connect to the database (creates fridge.db if it doesn't exist)
conn = sqlite3.connect("fridge.db")
cur = conn.cursor()

# Start fresh each time this script runs
cur.execute("DROP TABLE IF EXISTS items")

# Create the items table
cur.execute("""
    CREATE TABLE items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity TEXT,
        location TEXT,
        date_added TEXT,
        expiry_date TEXT
    )
""")

# Add some starter items (dates are YYYY-MM-DD)
items = [
    ("Milk", "1 gallon", "fridge", "2026-10-27", "2026-11-08"),
    ("Eggs", "6", "fridge", "2026-10-25", "2026-11-30"),
    ("Spinach", "1 bag", "fridge", "2026-10-28", "2026-11-01"),
    ("Chicken breast", "2 lbs", "fridge", "2026-10-29", "2026-11-05"),
    ("Mozzarella cheese", "1 log", "fridge", "2026-10-20", "2026-11-10"),
]

cur.executemany("""
    INSERT INTO items (name, quantity, location, date_added, expiry_date)
    VALUES (?, ?, ?, ?, ?)
""", items)

# Save and close
conn.commit()
conn.close()

print(f"Database created with {len(items)} items!")