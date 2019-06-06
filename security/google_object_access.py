class ObjectAccess:
    def __init__(self, acc, who_access='anyone', role='writer'):
        self.google_acc = acc
        email = None

        if "@" in who_access:
            email = who_access
            who_access = "user"

        self.__body = {'type': who_access, 'role': role}

        if email is not None:
            self.__body["value"] = email

    def set_roles(self, idx):
        return self.google_acc.drive_service.permissions().create(
            fileId=idx,
            body=self.__body,
            fields='id'
        ).execute()