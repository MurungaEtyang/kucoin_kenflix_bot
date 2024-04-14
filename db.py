import mysql.connector

class DatabaseManager:
    __data = 'please contact Evans 0717325657 for update'
    __table_name = "kenflix_message"
    def __init__(self, host="db4free.net", user="google_pro", password="Evans1324$M", database="google_pro"):
        
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute(f'''CREATE TABLE IF NOT EXISTS {self.__table_name} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))''')
        self.conn.commit()

    def insert_data(self, table_name = "kenflix_message"):
        self.cur.execute(f'''SELECT * FROM {table_name} WHERE name = %s''', (self.__data,))
        existing_data = self.cur.fetchone()
        if existing_data:
            # If data already exists, update it
            self.cur.execute(f'''UPDATE {table_name} SET name = %s WHERE name = %s''', (self.__data, self.__data))
        else:
            # If data doesn't exist, insert it
            self.cur.execute(f'''INSERT INTO {table_name} (name) VALUES (%s)''', (self.__data,))
        self.conn.commit()

    def fetch_data_kenflix(self, table_name = "kenflix_security"):
        self.cur.execute(f'''SELECT * FROM {table_name}''')
        rows = self.cur.fetchall()
        return [row[1] for row in rows]
    
    def fetch_data_message(self, table_name= "kenflix_message"):
        self.cur.execute(f'''SELECT * FROM {table_name}''')
        rows = self.cur.fetchall()
        return [row[1] for row in rows]

    def close_connection(self):
        self.conn.close()

# Example usage
if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.create_table()
    db_manager.insert_data()
    # Fetch data
    data = db_manager.fetch_data_kenflix()
    print("Data fetched from the database:")
    for word in data:
        print(word)

    data1 = db_manager.fetch_data_message()
    print("Data fetched from the database:")
    
    print(data1)

    # Close connection
    db_manager.close_connection()
