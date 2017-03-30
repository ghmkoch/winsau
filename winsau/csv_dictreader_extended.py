from csv import DictReader
from terminaltables import AsciiTable


class DictReaderExtended(object, DictReader):
    def __init__(self, caller_cls=None, *args, **kwargs):
        DictReader.__init__(self, *args, **kwargs)
        self.caller_cls = caller_cls

    def __str__(self):

        data = list()

        for i, row in enumerate(self):
            if i is 0:
                data.append([j for j in row.keys()])

            data.append([j for j in row.values()])

        table = AsciiTable(data)
        if self.caller_cls:
            table.title = self.caller_cls.__name__

        return table.table
