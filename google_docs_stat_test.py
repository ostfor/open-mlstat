from google_docs_stat import get_host_name, get_commit, GoogleDocsStats
from google_sheets.sheet_query import SheetQuery


def main():
    # GoogleDrive(acc).create_folder("train_statistics")

    gstat = GoogleDocsStats("testing_case", "data/credentials/drive.json")

    query = SheetQuery(1, 1, 0.6, "1906061110", 0.2, server_id=get_host_name(), commit=get_commit())
    gstat.add(query, weights_file="data/weight.ckpt", test_set_file="data/test.1.txt", train_set_file="data/train.1.txt")


if __name__ == '__main__':
    main()
