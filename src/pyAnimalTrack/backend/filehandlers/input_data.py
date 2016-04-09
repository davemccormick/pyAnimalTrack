
class InputData(object):
    """ Base input class to inherit from. Methods are all effectively pure virtual.
    """

    def __init__(self):
        return
        

    def getData(self):
        """ Source the data and return an object with accessible attributes.
        """

        raise Exception("Child class must implement this method.")


    def getColumn(self, columnName):
        """ Get a column of data from within the object.
            Object should be able to access a columnName of data as an attribute.
        """

        raise Exception("Child class must implement this method.")


