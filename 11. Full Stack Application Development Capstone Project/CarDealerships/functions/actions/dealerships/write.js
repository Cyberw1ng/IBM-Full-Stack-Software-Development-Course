const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');

const db = new sqlite3.Database('dealerships.db');

// Read data from JSON file
const jsonData = fs.readFileSync('dealerships.json', 'utf8');
const dealerships = JSON.parse(jsonData);

// Serialize database operations to ensure they are executed in sequence
db.serialize(() => {
    // Create dealerships table if it doesn't exist
    db.run(`CREATE TABLE IF NOT EXISTS dealerships (
        id INTEGER PRIMARY KEY,
        city TEXT,
        state TEXT,
        st TEXT,
        address TEXT,
        zip TEXT,
        lat REAL,
        long REAL,
        short_name TEXT,
        full_name TEXT
    )`);

    // Prepare and insert data into the dealerships table
    const stmt = db.prepare(
        'INSERT INTO dealerships (id, city, state, st, address, zip, lat, long, short_name, full_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    );

    dealerships.dealerships.forEach(dealership => {
        stmt.run(
            dealership.id,
            dealership.city,
            dealership.state,
            dealership.st,
            dealership.address,
            dealership.zip,
            dealership.lat,
            dealership.long,
            dealership.short_name,
            dealership.full_name
        );
    });

    stmt.finalize(); // Finalize the prepared statement
});

// Close the database connection
db.close(err => {
    if (err) {
        return console.error('Error closing database connection:', err.message);
    }
    console.log('Data imported successfully. Database connection closed.');
});
