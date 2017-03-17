from collections import defaultdict

from scraper import get_submission_url, get_projects_info, get_contributors
import db

# grab all the info from devpost! CURRENTLY TESTING ONLY
# select rows from the database and page scrape
# currently returns a histogram of # contributors per project
def scrape_devpost(conn, verbose=False, silent=True):
    query = "SELECT id, title, start_date, end_date FROM hackathon LIMIT 6"
    with conn.cursor() as cursor:
        cursor.execute(query)
        hist = defaultdict(int)
        for x in range(0, cursor.rowcount):
            row = cursor.fetchone()
            if verbose and not silent:
                print(row['title'], end=' ', flush=True)
            elif not silent:
                print('.', end=' ', flush=True)
            save_hackathon(conn, row, verbose=verbose, silent=silent)
        if not verbose and not silent:
            print()
        return hist

def save_hackathon(conn, row, verbose=False, silent=True):
    update_progress = "UPDATE hackathon_scrape_status SET status_id = {{}} WHERE hackathon_id = {}".format(row['id'])
    start_progress = update_progress.format(1)
    end_progress = update_progress.format(2)
    nothing_found = update_progress.format(-1)
    failed_progress = update_progress.format(-2)
    submission_url = get_submission_url(row['title'], row['start_date'], row['end_date'])
    if verbose and not silent:
        print(submission_url)
    elif not silent:
        pass
    with conn.cursor() as cursor:
        if submission_url is None:
            cursor.execute(nothing_found)
            conn.commit()
        else:
            project_info = get_projects_info(submission_url)
            cursor.execute(start_progress)
            conn.commit()
            try:
                for title, devpost_url in project_info:
                    save_project(conn, row['id'], title, devpost_url, verbose=verbose, silent=silent)
                    contributors = get_contributors(devpost_url)
            except Exception as err:
                if not silent:
                    print("Failed on hackathon #{} ({})".format(row['id'], row['title']))
                cursor.execute(failed_progress)
                conn.commit()
                raise(err)
            cursor.execute(end_progress)
            conn.commit()

def save_project(conn, h_id, title, url, verbose=False, silent=True):
    add_project = "INSERT INTO project (hackathon_id, title, devpost_url) VALUES ({}, {}, {})".format(h_id, title, url)
    print(add_project)
    raise NotImplementedError

if __name__=='__main__':
    print(scrape_devpost(db.get_conn(), silent=False))
