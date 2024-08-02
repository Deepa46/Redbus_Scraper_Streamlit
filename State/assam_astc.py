import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import pandas as pd


driver = webdriver.Chrome()


# Function to extract route name and link
def route_info():
    r_name, r_link = [], []
    head_all = driver.find_element(By.CSS_SELECTOR, 'div.D117_main.D117_container')
    route_element = head_all.find_elements(By.CLASS_NAME, 'route')
    for route_elements in route_element:
        route_link = route_elements.get_attribute('href')
        r_link.append(route_link)
        route_name = route_elements.get_attribute('title')
        r_name.append(route_name)
    return r_name, r_link


# Open the state url
driver.get('https://www.redbus.in/online-booking/astc/?utm_source=rtchometile')
time.sleep(5)

# Get  route name,link from the first page
r_name, r_link = route_info()

# pagination buttons
pagination_container = driver.find_element(By.CLASS_NAME, 'DC_117_paginationTable')
pagination_buttons = pagination_container.find_elements(By.CLASS_NAME, 'DC_117_pageTabs')

# Loop for each pagination number
for page_num in range(1, len(pagination_buttons)):
    try:
        pagination_container = driver.find_element(By.CLASS_NAME, 'DC_117_paginationTable')
        pagination_buttons = pagination_container.find_elements(By.CLASS_NAME, 'DC_117_pageTabs')
        driver.execute_script("arguments[0].scrollIntoView();", pagination_buttons[page_num])
        driver.execute_script("arguments[0].click();", pagination_buttons[page_num])
        time.sleep(5)
        route_names, route_links = route_info()
        r_name.extend(route_names)
        r_link.extend(route_links)
    except Exception as e:
        print(f"Error on page {page_num + 1}: {e}")
        break

# Close the driver
driver.quit()


# Function to click a button(View buss)
def click_button(driver, wait, xpath):
    try:
        button = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView();", button)
        time.sleep(1)  # Wait
        if button.is_displayed() and button.is_enabled():
            driver.execute_script("arguments[0].click();", button)
            wait.until(EC.staleness_of(button))
            return True
    except:
        pass
    return False


# Initialize list to store bus data
route_names_column,route_link_column, bus_names, bus_type, dp_time, duration, ap_time, fare, seat, rating =[], [], [], [], [], [], [], [], [], []

# Scrape bus details for each route
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 50)

for route_name, link in zip(r_name, r_link):
    driver.get(link)

    # Wait for the page to load
    try:
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'clearfix.row-one')))
    except TimeoutException:
        continue
    # Click the "View Buses" buttons
    click_button(driver, wait, '//div[@class="button"][1]')
    try:
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(2)
        click_button(driver, wait, '(//div[@class="button"])[2]')
    except:
        pass
    # to scroll until end of page
    p = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(5)
        new = driver.execute_script("return document.body.scrollHeight")
        if new == p:
            break
        p = new
    #  bus details elements
    bus_details = driver.find_elements(By.CLASS_NAME, 'clearfix.row-one')

    # Extract bus details
    for bus in bus_details:
        try:
            route_names_column.append(route_name)
            route_link_column.append(link)
            bus_names.append(bus.find_element(By.XPATH, './/div[starts-with(@class,"travels")]').text)
            bus_type.append(bus.find_element(By.XPATH, './/div[starts-with(@class,"bus-type")]').text)
            dp_time.append(bus.find_element(By.XPATH, './/div[starts-with(@class,"dp-time")]').text)
            duration.append(bus.find_element(By.XPATH, './/div[starts-with(@class,"dur")]').text)
            ap_time.append(bus.find_element(By.XPATH, './/div[starts-with(@class,"bp-time")]').text)
            fare.append(
                bus.find_element(By.XPATH, './/span[starts-with(@class,"f-19") or starts-with(@class,"f-bold")]').text)
            seat.append(bus.find_element(By.XPATH, './/div[starts-with(@class,"seat-left m-top") ]').text)
            try:
                rating.append(bus.find_element(By.XPATH, ".//div[starts-with(@class, 'lh-18 rating')]/span").text)
            except NoSuchElementException:
                rating.append("0")
        except:
            pass

# Close the driver
driver.quit()

# Save bus data to DataFrame
df = pd.DataFrame({
    "Route Name": route_names_column,
    "Route Link": route_link_column,
    "Bus Name": bus_names,
    "Bus Type": bus_type,
    "Departure Time": dp_time,
    "Duration": duration,
    "Arrival Time": ap_time,
    "Fare": fare,
    "Seats Available": seat,
    "Rating": rating
})

# Save DataFrame to CSV File
df.to_csv('assam_astc.csv', index=False)

print("Data stored in CSV file successfully.")
