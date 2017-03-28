from collections import defaultdict

from scraper import get_submission_url, get_projects_info, get_contributors
import db

STATUS_UPDATE = lambda status_id: lambda hackathon_id: "UPDATE hackathon_scrape_status SET status_id = {} WHERE hackathon_id = {}".format(status_id, hackathon_id)
NOT_STARTED = 0
PROJECTS_STARTED = 1
PROJECTS_COMPLETED = 2
CONTRIBUTORS_STARTED = 3
CONTRIBUTORS_COMPLETED = 4
NOTHING_FOUND = -1
PROJECTS_FAILED = -2
CONTRIBUTORS_FAILED = -3

# grab all the info from devpost! NOT DONE
# select rows from the database and page scrape
# TODO implement retry
def scrape_devpost(conn, verbose=False, silent=True):
    query = "SELECT h.id AS id, h.title AS title, h.start_date AS start_date, h.end_date AS end_date, s.status_id AS status_id FROM hackathon AS h JOIN hackathon_scrape_status AS s ON h.id = s.hackathon_id"
    with conn.cursor() as cursor:
        cursor.execute(query)
        for x in range(0, cursor.rowcount):
            # TODO make this printing better/more consistent (esp. status)
            row = cursor.fetchone()
            if verbose and not silent:
                print(row['title'], end=' ', flush=True)
            elif not silent:
                print('.', end=' ', flush=True)
            if row['status_id'] is NOT_STARTED:
                save_hackathon_projects(conn, row['id'], row['title'], row['start_date'], row['end_date'], verbose=verbose, silent=silent)
            elif not silent and verbose:
                print('status_id: {}'.format(row['status_id']))
            elif not silent and not verbose:
                print('x', end=' ', flush=True)
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
            cursor.execute(STATUS_UPDATE(NOTHING_FOUND)(h_id))
            conn.commit()
        else:
            project_info = get_projects_info(submission_url)
            cursor.execute(STATUS_UPDATE(PROJECTS_STARTED)(h_id))
            conn.commit()
            try:
                with conn.cursor() as ap_cursor:
                    # TODO BUG: (in PennApps Fall 2014
                    # UnicodeEncodeError: 'latin-1' codec can't encode character '\u25bc' inposition 67: ordinal not in range(256)
                    add_project_query = "INSERT INTO project (hackathon_id, title, devpost_url) VALUES (%s, %s, %s)"
                    add_project = lambda h_id, title, url: ap_cursor.execute(add_project_query, (h_id, title.encode('unicode_escape'), url))
                    for title, devpost_url in project_info:
                        add_project(h_id, title, devpost_url)
                    conn.commit()
            except Exception as err:
                if not silent:
                    print("Failed on hackathon #{} ({})".format(h_id, h_title))
                    print("Project {} {}".format(title, devpost_url))
                cursor.execute(STATUS_UPDATE(PROJECTS_FAILED)(h_id))
                # TODO rollback ap_cursor's inserts?
                conn.commit()
                raise(err)
            cursor.execute(STATUS_UPDATE(PROJECTS_COMPLETED)(h_id))
            conn.commit()

# save project into the database (and all its contibutors)
def save_project(conn, h_id, title, url, verbose=False, silent=True):
    with conn.cursor() as cursor:
        cursor.execute(add_project, (h_id, title, url))

# save person into the database (skip if already present)
def save_person(conn, name, devpost_username, verbose=False, silent=True):
    raise NotImplementedError

if __name__=='__main__':
    scrape_devpost(db.get_conn(), silent=False)
