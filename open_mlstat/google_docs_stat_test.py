from open_mlstat.google_docs_stat import GoogleDocsStats
from open_mlstat.tools.helpers import get_commit, get_host_name
from open_mlstat.google_sheets.sheet_query import SheetQuery
from open_mlstat.tools.helpers import current_timestamp


def main():
    # GoogleDrive(acc).create_folder("train_statistics")
    timestamp = current_timestamp()
    gstat = GoogleDocsStats("testing_case", "data/credentials/drive.json")

    query = SheetQuery(1, 1, 0.6, timestamp, 0.2, server_id=get_host_name(), commit=get_commit())
    gstat.add(query, "test_{}".format(timestamp))


if __name__ == '__main__':
    main()
