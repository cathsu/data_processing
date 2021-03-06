from datetime import datetime, timedelta
import pandas as pd
import numpy as np

class MyDataFrame(object): 
    """
    A class used to read a file into a pandas dataframe 

    Attributes
    ---------- 
    file_name : str
        Name of file to be read into CSV 
    df : pd.Dataframe
        Stores the data contained in the file 
    """
    def __init__(self, file_name, df):
        self.file_name = file_name
        self.df = pd.DataFrame()

    def print_df(self) -> None: 
        """Prints the dataframe."""
        
        print(self.df)
    
    def print_dtypes(self) -> pd.Series: 
        """Prints the data types of each column in the dataframe."""
        
        print(self.df.dtypes)
    
    def get_df(self) -> pd.DataFrame: 
        """Returns the dataframe."""
        
        return self.df

    def get_column(self, column_label: str) -> pd.Series:
        """Returns the column associated with the column label"""
        
        return self.df[column_label]
    
    #TODO: What does @property do???
    @property
    def get_column_labels(self) -> pd.Index:
        """Returns the column labels of the dataframe""" 
        
        return self.df.columns
    
    def set_column(self,column_label: str, data_list: list) -> None:
        """Sets the column in the dataframe associated with column label
         equal to the given list"""

        self.df[column_label] = data_list

class ExcelDataFrame (MyDataFrame): 
    """ 
    Extends MyDataFrame to read in the Excel configuration file of the CSV into a pandas dataframe

    Attributes
    ----------
    file_name : str 
        Name of file to be read into CSV 
    df : pd.DataFrame
        Stores the data contained in the file  
    sheet_name : str 
        Name of sheet in Excel file we want read into a dataframe
    """
    def __init__(self, file_name, df, sheet_name): 
        super().__init__(file_name, df)
        self.sheet_name = sheet_name
    
    def create(self) -> None: 
        """Reads a sheet of the configuration file into a dataframe"""

        self.df = self.df.append(pd.read_excel(self.file_name + '.xlsx', sheet_name = self.sheet_name, dtype = {'Title': str}))
    
class MappedExcelDataFrame(ExcelDataFrame): 
    """Extends ExcelDataFrame to process the mapped settings of the configuration file
    
     Attributes
    ----------
    file_name : str 
        Name of file to be read into CSV 
    df : pd.DataFrame
        Stores the data contained in the file  
    sheet_name : str 
        Name of sheet in Excel file we want read into a dataframe
    transpose_col: str
        Indicates whether data is to be transposed
    """
    
    def __init__(self, file_name, df, sheet_name, transpose_col): 
        super().__init__(file_name, df, sheet_name)
        self.transpose_col = transpose_col

    def format(self, col_labels):
        """Alters several settings of the configuration dataframe. 
        Changes: 
            a) Create a new column labeled 'Input Column Numbers' that creates a copy of 'Input' column 
                i)  If data is NOT transposed: coverts the column letters to column numbers.
                ii) If data is transposed: stores a copy of the column numbers   
            b) Column letters/numbers in 'Input' have been replaced by column labels   
            c) Column letters in 'Output' have been replaced by column numbers.  
            d) Empty column titles in 'Title' have been filled in with the original column labels 

        Parameters
        ---------- 
        col_labels : pd.Series
            Original labels of the CSV columns 

        Returns
        ------- 
        None 
        """
        
        # TODO: Research super() https://realpython.com/python-super/
        
        if (not self.transpose_col.dropna().empty and self.transpose_col.loc[0].upper() == 'YES'): 
            super().set_column('Input Column Numbers', super().get_column('Input'))
        else: 
            super().set_column('Input Column Numbers', super().get_column('Input').str.upper())
            data = self._letter2int(super().get_column('Input Column Numbers'))
            super().set_column('Input Column Numbers', data)

        data = self._convert2title(super().get_column('Input'), col_labels)
        super().set_column('Input', data)

        data = self._letter2int(super().get_column('Output'))
        super().set_column('Output', data)

        data = self._default_titles(super().get_column('Title'), super().get_column('Input'))
        super().set_column('Title', data)

    def _convert2title(self, indices, names) -> pd.Series:
        """
        Converts a series that contains CSV column letters or numbers into its corresponding column labels 

        Parameters
        ---------- 
        indices: pd.Series
            Column letters or numbers
        names : pd.Index
            Column labels 

        Returns
        ------- 
        pd.Series 
            New series where column letters have been converted into their column labels 
        """

        col_title = []
        if (self.transpose_col.dropna().empty or self.transpose_col.loc[0].upper() == 'NO'): 
            indices = self._letter2int(indices)
        
        for x in range(indices.size):
            index = indices.loc[x]      
            title = names[index-1]
            col_title.append(title)
        
        return pd.Series(col_title)
    
    def _letter2int(self, letter_series):
        """Converts a Series of Excel column letter into its corresponding column number 
        Source: https://www.geeksforgeeks.org/find-excel-column-number-column-title/

        Parameters
        ---------- 
        letter_series: pd.Series
            Excel column letters

        Returns
        ------ 
        pd.Series
            Letter column values in letter_series have been replaced with their corresponding column number 
        """
        
        result = 0
        for col_letter in letter_series: 
            result = 0
            for x in col_letter: 
                x = x.upper()
                result *= 26
                result += ord(x) - ord('A') + 1   
            letter_series.replace(col_letter, result, inplace=True)
        return letter_series
    
    def _default_titles(self, new_labels, original_labels): 
        """
        Provides a default title to processed CSV columns that were not given a new title in the 
        configuration file. 

        Parameters
        ---------- 
        new_labels : series
            New labels of the processed columns
        original_labels : series
            Old labels of the processed columns 

        Returns
        ------- 
        pd.Series
            Processed CSV columns that were not given a new label are now associated 
            with their original label
        """
        
        x = 0
        for title in new_labels: 
            if (pd.isnull(title)): 
                new_labels.iat[x] = original_labels.iat[x]
            x += 1
        return new_labels

