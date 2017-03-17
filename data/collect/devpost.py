from collections import defaultdict

from scraper import get_submission_url, get_projects_info, get_contributors
import db

STATUS_UPDATE = lambda status_id: lambda hackathon_id: "UPDATE hackathon_scrape_status SET status_id = {} WHERE hackathon_id = {}".format(status_id, hackathon_id)
NOT_STARTED = STATUS_UPDATE(0)
PROJECTS_STARTED = STATUS_UPDATE(1)
PROJECTS_COMPLETED = STATUS_UPDATE(2)
CONTRIBUTORS_STARTED = STATUS_UPDATE(3)
CONTRIBUTORS_COMPLETED = STATUS_UPDATE(4)
NOTHING_FOUND = STATUS_UPDATE(-1)
PROJECTS_FAILED = STATUS_UPDATE(-2)
CONTRIBUTORS_FAILED = STATUS_UPDATE(-3)

# grab all the info from devpost! NOT DONE
# select rows from the database and page scrape
def scrape_devpost(conn, verbose=False, silent=True):
    query = "SELECT id, title, start_date, end_date FROM hackathon LIMIT 6"
    with conn.cursor() as cursor:
        cursor.execute(query)
        for x in range(0, cursor.rowcount):
            row = cursor.fetchone()
            if verbose and not silent:
                print(row['title'], end=' ', flush=True)
            elif not silent:
                print('.', end=' ', flush=True)
            save_hackathon_projects(conn, row['id'], row['title'], row['start_date'], row['end_date'], verbose=verbose, silent=silent)
        if not verbose and not silent:
            print()
    # TODO query and populate all projects' contributors
    #raise NotImplementedError

# save a hackathon's projects into the database
def save_hackathon_projects(conn, h_id, h_title, h_start, h_end, verbose=False, silent=True):
    submission_url = get_submission_url(h_title, h_start, h_end)
    if verbose and not silent:
        print(submission_url)
    elif not silent:
        pass
    with conn.cursor() as cursor:
        if submission_url is None:
            cursor.execute(NOTHING_FOUND(h_id))
            conn.commit()
        else:
            project_info = get_projects_info(submission_url)
            cursor.execute(PROJECTS_STARTED(h_id))
            conn.commit()
            try:
                with conn.cursor() as ap_cursor:
                    add_project_query = "INSERT INTO project (hackathon_id, title, devpost_url) VALUES (%s, %s, %s)"
                    add_project = lambda h_id, title, url: ap_cursor.execute(add_project_query, (h_id, title, url))
                    for title, devpost_url in project_info:
                        add_project(h_id, title, devpost_url)
                    conn.commit()
            except Exception as err:
                if not silent:
                    print("Failed on hackathon #{} ({})".format(h_id, h_title))
                cursor.execute(PROJECTS_FAILED(h_id))
                conn.commit()
                raise(err)
            cursor.execute(PROJECTS_COMPLETED(h_id))
            conn.commit()

# save project into the database (and all its contibutors)
def save_project(conn, h_id, title, url, verbose=False, silent=True):
    with conn.cursor() as cursor:
        cursor.execute(add_project, (h_id, title, url))

# save person into the database (skip if already present)
def save_person(conn, name, devpost_username, verbose=False, silent=True):
    raise NotImplementedError

if __name__=='__main__':
    print(scrape_devpost(db.get_conn(), silent=False))
