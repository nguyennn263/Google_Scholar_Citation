from google_scholar_citation import find_google_citation_profile
from format_excel import format_excel

def main():
    excel_file = "names.xlsx"
    find_google_citation_profile(excel_file);
    print ("Finished")
    format_excel(excel_file)

if __name__ == "__main__":
    main()  
    