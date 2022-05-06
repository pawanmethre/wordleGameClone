import sqlite3

conn = sqlite3.connect('data.db')
print("Opened database successfully")

conn.execute('''CREATE TABLE WORDS
         (DATE TEXT PRIMARY KEY NOT NULL,
         WORD TEXT NOT NULL);''')

conn.execute('''CREATE TABLE PROFILE
         (EMAIL TEXT PRIMARY KEY NOT NULL,
         NAME TEXT NOT NULL,
         SCORE INT NOT NULL DEFAULT 0);''')

conn.execute('''CREATE TABLE GAME_STATS
         (EMAIL TEXT  NOT NULL,
         DATE TEXT NOT NULL,
         TRIALS INT NOT NULL,
         COMPLETED INT NOT NULL, PRIMARY KEY(EMAIL, DATE));''')



print("Table created successfully")

conn.execute("INSERT INTO WORDS (DATE, WORD) \
      VALUES ('05/01/22', 'train')")

conn.execute("INSERT INTO WORDS (DATE, WORD) \
      VALUES ('05/02/22', 'mango')")

conn.execute("INSERT INTO WORDS (DATE, WORD) \
      VALUES ('05/03/22', 'badge')")

conn.execute("INSERT INTO WORDS (DATE, WORD) \
      VALUES ('05/04/22', 'state')")

conn.execute("INSERT INTO WORDS (DATE, WORD) \
      VALUES ('05/05/22', 'range')")

conn.execute("INSERT INTO WORDS (DATE, WORD) \
      VALUES ('05/06/22', 'class')")

conn.execute("INSERT INTO WORDS (DATE, WORD) \
      VALUES ('05/07/22', 'cameo')")

conn.execute("INSERT INTO WORDS (DATE, WORD) \
      VALUES ('05/08/22', 'buble')")

conn.execute("INSERT INTO WORDS (DATE, WORD) \
      VALUES ('05/09/22', 'award')")

conn.execute("INSERT INTO WORDS (DATE, WORD) \
      VALUES ('05/10/22', 'cabin')")

conn.execute("INSERT INTO WORDS (DATE, WORD) \
      VALUES ('05/11/22', 'earth')")

conn.execute("INSERT INTO WORDS (DATE, WORD) \
      VALUES ('05/12/22', 'ideal')")

conn.execute("INSERT INTO WORDS (DATE, WORD) \
      VALUES ('05/13/22', 'ghost')")


conn.commit()
conn.close()