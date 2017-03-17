drop table if exists scrape_status;
create table scrape_status (
    id int not null,
    description varchar(256) not null,

    primary key (id)
);

insert into scrape_status (id, description)
values
    (0, 'not started'),
    (1, 'started'),
    (2, 'finished'),
    (-1, 'nothing found'),
    (-2, 'failed');

drop table if exists hackathon_scrape_status;
create table hackathon_scrape_status (
    hackathon_id int not null references hackathon(id),
    status_id int not null references scrape_status(id)
);

delimiter //
drop trigger if exists hackathon_scrape_status_init//
create trigger hackathon_scrape_status_init
after insert
    on hackathon for each row
begin
    insert into hackathon_scrape_status (hackathon_id, status_id)
    values (new.id, 0);
end//
delimiter ;

insert into hackathon_scrape_status (hackathon_id, status_id)
select id, 0 from hackathon;
