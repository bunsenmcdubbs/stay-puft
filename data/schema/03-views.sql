drop view if exists hackathon_scrape_status_info;
create view hackathon_scrape_status_info
as 
    select h.id, h.title, hss.status_id, ss.description
    from hackathon h
    join hackathon_scrape_status hss
        on hss.hackathon_id = h.id
    join scrape_status ss
        on ss.id = hss.status_id
    order by hss.status_id desc
;

drop view if exists hackathon_info;
create view hackathon_info
as
    select h.id, h.title, h.start_date, h.end_date, c.num_projects
    from hackathon h
    join (
        select h.id, count(*) as num_projects
        from hackathon h
        join project p
            on h.id = p.hackathon_id
        group by h.id
    ) c
        on c.id = h.id
;

drop view if exists college_hackathon_id;
create view college_hackathon_id
as
    select id
    from hackathon
    where
        host like '%university%' or
        host like '%college%'
;
