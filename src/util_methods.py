import datetime
def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d/%m/%Y')
        return True
    except ValueError:
        print("Incorrect data format, should be DD/MM/YYYY")
