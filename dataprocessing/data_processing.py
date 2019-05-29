import pandas as pd
import user_interface
import dataframes 
import files
import directory as dir

if __name__ == '__main__': 
    ### Main execution block ###
    user_interface.banner()

    repeat = 'y'
    while (repeat.lower() == 'y'): 
        #try: 
        config_list = user_interface.choose_config()
        config_sheet_list = config_list[0]
        config_title = config_list[1]
        input_csv = user_interface.choose_csv()
        output_name = user_interface.choose_output_name()

        # Read the two sheets of the configuration file: 'Mapped' and 'General' Settings into two different dataframes
        mapped_df = dataframes.MappedExcelDataFrame(config_title, pd.DataFrame(), config_sheet_list.sheetnames[0])
        mapped_df.create()
        general_df = dataframes.ExcelDataFrame(config_title, pd.DataFrame(), config_sheet_list.sheetnames[1])
        general_df.create()

        # Create a dataframe to hold the raw CSV file and then read said dataframe into an Excel file 
        raw_data_df = dataframes.CSVDataFrame(input_csv, pd.DataFrame(), mapped_df, general_df, input_csv)
        raw_data_df.create()
        raw_data_df.read_into_excel()

        # Convert the 'Input' and 'Output' column letters into, respectively, column titles and numbers. 
        # Keep a standalone copy of the 'Output.'
        mapped_df.format(raw_data_df.get_column_labels)

        # Store the columns we want mapped into a new dataframe 
        output_df = raw_data_df.map_columns()

        # Convert times into elapsed times 
        raw_data_df.convert_to_elapsed_time(output_df)

        # Create output files 
        excel_file = files.ExcelFile(mapped_df,general_df,output_df, output_name)
        excel_file.output()

        jpeg_file = files.JPEGFile(mapped_df, general_df, output_df, output_name)
        jpeg_file.output()

        pdf_file = files.PDFFile(mapped_df, general_df, output_df, output_name)
        pdf_file.output()

        txt_file = files.TXTFile(mapped_df, general_df, output_df, output_name)
        txt_file.output()

        # Create directory and move files 
        directory = dir.Directory(output_name, 
                                    raw_data_df.get_name(), 
                                    excel_file.get_name(), 
                                    jpeg_file.get_name(), 
                                    pdf_file.get_name(), 
                                    txt_file.get_name())
        directory.create()

        #repeat = input('Do you want to process another CSV? (y/n): ')
        #except: 
        #print('This is an error message')
        repeat = input('Do you want to process another CSV? (y/n): ')

