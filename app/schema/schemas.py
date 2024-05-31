from typing import List,Dict,Tuple
import datetime

class DataFormatter:
    """
    Convert List of Tuples to List of Dictionary.
    
    Returns:
        List[Dictionary] : Formatted Data
    """
 

    def dictionary_convertor(self,table_columns,table_row) -> Dict:
        """
        Coverter List to dictionary

        Args:
            table_columns (tuple) : hold names of columns
            table_row (tuple) : hold data of single row
        
        Return:
            Dictionary : data with key value Pair
        """

        formatted_data = {}
        for index in range(len(table_row)):
            print(table_row[index])
            if type(table_row[index]) == datetime.date:

                date = table_row[index].strftime("%Y-%m-%d")
                print(date)
                formatted_data[table_columns[index]] = date
            else:
                formatted_data[table_columns[index]] = table_row[index]
        
        print(formatted_data)
        return formatted_data
    
    def dictionary_list(self,table_data,schema = [],table_column = []):
        
        """
        Covert schema and table_data to List of dictionary

        Args:
            schema (List[Tuples]) : hold names of column defination
            table_data (List[Tuple]) : hold data of Table
        
        Return:
            Dictionary[Dictionary] : Formatted Data
        """
        return [self.dictionary_convertor(table_column, table_row ) for table_row in table_data]
        
