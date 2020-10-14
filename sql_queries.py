import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events(
artist varchar, 
auth varchar NOT NULL, 
firstName varchar, 
gender char, 
itemInSession int NOT NULL, 
lastName varchar, 
length float, 
level varchar NOT NULL, 
location varchar,
method varchar,
page varchar NOT NULL,
registration varchar,
sessionId int NOT NULL,
song varchar,
status int,
ts bigint NOT NULL,
userAgent varchar,
userId int
);

""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs(
num_songs int NOT NULL, 
artist_id varchar NOT NULL, 
artist_latitude varchar, 
artist_longitude varchar, 
artist_location varchar, 
artist_name varchar, 
song_id varchar NOT NULL, 
title text, 
duration float,
year int
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users(
user_id int PRIMARY KEY, 
first_name varchar NOT NULL, 
last_name varchar NOT NULL, 
gender varchar, 
level varchar
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs(
song_id varchar PRIMARY KEY, 
title varchar NOT NULL, 
artist_id varchar, 
year int, 
duration float
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists(
artist_id varchar PRIMARY KEY, 
name varchar NOT NULL, 
location text, 
latitude float, 
longitude float
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time(
start_time timestamp PRIMARY KEY NOT NULL, 
hour int, 
day int, 
week int, 
month int, 
year int, 
weekday int
);
""")


songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays(
songplay_id int IDENTITY(1, 1) PRIMARY KEY, 
start_time timestamp REFERENCES time(start_time) NOT NULL, 
user_id int REFERENCES users(user_id) NOT NULL, 
level varchar, 
song_id varchar REFERENCES songs(song_id), 
artist_id varchar REFERENCES artists(artist_id), 
session_id int, 
location text, 
user_agent text
);
""")

# STAGING TABLES

staging_events_copy = ("""
    COPY staging_events from {}
    IAM_ROLE '{}'
    format as json {}
""").format(config.get("S3", "LOG_DATA"), config.get("IAM_ROLE","ARN"), config.get("S3", "LOG_JSONPATH"))

staging_songs_copy = ("""
COPY staging_songs from {}
    IAM_ROLE '{}'
    format as json 'auto'
""").format(config.get("S3", "SONG_DATA"), config.get("IAM_ROLE","ARN"))

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, 
artist_id, session_id, location, user_agent)
SELECT DISTINCT TIMESTAMP 'epoch' + se.ts/1000 * interval '1 second' as start_time, se.userId, se.level, ss.song_id, ss.artist_id, se.sessionId, se.location, se.userAgent
FROM staging_events AS se
JOIN staging_songs AS ss
ON ss.title = se.song AND ss.artist_name = se.artist
WHERE se.page = 'NextSong';
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
SELECT DISTINCT userId, firstName, lastName, gender, level
FROM staging_events
WHERE userId IS NOT NULL AND page = 'NextSong';
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
SELECT DISTINCT song_id, title, artist_id, year, duration
FROM staging_songs
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
SELECT DISTINCT artist_id, artist_name, artist_location AS location, CAST(artist_latitude AS float) AS latitude, CAST(artist_longitude AS float) AS longitude
FROM staging_songs
""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
SELECT DISTINCT t.start_time, EXTRACT(hour from t.start_time) as hour, EXTRACT(day from t.start_time) as day, EXTRACT(week from t.start_time) as week, EXTRACT(month from t.start_time) as month, EXTRACT(year from t.start_time) as year, EXTRACT(weekday from t.start_time) as weekday
FROM (SELECT start_time
FROM songplays) AS t
WHERE start_time IS NOT NULL;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]