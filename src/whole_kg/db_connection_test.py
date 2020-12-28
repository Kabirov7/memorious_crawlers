import dataset


def connect():
    db = dataset.connect('postgresql://goszakup@postgresgoszakup:Fdkvm%2503aJhdgc@postgresgoszakup.postgres.database.azure.com:5432/goszakup_dev')
    result = db.query('SELECT * FROM kg_procurement LIMIT 10')
    for row in result:
        print(row)


connect()
