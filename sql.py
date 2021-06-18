import sqlite3
with sqlite3.connect("farmers.db") as connection:
    c = connection.cursor()

    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS farmers_list(
            farmer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            age INT,
            email TEXT,
            phone_number VARCHAR(15),
            plants TEXT,
            seeds TEXT,
            tools TEXT,
            chemicals TEXT
        )
        '''
    );

    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS logins(
            farmer_id TEXT,
            username TEXT,
            password TEXT
        )
        '''
    );

    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS needs(
            need_id INTEGER PRIMARY KEY AUTOINCREMENT,
            need_text TEXT,
            farmer_id TEXT
        )
        '''
    );

    c.execute(
        '''
        INSERT INTO needs(need_text, farmer_id) VALUES(
            "need some tomato seeds",
            "1"
        )
        '''
    )

    """
    c.execute(
        '''
        INSERT INTO farmers_list(first_name, last_name, age, email, phone_number, plants, seeds, tools, chemicals) VALUES(
            "John", "Smith", 42, "johnsmith@hotmail.com", 1234567, "tomato", "eggplant(15)", "shovel", "pesticide"
        )
        '''
    );
    """