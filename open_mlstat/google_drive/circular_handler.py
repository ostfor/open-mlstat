from googleapiclient.http import HttpError
import logging
import csv


def find_bad_files(good_ids, file_metas):
    bad_ids = []
    _good_ids = []

    for file_m in file_metas:
        _id = file_m['id']
        if _id in good_ids:
            _good_ids.append(_id)
        else:
            bad_ids.append(_id)
    return bad_ids, _good_ids


def parser(fname="./data/Statistics - HandSeg_Default.csv"):
    def process_block(block, id_prefix="File id: "):
        fields = block.split('\n')
        field = None
        for f in fields:
            if id_prefix in f:
                field = f
                break
        if field is None:
            raise RuntimeError("Can'not find prefix " + id_prefix + " in block")
        return field.strip(id_prefix)

    with open(fname, 'r') as f:
        block_id = 6
        reader = csv.reader(f)
        good_indexes = []
        for row in reader:
            if 'v' in row[0]:
                good_indexes.append(process_block(row[block_id]))
        return good_indexes


def delete_all_bad(gstat):
    # WARNING: !!! Not use it until fix this error
    # TODO: find "bads" smarter: avoid adding folders to "badS"
    ls_query_result = gstat.acc.drive_service.files().list(pageSize=1000).execute()
    bad, _good_ids = find_bad_files(ground_good_ids, ls_query_result["files"])

    del_commands = []
    for bad_id in bad:
        if bad_id in _good_ids:
            print("not good")
        else:
            # TODO: HERE: Not Delete Folders
            del_commands.append(gstat.acc.drive_service.files().delete(fileId=bad_id))

    for d in del_commands:
        try:
            d.execute()
        except HttpError as e:
            print(e)

    ls_query_result = gstat.acc.drive_service.files().list(pageSize=1000).execute()
    assert len(ls_query_result['files']) == len(_good_ids)


def emptyTrash(gstat):
    gstat.acc.drive_service.files().emptyTrash().execute()


def get_storage_limits(gstat):
    a = gstat.acc.drive_service.about().get(fields='*').execute()
    quota = a["storageQuota"]
    free_space = int(quota['limit']) - int(quota['usage'])
    free_space_mb = free_space / 1024 / 1024.0
    available_space_mb = int(quota['limit']) / 1024 / 1024.0
    logging.info("Free %s MB from %s MB", free_space_mb, available_space_mb)

    return free_space_mb / available_space_mb
