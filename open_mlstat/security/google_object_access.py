from googleapiclient.errors import HttpError
import logging


class ObjectAccess:
    def __init__(self, acc, who_access='anyone', role='writer'):
        self.logger= logging.getLogger(__name__)
        self.google_acc = acc
        email = None

        if "@" in who_access:
            email = who_access
            who_access = "user"

        self.__body = {'type': who_access, 'role': role}

        if email is not None:
            self.__body["value"] = email

    def set_roles(self, idx):
        try:
            return self.google_acc.drive_service.permissions().create(
                fileId=idx,
                body=self.__body,
                fields='id'
            ).execute()
        except HttpError as err:
            self.logger.error("Http Error while setting access write %s", err)
            return None
