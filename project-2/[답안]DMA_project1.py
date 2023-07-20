import mysql.connector


# TODO: REPLACE THE VALUE OF VARIABLE team (EX. TEAM 1 --> team = 1)
team = 8


# Requirement1: create schema ( name: DMA_team## )
def requirement1(host, user, password):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute('SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;')

    # TODO: WRITE CODE HERE
    print('Creating schema...')
    cursor.execute('DROP DATABASE IF EXISTS DMA_team%02d;' % team)
    cursor.execute('CREATE DATABASE IF NOT EXISTS DMA_team%02d;' % team)

    # TODO: WRITE CODE HERE
    cursor.close()


# Requierement2: create table
def requirement2(host, user, password):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute('SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;')

    # TODO: WRITE CODE HERE
    print('Creating tables...')
    cursor.execute('USE DMA_team%02d;' % team)

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user(
    id BIGINT(20) NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    profile_image TINYINT(1) default 0,
    items_count INT(11) default 0,
    UNIQUE (user_name),
    PRIMARY KEY (id) );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS item(
    id INT(11) NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    price VARCHAR(255),
    beta_version TINYINT(1) default 0,
    ratings INT(11) default 0,
    metascore INT(11) default 0,
    developer VARCHAR(255),
    release_date DATE,
    PRIMARY KEY (id) );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_item(
    user_id BIGINT(20) NOT NULL,
    item_id INT(11) NOT NULL,
    usagetime_2weeks INT(11) NOT NULL,
    usagetime_total INT(11) NOT NULL,
    PRIMARY KEY (user_id, item_id) );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS review(
    id VARCHAR(255) NOT NULL,
    user_id BIGINT(20) NOT NULL,
    item_id INT(11) NOT NULL,
    recommend INT(11) NOT NULL,
    body INT(11) NOT NULL,
    helpful_score VARCHAR(255) NOT NULL,
    helpful_count INT(11) default 0,
    posted_date DATE NOT NULL,
    PRIMARY KEY (id) );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS genre(
    id VARCHAR(255) NOT NULL,
    genre_name VARCHAR(255) NOT NULL,
    UNIQUE (genre_name),
    PRIMARY KEY (id) );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS item_genre(
    item_id INT(11) NOT NULL,
    genre_id VARCHAR(255) NOT NULL,
    PRIMARY KEY (item_id, genre_id) );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bundle(
    id INT(11) NOT NULL,
    bundle_name VARCHAR(255) NOT NULL,
    price VARCHAR(255) NOT NULL,
    final_price VARCHAR(255) NOT NULL,
    discount VARCHAR(255) NOT NULL,
    PRIMARY KEY (id) );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bundle_item(
    bundle_id INT(11) NOT NULL,
    item_id INT(11) NOT NULL,
    PRIMARY KEY (bundle_id, item_id) );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bundle_genre(
    bundle_id INT(11) NOT NULL,
    genre_id VARCHAR(255) NOT NULL,
    genre_count INT(11) NOT NULL,
    PRIMARY KEY (bundle_id, genre_id) );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tag(
    item_id INT(11) NOT NULL,
    tag_name VARCHAR(255) NOT NULL,
    tag_order INT(11) NOT NULL,
    PRIMARY KEY (item_id, tag_name) );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS item_specs(
    item_id INT(11) NOT NULL,
    spec_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (item_id, spec_name) );
    ''')

    # TODO: WRITE CODE HERE
    cursor.close()


# Requirement3: insert data
def requirement3(host, user, password, directory):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute('SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;')

    # TODO: WRITE CODE HERE
    print('Inserting data...')
    cursor.execute('USE DMA_team%02d;' % team)
    table_name = ['user', 'item', 'user_item', 'review', 'genre', 'item_genre', 
                    'bundle', 'bundle_item', 'bundle_genre', 'tag', 'item_specs']

    for table in table_name:
        print(table)
        filepath = directory + '/' + table + '.csv'
        with open(filepath, 'r', encoding='utf-8') as csv_data:
            next(csv_data, None)  # skip the headers

            if table in ['user', 'user_item']:
                for row in csv_data:
                    # Change the null data
                    row = row.strip().split(sep=',')
                    if '' in row:
                        temp = []
                        for item in row:
                            if item == '':
                                item = None
                            temp.append(item)
                        row = temp
                    cursor.execute('INSERT INTO ' + table + ' VALUES (%s,%s,%s,%s)', row)
                    cnx.commit()

            elif table in ['genre', 'item_genre', 'bundle_item', 'item_specs']:
                for row in csv_data:
                    # Change the null data
                    row = row.strip().split(sep=',')
                    if '' in row:
                        temp = []
                        for item in row:
                            if item == '':
                                item = None
                            temp.append(item)
                        row = temp
                    cursor.execute('INSERT INTO ' + table + ' VALUES (%s,%s)', row)
                    cnx.commit()

            elif table in ['bundle_genre', 'tag']:
                for row in csv_data:
                    # Change the null data
                    row = row.strip().split(sep=',')
                    if '' in row:
                        temp = []
                        for item in row:
                            if item == '':
                                item = None
                            temp.append(item)
                        row = temp
                    cursor.execute('INSERT INTO ' + table + ' VALUES (%s,%s,%s)', row)
                    cnx.commit()

            elif table in ['bundle']:
                for row in csv_data:
                    # Change the null data
                    row = row.strip().split(sep=',')
                    if '' in row:
                        temp = []
                        for item in row:
                            if item == '':
                                item = None
                            temp.append(item)
                        row = temp
                    cursor.execute('INSERT INTO ' + table + ' VALUES (%s,%s,%s,%s,%s)', row)
                    cnx.commit()

            elif table in ['item', 'review']:
                for row in csv_data:
                    # Change the null data
                    row = row.strip().split(sep=',')
                    if '' in row or 'nan' in row:
                        temp = []
                        for item in row:
                            if item == '' or item == 'nan':
                                item = None
                            temp.append(item)
                        row = temp
                    cursor.execute('INSERT INTO ' + table + ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', row)
                    cnx.commit()

    # TODO: WRITE CODE HERE
    cursor.close()


# Requirement4: add constraint (foreign key)
def requirement4(host, user, password):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute('SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;')

    # TODO: WRITE CODE HERE
    print('Adding constraints...')
    cursor.execute('USE DMA_team%02d;' % team)

    cursor.execute('ALTER TABLE user_item ADD CONSTRAINT FOREIGN KEY (user_id) REFERENCES user(id);')
    print("constraint 1 added")

    cursor.execute('ALTER TABLE user_item ADD CONSTRAINT FOREIGN KEY (item_id) REFERENCES item(id);')
    print("constraint 2 added")

    cursor.execute('ALTER TABLE review ADD CONSTRAINT FOREIGN KEY (user_id) REFERENCES user(id);')
    print("constraint 3 added")

    cursor.execute('ALTER TABLE review ADD CONSTRAINT FOREIGN KEY (item_id) REFERENCES item(id);')
    print("constraint 4 added")

    cursor.execute('ALTER TABLE item_genre ADD CONSTRAINT FOREIGN KEY (item_id) REFERENCES item(id);')
    print("constraint 5 added")

    cursor.execute('ALTER TABLE item_genre ADD CONSTRAINT FOREIGN KEY (genre_id) REFERENCES genre(id);')
    print("constraint 6 added")

    cursor.execute('ALTER TABLE bundle_item ADD CONSTRAINT FOREIGN KEY (bundle_id) REFERENCES bundle(id);')
    print("constraint 7 added")

    cursor.execute('ALTER TABLE bundle_item ADD CONSTRAINT FOREIGN KEY (item_id) REFERENCES item(id);')
    print("constraint 8 added")

    cursor.execute('ALTER TABLE bundle_genre ADD CONSTRAINT FOREIGN KEY (bundle_id) REFERENCES bundle(id);')
    print("constraint 9 added")

    cursor.execute('ALTER TABLE bundle_genre ADD CONSTRAINT FOREIGN KEY (genre_id) REFERENCES genre(id);')
    print("constraint 10 added")

    cursor.execute('ALTER TABLE tag ADD CONSTRAINT FOREIGN KEY (item_id) REFERENCES item(id);')
    print("constraint 11 added")

    cursor.execute('ALTER TABLE item_specs ADD CONSTRAINT FOREIGN KEY (item_id) REFERENCES item(id);')
    print("constraint 12 added")

    # TODO: WRITE CODE HERE
    cursor.close()


# TODO: REPLACE THE VALUES OF FOLLOWING VARIABLES
host = 'localhost'
user = 'root'
password = 'gkfk8705'
directory = './dataset(revised)'

requirement1(host=host, user=user, password=password)
requirement2(host=host, user=user, password=password)
requirement3(host=host, user=user, password=password, directory=directory)
requirement4(host=host, user=user, password=password)
print('Done!')