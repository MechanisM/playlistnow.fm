-- for mysql
ALTER TABLE auth_user MODIFY username varchar(255);
ALTER TABLE auth_user MODIFY first_name varchar(255);
ALTER TABLE auth_user MODIFY last_name varchar(255);
alter table auth_user auto_increment=40000;
alter table playlist_playlist auto_increment=40000;
alter table music_track auto_increment=40000;
alter table music_artist auto_increment=40000;
-- for postgres
-- ALTER TABLE "auth_user" ALTER "first_name" TYPE varchar(255);
-- ALTER TABLE "auth_user" ALTER "last_name" TYPE varchar(255);
-- ALTER TABLE "auth_user" ALTER "username" TYPE varchar(255);
-- select setval('music_artist_id_seq'::regclass, 40000);
-- select setval('music_track_id_seq'::regclass, 40000);
-- select setval('playlist_playlist_id_seq'::regclass, 40000);
-- select setval('auth_user_id_seq'::regclass, 40000);
