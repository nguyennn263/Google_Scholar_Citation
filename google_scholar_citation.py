import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def find_google_citation_profile(_excel_file):
    # Set up Selenium webdriver with Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode, without GUI
    service = Service('/usr/bin/chromedriver')  # Path to chromedriver executable
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Read Excel file and extract names
    df = pd.read_excel(_excel_file)
    names = df['Name'].tolist()

    # Iterate through names and search on Google Scholar
    results = []
    for name in names:
        print(name)
        urls = []
        driver.delete_all_cookies()
        driver.get('https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=' + name.replace(' ', '+'))
        while True:  # Loop until cannot find or use next_button
            profile_links = driver.find_elements(By.CSS_SELECTOR, '.gs_ai_name a')
            if profile_links:
                for link in profile_links:
                    profile_name = link.text
                    if profile_name.lower() == name.lower():
                        url = link.get_attribute('href')
                        urls.append(url)

            next_button = driver.find_elements(By.CSS_SELECTOR, '#gsc_authors_bottom_pag button[aria-label="Next"]')
            
            if next_button:
                if next_button[0].get_attribute('disabled'):
                    break
                else:
                    next_button[0].click()
                    time.sleep(1)        
            else: break
            
        if len(urls) > 1:   
            results.append(f'Multiple Matches:{len(urls)}\n' + '\n'.join(urls))
        elif len(urls) == 1:
            results.append(urls[0])
        else:
            results.append(' ')
        time.sleep(1)
    # Update Excel file with the URLs
    df['GoogleScholar'] = results
    df.to_excel(_excel_file, index=False)
    
    # Quit
    driver.quit()


if __name__ == '__main__':
    excel_file = 'names.xlsx'
    find_google_citation_profile(excel_file);