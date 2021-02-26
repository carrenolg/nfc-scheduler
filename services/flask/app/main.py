# main
import google_drive_service as drive
import gmail_service as gmail
import scheduler
import spreadsheet_service as spreadsheet


def main():
    # get data from google drive
    data_file = drive.get_data_file()
    # read lines and split each one by ','
    lines = [item.strip().split(',') for item in data_file.split('\n')]
    #  create scheduler
    scheduled = scheduler.data_processing(lines[1:])
    # create spreadsheet
    spreadsheet.create(scheduled)
    # send email with spreadsheet attached, path= utils/
    gmail.send()


if __name__ == '__main__':
    main()
