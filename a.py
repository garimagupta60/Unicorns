from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
import streamlit as st
import pandas as pd
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')  # Sometimes needed for headless mode


# service = Service(
#   ChromeDriverManager().install()
# )

driver = webdriver.Chrome(
  options=chrome_options
)

def scrapper():  # corrected function name and parameter name
    
    try: 
        # query = input("Enter your search query: ")
        # encoded_query = urllib.parse.quote_plus(query)

        driver.get('https://www.investindia.gov.in/indian-unicorn-landscape')
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "uni-logos")))
        items = driver.find_elements(By.CLASS_NAME, "uni-logos")
        results = []
        for item in items:
            urls=item.find_elements(By.CSS_SELECTOR,'a')
            for url in urls:
                results.append(url.get_attribute('href'))
        df = pd.DataFrame(results)
        csv_data = df.to_csv(index=False)
        with open('unicorn.csv', 'w', encoding='utf-8') as f:
            f.write(csv_data)

        return csv_data
    finally:
        driver.quit()

def main():
    st.title('Unicorn Scrapper')
    html_temp=""
    if st.button('Search'):
            csv_data = scrapper()
            if csv_data:  # Check if `csv_data` is not None
                st.success("Finally scrapped")

                # Add download button for CSV
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name='unicorn.csv',
                    mime='text/csv'
                )
            else:
                st.error("An error occurred while scraping.")
    
if __name__=='__main__':
    main()
     

