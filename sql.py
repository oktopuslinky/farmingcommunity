import sqlite3
with sqlite3.connect("farmers.db") as connection:
    c = connection.cursor()

    c.execute('DROP TABLE farmers_list')
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
            chemicals TEXT,
            picture TEXT
        )
        '''
    );

    """
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS photos(
            photo BLOB
        )
        '''
    )
    """
    #c.execute('INSERT INTO logins VALUES("1", "johnsmith@hotmail.com", "admin")');
    c.execute('DROP TABLE logins')
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS logins(
            farmer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            password TEXT
        )
        '''
    );

    c.execute('DROP TABLE needs')
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS needs(
            need_id INTEGER PRIMARY KEY AUTOINCREMENT,
            need_text TEXT,
            farmer_id TEXT
        )
        '''
    );

    """
    c.execute(
        '''
        INSERT INTO needs(need_text, farmer_id) VALUES(
            "need some tomato seeds",
            "1"
        )
        '''
    )
    """
    """
    c.execute(
        '''
        INSERT INTO farmers_list(first_name, last_name, age, email, phone_number, plants, seeds, tools, chemicals) VALUES(
            "John", "Smith", 42, "johnsmith@hotmail.com", 1234567, "tomato", "eggplant(15)", "shovel", "pesticide"
        )
        '''
    );
    """