import mysql.connector


# TODO: REPLACE THE VALUE OF VARIABLE team (EX. TEAM 1 --> team = 1)
team = 10


# Requirement1: create schema ( name: DMA_team## )
def requirement1(host, user, password):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute('SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;')

    # TODO: WRITE CODE HERE
    cursor.execute('CREATE SCHEMA IF NOT EXISTS DMA_team{} CHARACTER SET = utf8;'.format(team))
    # TODO: WRITE CODE HERE
    cursor.close()


# Requirement2: create table
def requirement2(host, user, password):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute('SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;')

    # TODO: WRITE CODE HERE
    cursor.execute('USE DMA_team{};'.format(team))
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user(
    id BIGINT(20) NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    profile_image TINYINT(1) DEFAULT 0,
    items_count INT(11) DEFAULT 0,
    PRIMARY KEY(id),
    UNIQUE (user_name));
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS item(
    id BIGINT(20) NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    price VARCHAR(255),
    beta_version TINYINT(1) DEFAULT 0,
    ratings INT(11) DEFAULT 0,
    metascore INT(11) DEFAULT 0,
    developer VARCHAR(255),
    release_date DATE,
    PRIMARY KEY(id));
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_item(
    user_id BIGINT(20) NOT NULL,
    item_id BIGINT(20) NOT NULL,
    usagetime_2weeks INT(11) NOT NULL,
    usagetime_total INT(11) NOT NULL,
    PRIMARY KEY(user_id, item_id));
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS review(
    id VARCHAR(255) NOT NULL,
    user_id BIGINT(20) NOT NULL,
    item_id BIGINT(20) NOT NULL,
    recommended INT(11) NOT NULL,
    body INT(11) NOT NULL,
    helpful_score VARCHAR(255) NOT NULL,
    helpful_count INT(11) DEFAULT 0,
    posted_date DATE NOT NULL,
    PRIMARY KEY(id));
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS genre(
    id VARCHAR(255) NOT NULL,
    genre_name VARCHAR(255) NOT NULL,
    PRIMARY KEY(id),
    UNIQUE (genre_name));
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS item_genre(
    item_id BIGINT(20) NOT NULL,
    genre_id VARCHAR(255) NOT NULL,
    PRIMARY KEY(item_id, genre_id));
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bundle(
    id INT(11) NOT NULL,
    bundle_name VARCHAR(255) NOT NULL,
    price VARCHAR(255) NOT NULL,
    final_price VARCHAR(255) NOT NULL,
    discount VARCHAR(255) NOT NULL,
    PRIMARY KEY(id));
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bundle_item(
    bundle_id INT(11) NOT NULL,
    item_id BIGINT(20) NOT NULL,
    PRIMARY KEY(bundle_id, item_id));
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bundle_genre(
    bundle_id INT(11) NOT NULL,
    genre_id VARCHAR(255) NOT NULL,
    genre_count INT(11) NOT NULL,
    PRIMARY KEY(bundle_id, genre_id));
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tag(
    item_id BIGINT(20) NOT NULL,
    tag_name VARCHAR(255) NOT NULL,
    tag_order INT(11) NOT NULL,
    PRIMARY KEY(item_id, tag_name));
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS item_specs(
    item_id BIGINT(20) NOT NULL,
    spec_name VARCHAR(255) NOT NULL,
    PRIMARY KEY(item_id, spec_name));
    ''')
    # TODO: WRITE CODE HERE
    cursor.close()


# Requirement3: insert data
def requirement3(host, user, password, directory):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute('SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;')

    # TODO: WRITE CODE HERE
    cursor.execute('USE DMA_team{};'.format(team))

    def insert2Table(tablename):
        filepath = directory + '/' + '{}.csv'.format(tablename)
        with open(filepath, 'r', encoding='utf-8') as f:
            for row in f.readlines()[1:]:
                row = row.strip().split(',')
                values = [str(value) if value.isnumeric() else '\"{}\"'.format(value) if value != "" and value != 'nan' else 'null' for value in row]
                values = ','.join(values)
                cursor.execute('INSERT INTO {} VALUES ({});'.format(tablename, values))

    tablenames = ['user', 'item', 'user_item', 'review', 'genre', 'item_genre', 'bundle', 'bundle_item', 'bundle_genre', 'tag', 'item_specs']
    for tablename in tablenames: insert2Table(tablename)
    cnx.commit()
    # TODO: WRITE CODE HERE
    cursor.close()


# Requirement4: add constraint (foreign key)
def requirement4(host, user, password):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute('SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;')

    # TODO: WRITE CODE HERE
    cursor.execute('USE DMA_team{};'.format(team))
    cursor.execute('ALTER TABLE user_item ADD CONSTRAINT FOREIGN KEY (user_id) REFERENCES user(id);')
    cursor.execute('ALTER TABLE user_item ADD CONSTRAINT FOREIGN KEY (item_id) REFERENCES item(id);')
    cursor.execute('ALTER TABLE review ADD CONSTRAINT FOREIGN KEY (user_id) REFERENCES user(id);')
    cursor.execute('ALTER TABLE review ADD CONSTRAINT FOREIGN KEY (item_id) REFERENCES item(id);')
    cursor.execute('ALTER TABLE item_genre ADD CONSTRAINT FOREIGN KEY (item_id) REFERENCES item(id);')
    cursor.execute('ALTER TABLE item_genre ADD CONSTRAINT FOREIGN KEY (genre_id) REFERENCES genre(id);')
    cursor.execute('ALTER TABLE bundle_item ADD CONSTRAINT FOREIGN KEY (bundle_id) REFERENCES bundle(id);')
    cursor.execute('ALTER TABLE bundle_item ADD CONSTRAINT FOREIGN KEY (item_id) REFERENCES item(id);')
    cursor.execute('ALTER TABLE bundle_genre ADD CONSTRAINT FOREIGN KEY (bundle_id) REFERENCES bundle(id);')
    cursor.execute('ALTER TABLE bundle_genre ADD CONSTRAINT FOREIGN KEY (genre_id) REFERENCES genre(id);')
    cursor.execute('ALTER TABLE tag ADD CONSTRAINT FOREIGN KEY (item_id) REFERENCES item(id);')
    cursor.execute('ALTER TABLE item_specs ADD CONSTRAINT FOREIGN KEY (item_id) REFERENCES item(id);')
    # TODO: WRITE CODE HERE
    cursor.close()


# TODO: REPLACE THE VALUES OF FOLLOWING VARIABLES
host = 'localhost'
user = 'root'
password = '' # need to set password
directory = './dataset'

requirement1(host=host, user=user, password=password)
requirement2(host=host, user=user, password=password)
requirement3(host=host, user=user, password=password, directory=directory)
requirement4(host=host, user=user, password=password)