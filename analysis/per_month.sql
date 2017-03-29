select
    year(min(start_date)) as year,
    month(min(start_date)) as month,
    avg(num_projects) as avg_num_projects,
    count(*) as num_hackathons
from hackathon_info
group by year(start_date), month(start_date);
