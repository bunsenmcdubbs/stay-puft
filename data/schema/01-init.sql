drop table if exists hackathon;
create table hackathon (
    id int auto_increment not null,
    title varchar(256) not null,
    start_date date not null,
    end_date date not null,
    city varchar(512),
    host varchar(512),
    length int,
    num_participants varchar(32),
    allows_hs bool,
    cost varchar(100),

    primary key (id),
    unique index (title, start_date, end_date),

    index (start_date),
    index (end_date)
);

drop table if exists project;
create table project (
    id int auto_increment not null,
    title varchar(256) not null,
    hackathon_id int not null references hackathon (id),
    github_url varchar(256),
    devpost_url varchar(256),

    primary key (id)
);

drop table if exists devpost_user;
create table devpost_user (
    id int auto_increment not null,
    name varchar(128) not null,
    profile_url varchar(256) not null,

    primary key (id)
);

drop table if exists github_user;
create table github_user (
    id int auto_increment not null,
    name varchar(128) not null,
    profile_url varchar(256) not null,

    primary key (id)
);

drop table if exists project_devpost_submitter;
create table project_devpost_submitter (
    project_id int not null references project (id),
    user_id int not null references devpost_user (id)
);

drop table if exists project_github_contributor;
create table project_github_contributor (
    project_id int not null references project (id),
    user_id int not null references github_user (id)
);
