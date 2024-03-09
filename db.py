import psycopg2


db = psycopg2.connect('postgres://adilka:XG7hOpA6q5lOinRtltyv271PZ8PB6vph@dpg-cka3cqfs0fgc739f48kg-a.singapore-postgres.render.com/main_wp2z')
cur = db.cursor()

cur.execute("""SELECT * FROM LIST""")
db.commit()
print(cur.fetchall())