const express = require('express');
const cors = require('cors');
const sqlite = require('sqlite3');

const app = express();

const db = new sqlite.Database('dealerships.db', err => {
    if (err) {
        console.error("Couldn't connect to database")
    } else {
        console.log("Dealerships online!")
    }
})

app.use(cors());

app.get('/dealerships', (req, res) => {
    let query = 'SELECT * FROM dealerships';
    
    if (req.query.state) {
      query += ` WHERE st=${req.query.state}`;
    }
    
    if (req.query.dealerId) {
      query += ` WHERE id=${req.query.dealerId}`;
    }
    
    console.log(`GET request, making db query:\n ${query}`)

    db.all(query, [], (err, rows) => {
      if (err) {
        throw err;
      }
      res.json(rows);
    });
});

const port = 3300;

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
})
