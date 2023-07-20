# project-1
Conceptual DB design &amp; DB implementation

## Requirement 1:
make database named "DMA_team10"
if already existing, do not make

## Requirement 2:
create each table if not existing

used SQL syntax
``` SQL
CREATE TABLE IF NOT EXISTS table_name(variables);
```

### user
primary key: id
(BIGINT(20) id, VARCHAR(255) user_name, TINYINT(1) profile_image, INT(11) items_count)

### item
primary key: id
(BIGINT(20) id, VARCHAR(255) item_name, VARCHAR(255) price, TINYINT(1) beta_version, INT(11) ratings, INT(11) metascore, VARCHAR(255) developer, DATE release_date)

### user_item
primary key: user_id, item_id
(BIGINT(20) user_id, INT(11) item_id, INT(11) usagetime_2weeks, INT(11) usagetime_total)

### review
primary key: id
(VARCHAR(255) id, BIGINT(20) user_id, INT(11) item_id, INT(11) recommended, INT(11) body, VARCHAR(255) helpful_score, INT(11) helpful_count, DATE posted_date)

### genre
primary key: id
(VARCHAR(255) id, VARCHAR(255) genre_name)

### item_genre
primary key: item_id, genre_id
(INT(11) item_id, VARCHAR(255) genre_id)

### bundle
primary key: id
(INT(11) bundle_id, VARCHAR(255) bundle_name, VARCHAR(255) price, VARCHAR(255) final_price, VARCHAR(255) discount)

### bundle_item
primary key: bundle_id, item_id
(INT(11) bundle_id, INT(11) item_id)

### bundle_genre
primary key: bundle_id, genre_id
(INT(11) bundle_id, VARCHAR(255) genre_id)

### tag
primary key: item_id, tag_name
(INT(11) item_id, VARCHAR(255) tag_name, INT(11) tag_order)

### item_specs
primary key: item_id, spec_name
(INT(11) item_id, VARCHAR(255) spec_name)

## Requirement3
used SQL syntax
```SQL
INSERT INTO table_name VALUES (input_data);
```
```python
def insert2Table(tablename):
        print(tablename)
        filepath = directory + '/' + '{}.csv'.format(tablename)
        with open(filepath, 'r', encoding='utf-8') as f:
            for row in f.readlines()[1:]:
                row = row.strip().split(',')
                row = [str(value) if value.isnumeric() else '\"{}\"'.format(value) if value != "" else 'null' for value in row]
                values = ','.join(row)
                cursor.execute('INSERT INTO {} VALUES ({});'.format(tablename, values))
```
opens the csv file corresponding with the table name
read each by line and insert data for each variables

## Requirement4
used SQL syntax example
```SQL
ALTER TABLE user_item ADD CONSTRAINT FOREIGN KEY (user_id) REFERENCES user(id);
```
after data insert, set foreign keys