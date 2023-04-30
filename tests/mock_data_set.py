from abc import abstractmethod


class DataProvider:
    @abstractmethod
    def set_data(self):
        pass


class DataSet:
    prepare = False

    def __init__(self, *args):
        self.all_data_set = []
        for _, v in enumerate(args):
            if not isinstance(v, DataProvider):
                raise TypeError(
                    "required type: DataProvider, given type: " + type(v))
            self.all_data_set.append(v)

    def set_data(self):
        if self.prepare:
            return
        for data in self.all_data_set:
            try:
                data.set_data()
            except:
                pass
        self.prepare = True
