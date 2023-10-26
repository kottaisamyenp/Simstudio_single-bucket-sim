#pytest main_2.py --html=report.html
#open report.html
#with automatic user creation
import os
import time
import pytest
import math
from faker import Faker
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from prices_store import prices,price_zyngBeanz,price_others
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_experimental_option("detach", True)
    #driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit() 
 

def test_user_creation_and_login(driver):
    # Open the website
    driver.get('https://simstudioadmin-uat.catalyx.live/signin')
    original_window = driver.current_window_handle

    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//iframe[@title='Sign in with Google Button']"))
    )
    driver.switch_to.frame(iframe)

    # Locate and click the Google Sign-In button with explicit wait
    google_sign_in_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='container']/div/div[2]/span[1]"))
    )
    google_sign_in_button.click()

    driver.switch_to.window(driver.window_handles[-1])

    email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'identifierId')))
    email_input.send_keys('kottaisamy.k@enparadigm.com')

    next_button = driver.find_element(By.XPATH, '//*[@id="identifierNext"]')
    next_button.click()

    password_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
    password_input.send_keys('Test_enp@1234')
    next_button = driver.find_element(By.XPATH, '//*[@id="passwordNext"]')
    next_button.click()

    driver.switch_to.window(original_window)
    create_user = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebar-left"]/div[1]/div[2]/label[3]/div/div[2]/div/span')))
    create_user.click()


    fake = Faker()
    random_username = fake.email()
    random_name = fake.name()
    print(random_username)
    print(random_name)

    name_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="name"]')))
    username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="user_name"]')))

    username_input.send_keys(random_username)
    name_input.send_keys(random_name)

    save_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="create_user_btn"]')))
    save_button.click()
    time.sleep(1)
    
    new_url = "https://simstudio-uat.catalyx.live/signin?module_id=d37817a3-a0c8-4942-a788-c000af6265e0"
    driver.get(new_url)
    time.sleep(1)
    login = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@id='user_name']")))
    login.send_keys(random_username, Keys.ENTER)
    time.sleep(3)



#login
def test_login(driver):
    global popup_detected
    assertion_result = True  # Initialize the assertion result as True
    try:
        wait = WebDriverWait(driver,2)
        popup_message = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='swal2-content']")))
        print(popup_message.text)
        if popup_message.is_displayed():
            # If the popup message is displayed, set the flag and quit the WebDriver
            popup_detected = True
            driver.quit()
            assertion_result = False  # Set the assertion result to False               
    except:
        pass
    if not assertion_result:
        assert False, "User Not Found"  


final_market_share_value = []
changed_sliders_value_in_period_1 = []
changed_sliders_value_in_period_2 = []
changed_sliders_value_in_period_3 = []
changed_sliders_value_in_period_4 = []
timestamp = time.strftime("%H%M%S_%Y%m%d")
popup_detected = False

#making directory for screenshots
screenshot_true = f'screenshots/assert_true/{timestamp}/'
if not os.path.exists(screenshot_true):
    os.makedirs(screenshot_true)
screenshot_false = f'screenshots/assert_false/{timestamp}/'
if not os.path.exists(screenshot_false):
    os.makedirs(screenshot_false)   
 

# First Page After login
def test_simulation_name(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='header-simulation-name padding-left-45 padding-top-10 padding-bottom-10 theme-font2']")))
    actual_text = element.text
    expected_text = "Anchor"
    print(actual_text)
    if actual_text == expected_text:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'welcome_page.png'))
    else:  
        driver.save_screenshot(os.path.join(screenshot_false, 'welcome_page.png')) 
        assert actual_text == expected_text, f"Text verification failed. Expected: '{expected_text}', Actual: '{actual_text}'"
    
def test_first_page_heading(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    
    heading = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='heading theme-font16']")))
    actual_heading = heading.text
    expected_heading = "A new mission awaits!"
    print(actual_heading)
    if actual_heading == expected_heading:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'welcome_page.png'))
    else:   
        driver.save_screenshot(os.path.join(screenshot_false, 'welcome_page.png')) 
        assert actual_heading == expected_heading, f"Heading verification failed. Expected: '{expected_heading}', Actual: '{actual_heading}'"
    
def test_first_page_content(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    
    content = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'As you open your laptop on a Monday morning, you h')]")))
    actual_content = content.text
    print(actual_content)
    expected_content = "As you open your laptop on a Monday morning, you have a mail from your Managing Director, Dr. Bean himself!"
    if actual_content == expected_content:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'welcome_page.png'))
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'welcome_page.png'))
        assert actual_content == expected_content, f"Content verification failed. Expected: '{expected_content}', Actual: '{actual_content}'"
    
def test_first_page_content_intrigued(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    content_intrigued = driver.find_element(By.XPATH, "//p[contains(text(),'Intrigued, you open')]")
    actual_content_intrigued = content_intrigued.text
    print(actual_content_intrigued)
    expected_content_intregued = "Intrigued, you open the mail to see what it says…"
    if actual_content_intrigued == expected_content_intregued:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'welcome_page.png'))
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'welcome_page.png'))
        assert actual_content_intrigued == expected_content_intregued, f"Content verification failed. Expected: '{expected_content_intregued}', Actual: '{actual_content_intrigued}'"


# clicking next button 3 times to reach case summary page
def test_click_next_button_1(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@class='nextButton theme-font15']")))
    button.click()
    print("Next button clicked")
    time.sleep(15)
def test_click_next_button_2(driver):     
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.") 
    button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@class='nextButton theme-font15']")))
    button.click()
    print("Next button clicked")
    time.sleep(15)
def test_click_next_button_3(driver):     
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.") 
    button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@class='nextButton theme-font15']")))
    button.click()
    print("Next button clicked")
    time.sleep(15)
        

#case summary
def test_case_summary(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    kpi_1_content = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[normalize-space()='Final Market Share (Units)']")))
    actual_kpi_1_content = kpi_1_content.text
    expected_kpi_1_content = "Final Market Share (Units)"
    print(actual_kpi_1_content)
    if actual_kpi_1_content == expected_kpi_1_content:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'case_summary.png'))
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'case_summary.png'))
        assert actual_kpi_1_content == expected_kpi_1_content, f"Content verification failed. Expected: '{expected_kpi_1_content}', Actual: '{actual_kpi_1_content}'"

    kpi_1_perc = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='case_study_container']//div[1]//div[4]")))
    actual_kpi_1_perc = kpi_1_perc.text
    expected_kpi_1_perc = "27 %"
    print(actual_kpi_1_perc)
    if actual_kpi_1_perc == expected_kpi_1_perc:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'case_summary.png'))
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'case_summary.png'))
        assert actual_kpi_1_perc == expected_kpi_1_perc, f"Content verification failed. Expected: '{expected_kpi_1_perc}', Actual: '{actual_kpi_1_perc}'"

    kpi_2_content = driver.find_element(By.XPATH, "//div[normalize-space()='Cumulative Operating Margin %']")
    actual_kpi_2_content = kpi_2_content.text
    expected_kpi_2_content = "Cumulative Operating Margin %"
    print(actual_kpi_2_content)
    if actual_kpi_2_content == expected_kpi_2_content:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'case_summary.png'))
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'case_summary.png'))
        assert actual_kpi_2_content == expected_kpi_2_content, f"Content verification failed. Expected: '{expected_kpi_2_content}', Actual: '{actual_kpi_2_content}'"

    kpi_2_perc = driver.find_element(By.XPATH, "//div[@id='sib_case_study']//div[2]//div[4]")
    actual_kpi_2_perc = kpi_2_perc.text
    expected_kpi_2_perc = "5 %"
    print(actual_kpi_2_perc)
    if actual_kpi_2_perc == expected_kpi_2_perc:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'case_summary.png'))
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'case_summary.png'))
        assert actual_kpi_2_perc == expected_kpi_2_perc, f"Content verification failed. Expected: '{expected_kpi_2_perc}', Actual: '{actual_kpi_2_perc}'"

def test_table1_in_case_summary(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    table1 = driver.find_element(By.XPATH, "//*[@id='sib_case_study']/div/div[6]/div[1]/table")
    rows_table1 = table1.find_elements(By.XPATH, "//*[@id='sib_case_study']/div/div[6]/div[1]/table/tbody/tr")
    table1_data = []

    for row in rows_table1:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text for cell in cells]
        table1_data.append(row_data)

    expected_table1_data = [
        ["1", "40,800"],
        ["2", "53,400"],
        ["3", "69,100"],
        ["4", "90,000"],
    ]
    if table1_data == expected_table1_data:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'case_summary.png'))
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'case_summary.png'))
        assert table1_data == expected_table1_data, "Table data does not match expected data."

def test_table2_in_case_summary(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    table2 = driver.find_element(By.XPATH, "//*[@id='sib_case_study']/div/div[8]/table")
    rows_table2 = table2.find_elements(By.XPATH, "//*[@id='sib_case_study']/div/div[8]/table/tbody/tr")
    table2_data = []

    for row in rows_table2:
        cells = row.find_elements(By.TAG_NAME, "td")
        second_column_text = cells[1].text
        third_column_text = cells[2].text
        table2_data.append([second_column_text, third_column_text])

    expected_table2_data = [
        ["120", "160"],
        ["0", "200,000"],
        ["0", "100,000"],
        ["0", "200,000"],
    ]
    if table2_data == expected_table2_data:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'case_summary.png'))
    else:    
        driver.save_screenshot(os.path.join(screenshot_false, 'case_summary.png'))
        assert table2_data == expected_table2_data, "Table data does not match expected data."


def test_next_button_in_case_summary(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='buttonContainer']//button[@class='nextButton theme-font15'][normalize-space()='Next']")))
    button.click()
    print("Next button clicked in case summary page")
    time.sleep(5)


# ************ Period 1 ************** 
def test_period_1_sliders_default_value(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("************* Testing in Period 1 ************** ")
    ##verify sliders default values
    extracted_values = []
    expected_values = ['140', '100000', '50000', '100000']
    sliders = driver.find_elements(By.CSS_SELECTOR, '[role="slider"]')
    for slider in sliders:
        try:
            aria_valuenow = slider.get_attribute('aria-valuenow')
            extracted_values.append(aria_valuenow)
        except Exception as e:
            # Handle any exceptions, e.g., when the attribute is not found
            print(f"Error while processing a slider: {e}")
    non_zero_values = [value for value in extracted_values if value != '0']
    if set(non_zero_values) == set(expected_values):
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_1.png'))
        print("Assertion passed. Sliders Values match the expected values.")
    else:    
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_1.png'))
        assert set(non_zero_values) == set(expected_values), f"Values do not match. Expected: {set(expected_values)}, Actual: {set(non_zero_values)}"

    #verify projected Revenue value
def test_period_1_projected_revenue(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    proj_rev = driver.find_element(By.XPATH,"//div[@class='revenue_value theme-font8']")
    actual_proj_rev = proj_rev.text
    expected_proj_rev = "USD 1,142,400"
    if actual_proj_rev == expected_proj_rev:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_1.png'))
        print("Proj_rev is matched ")                               
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_1.png'))
        assert actual_proj_rev == expected_proj_rev, f"Text verification failed. Expected: '{expected_proj_rev}', Actual: '{actual_proj_rev}'"


    #verfy projected Operating margin
def test_period_1_projected_operating_margin(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    proj_mg = driver.find_element(By.XPATH,"//div[@class='operating_margin_value theme-font8']")
    actual_proj_mg = proj_mg.text
    expected_proj_mg = "USD 57,720"
    if actual_proj_mg == expected_proj_mg:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_1.png'))
        print("Proj_mg is matched ")                            
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_1.png'))
        assert actual_proj_mg == expected_proj_mg, f"Text verification failed. Expected: '{expected_proj_mg}', Actual: '{actual_proj_mg}'"

    #company performance content
def test_period_1_performance_content(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    perf_cont = driver.find_element(By.XPATH,"//div[@class='theme-font7 font-weight-500 padding-top-10']")
    actual_perf_cont = perf_cont.text
    expected_perf_cont = "Performance is calculated considering similar market share as last month: 20%"
    if actual_perf_cont == expected_perf_cont:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_1.png'))
        print("perf_cont is matched ")   
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_1.png'))                 
        assert actual_perf_cont == expected_perf_cont, f"Text verification failed. Expected: '{expected_perf_cont}', Actual: '{actual_perf_cont}'"

    #click on expand all
def test_period_1_expand_all(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    exp_btn = driver.find_element(By.XPATH,"//button[@id='expand_all_report']")
    exp_btn.click()
    print("Expand all clicked")

    time.sleep(2)
    #Profit And Loss Statement
def test_period_1_profit_loss_statement(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    pl_cont = driver.find_element(By.XPATH,"//div[@class='theme-font7 font-weight-500']")
    print(pl_cont.text)
    actual_pl_cont = pl_cont.text
    expected_pl_cont = "Hover over the items for the explanation."
    if actual_pl_cont == expected_pl_cont:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_1.png'))
        print("profit loss statement matched")  
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_1.png'))                               
        assert actual_pl_cont == expected_pl_cont, f"Text verification failed. Expected: '{expected_pl_cont}', Actual: '{actual_pl_cont}'"


    ##verify profit-loss table default data
def test_period_1_table_1(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    table = driver.find_element(By.CLASS_NAME, "bold_pandl")

    # Extract data from the table
    table_data = []
    for row in table.find_elements(By.TAG_NAME, "tr"):
        row_data = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
        if row_data:
            table_data.append(row_data)

    # Define the expected data
    expected_data = [
        ["Revenue", "1,142,400"],
        ["COGS", "(799,680)"],
        ["Gross Margin", "342,720"],
        ["Fixed Cost", "(23,000)"],
        ["Advertising", "(100,000)"],
        ["Sales Force Cost", "(50,000)"],
        ["Quality Control Cost", "(100,000)"],
        ["Admin Expense", "(12,000)"],
        ["Operating Margin / EBITDA", "57,720"]
    ]
    if table_data == expected_data:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_1.png'))
        print("Default pl table data matched" )
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_1.png'))    
    assert table_data == expected_data, "Profit-Loss Table default content does not match the expected data"

def test_period_1_table_2(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    ##verify cost structure table default data
    table = driver.find_element(By.XPATH, "//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[3]/div[3]/section/div/div/table")

    # Extract data from the table
    table_data = []
    for row in table.find_elements(By.TAG_NAME, "tr"):
        row_data = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
        if row_data:
            table_data.append(row_data)

    # Define the expected data
    expected_data = [
        ["Revenue", "100%"],
        ["COGS", "(70)%"],
        ["Gross Margin", "30%"],
        ["Fixed Cost", "(2)%"],
        ["Advertising", "(9)%"],
        ["Sales Force Cost", "(4)%"],
        ["Quality Control Cost", "(9)%"],
        ["Admin Expense", "(1)%"],
        ["Operating Margin / EBITDA", "5%"]
    ]
    if table_data == expected_data:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_1.png'))
        print("Default Cost Structure table data matched" )
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_1.png'))    
    assert table_data == expected_data, " Cost Structure Table Default content does not match the expected data"



def test_period_1_slider_1_manipulation(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    slider = driver.find_element(By.ID, "bucket-1-basic-slider1")
    pixels_to_move = 100
    action_chains = ActionChains(driver)
    action_chains.click_and_hold(slider).move_by_offset(pixels_to_move, 0).release().perform()
    slider_value = slider.get_attribute("aria-valuenow")
    print(slider_value)
    changed_sliders_value_in_period_1.append(slider_value)

   
    ##Second  slider-  Manipulation
def test_period_1_slider_2_manipulation(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    slider = driver.find_element(By.ID, "bucket-1-basic-slider2")
    pixels_to_move = 150
    action_chains = ActionChains(driver)
    action_chains.click_and_hold(slider).move_by_offset(pixels_to_move, 0).release().perform()
    slider_value = slider.get_attribute("aria-valuenow")
    print(slider_value) 
    changed_sliders_value_in_period_1.append(slider_value)

    ##3rd slider-  Manipulation
def test_period_1_slider_3_manipulation(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    slider = driver.find_element(By.ID, "bucket-1-basic-slider3")
    pixels_to_move = -150
    action_chains = ActionChains(driver)
    action_chains.click_and_hold(slider).move_by_offset(pixels_to_move, 0).release().perform()
    slider_value = slider.get_attribute("aria-valuenow")
    print(slider_value)
    changed_sliders_value_in_period_1.append(slider_value)

    ##4th slider-  Manipulation
def test_period_1_slider_4_manipulation(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    slider = driver.find_element(By.ID, "bucket-1-basic-slider4")
    pixels_to_move = 200
    action_chains = ActionChains(driver)
    action_chains.click_and_hold(slider).move_by_offset(pixels_to_move, 0).release().perform()
    slider_value = slider.get_attribute("aria-valuenow")
    print(slider_value)
    changed_sliders_value_in_period_1.append(slider_value)

    ##click on submit button
def test_submit_period_1(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    submit_btn = driver.find_element(By.XPATH,"//div[@id='submit_user_input']")
    submit_btn.click()
    print("Submit Button clicked in period 1")

    time.sleep(2)
    ##click yes on popup
    yes_btn = driver.find_element(By.XPATH,"//button[normalize-space()='Yes']")
    yes_btn.click()
    print("Clicked yes button on popup meassage")

    time.sleep(2)
    ##click ok on 2nd popup
    ok_btn = driver.find_element(By.XPATH,"//button[normalize-space()='OK']")
    ok_btn.click()
    print("Clicked ok button on 2nd popup")
    time.sleep(3)


# ************ Period 2 ************** 
def test_period_2_market_share(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("************* Testing in Period 2 ************** ")
    #market share (Month 2)
    time.sleep(2)
    market_share = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/span")
    actual_market_share = float(market_share.text.strip('%'))
    expected_min_market_share = 0
    expected_max_market_share =100
    print(market_share.text)
    if expected_min_market_share <= actual_market_share <= expected_max_market_share:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_2.png'))
        print("Market share is within the expected range") 
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_2.png'))                              
    assert expected_min_market_share <= actual_market_share <= expected_max_market_share, f"Text verification failed in Period 2. Expected:0% to 100% Actual: '{market_share.text}'"

#     #Sliders
def test_period_2_sliders_default_value(driver):      
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    extracted_values = []
    expected_values = set(changed_sliders_value_in_period_1)
    sliders = driver.find_elements(By.CSS_SELECTOR, '[role="slider"]')
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[role="slider"]')))
    for slider in sliders:
        try:
            #slider = wait.until(EC.visibility_of(slider))
            aria_valuenow = slider.get_attribute('aria-valuenow')
            extracted_values.append(aria_valuenow)
        except Exception as e:
            print(f"Error while processing a slider: {e}")
    non_zero_values = [value for value in extracted_values if value != '0']
    non_zero_set = set(non_zero_values)
    if non_zero_set == expected_values:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_2.png'))
        print("Sliders values matched in period 2")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_2.png'))    
    assert non_zero_set == expected_values, f"Values do not match. Expected: {expected_values}, Actual: {non_zero_set}"
    

def test_period_2_projected_revenue(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    proj_rev = driver.find_element(By.XPATH,"//div[@class='revenue_value theme-font8']")
    actual_proj_rev = float(''.join(filter(str.isdigit, proj_rev.text)))
    expected_min_proj_rev = 0
    print(actual_proj_rev)
    if actual_proj_rev >= expected_min_proj_rev:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_2.png'))
        print("Projected revenue Testing Passed in Period 2¸")    
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_2.png'))                    
    assert actual_proj_rev >= expected_min_proj_rev, f"Projected revenue not matched  . Expected: '{expected_min_proj_rev}', Actual: '{actual_proj_rev}'"

    # click on Expand all in Period-2
def test_period_2_expand_all(driver):   
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    exp_btn = driver.find_element(By.XPATH,"//button[@id='expand_all_report']")
    exp_btn.click()
    print("Expand all clicked")
    time.sleep(5)

    #table 1 (Profit and loss statement)
def test_period_2_table_1(driver):      
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("* Tabel 1 (Profit and loss statement) *")
    #Month 1
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[3]/div[2]/section/div/div[2]/table/tr[2]/td[3]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_2.png'))
        print("revenue Testing Passed")     
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_2.png'))                                  
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #Month 2(E)
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[3]/div[2]/section/div/div[2]/table/tr[2]/td[2]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_2.png'))
        print("revenue Testing Passed")    
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_2.png'))                                   
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"



    #table2 
def test_period_2_table_2(driver):      
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("* Tabel 2 (Cost structure) *")
    #month 1
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[3]/div[3]/section/div/div/table/tr[2]/td[3]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 100
    print(actual_revenue)
    if actual_revenue == expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_2.png'))
        print("revenue Testing Passed")  
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_2.png'))                                     
    assert actual_revenue == expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"

    #month 2(E)
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[3]/div[3]/section/div/div/table/tr[2]/td[2]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 100
    print(actual_revenue)
    if actual_revenue == expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_2.png'))
        print("revenue Testing Passed")    
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_2.png'))                                   
    assert actual_revenue == expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"



    # table 3  - Profit and Loss statement table (company wise)
def test_period_2_table_3(driver):       
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("* Tabel 3 (Profit-loss company-wise) *")
    #ZyngBeanz
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[2]/section/div/div/table/tr[2]/td[2]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_2.png'))
        print("revenue Testing Passed")    
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_2.png'))                                   
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #Alpha Corp.
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[2]/section/div/div/table/tr[2]/td[3]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_2.png'))
        print("revenue Testing Passed")         
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_2.png'))                              
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"

    #Beta Group
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[2]/section/div/div/table/tr[2]/td[4]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_2.png'))
        print("revenue Testing Passed")   
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_2.png'))                                    
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #Gamma Inc.
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[2]/section/div/div/table/tr[2]/td[5]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_2.png'))
        print("revenue Testing Passed")  
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_2.png'))                                     
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #Delta Brothers
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[2]/section/div/div/table/tr[2]/td[6]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_2.png'))
        print("revenue Testing Passed")         
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_2.png'))                              
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"

    #Table 4 Market Share Report (Unit Wise)
def test_period_2_table_4(driver):          
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("*  Table 4 - Market Share Report (Unit Wise) * ")
    table = driver.find_element(By.XPATH, "//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[3]/section/div/div/table")
    table_data = []
    for row in table.find_elements(By.TAG_NAME, "tr"):
        row_data = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
        if row_data:
            table_data.append(row_data)

    market_share_values = table_data[0][1:]
    # Convert the percentage strings to floats and calculate the sum
    percentage_values = [float(value.strip('%')) for value in market_share_values]
    total_percentage = sum(percentage_values)
    tolerance = 1
    # Check if the total percentage equals 100%
    if abs(total_percentage - 100.0) <= tolerance:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_2.png'))
        print("Market Share values(Unit wise) add up to 100%")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_2.png'))    
    assert abs(total_percentage - 100.0) <= tolerance,f"Error : Market Share values(Unit wise) add up to {total_percentage}%"       

 
    expected_range_min = 0
    expected_range_max = 50

    # Extract and verify the values
    other_values = [float(value.strip('%')) for value in table_data[0][2:]] # Remaining columns for other companies (Leaving ZyngBeanz)

    # Check if the other company values are within the expected range
    for value in other_values:
        if expected_range_min <= value <= expected_range_max:
            assert True
            driver.save_screenshot(os.path.join(screenshot_true, 'Period_2.png'))
            print(f'Value {value} is within the expected range (0% to 50%).')
        else:
            driver.save_screenshot(os.path.join(screenshot_false, 'Period_2.png'))
            assert False,f'Error : Value {value} is outside the expected range. Expected: 0% to 50%, Actual: {value}'

    #Table 5 Market Share Report (Revenue Wise)
def test_period_2_table_5(driver):                    
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("* Table 5 - Market Share Report (Revenue Wise) *")
    table = driver.find_element(By.XPATH, "//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[4]/section/div/div/table")
    table_data = []
    for row in table.find_elements(By.TAG_NAME, "tr"):
        row_data = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
        if row_data:
            table_data.append(row_data)

    market_share_values = table_data[0][1:]
    # Convert the percentage strings to floats and calculate the sum
    percentage_values = [float(value.strip('%')) for value in market_share_values]
    total_percentage = sum(percentage_values)
    tolerance = 1
    # Check if the total percentage equals 100%
    if abs(total_percentage - 100.0) <= tolerance:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_2.png'))
        print("Market Share values(Revenue wise) add up to 100%")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_2.png'))    
    assert abs(total_percentage - 100.0) <= tolerance,f"Error : Market Share values(Revenue wise) add up to {total_percentage}%"

    expected_range_min = 0
    expected_range_max = 50

    # Extract and verify the values
    other_values = [float(value.strip('%')) for value in table_data[0][2:]] # Remaining columns for other companies (leaving zyngBeanz)

    # Check if the other company values are within the expected range
    for value in other_values:
        if expected_range_min <= value <= expected_range_max:
            assert True
            driver.save_screenshot(os.path.join(screenshot_true, 'Period_2.png'))
            print(f'Value {value} is within the expected range (0% to 50%).')
        else:
            driver.save_screenshot(os.path.join(screenshot_false, 'Period_2.png'))
            assert False,f'Error : Value {value} is outside the expected range. Expected: 0% to 50%, Actual: {value}'

    #Table 6 Market Report
def test_period_2_table_6(driver):            
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    table = driver.find_element(By.XPATH, "//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[5]/section/div/div/table")
    prices(table)


    ###Now manipulate the slider 
    
    #first slider-  Manipulate the slider value
def test_period_2_slider_1_manipulation(driver):          
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    slider = driver.find_element(By.ID, "bucket-1-basic-slider1")
    pixels_to_move = -100
    action_chains = ActionChains(driver)
    action_chains.click_and_hold(slider).move_by_offset(pixels_to_move, 0).release().perform()
    slider_value = slider.get_attribute("aria-valuenow")
    print(slider_value)
    changed_sliders_value_in_period_2.append(slider_value)

    #Second slider
def test_period_2_slider_2_manipulation(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    slider = driver.find_element(By.ID, "bucket-1-basic-slider2")
    pixels_to_move = -70
    action_chains = ActionChains(driver)
    action_chains.click_and_hold(slider).move_by_offset(pixels_to_move, 0).release().perform()
    slider_value = slider.get_attribute("aria-valuenow")
    print(slider_value)
    changed_sliders_value_in_period_2.append(slider_value)

    #3rd slider
def test_period_2_slider_3_manipulation(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    slider = driver.find_element(By.ID, "bucket-1-basic-slider3")
    pixels_to_move = 140
    action_chains = ActionChains(driver)
    action_chains.click_and_hold(slider).move_by_offset(pixels_to_move, 0).release().perform()
    slider_value = slider.get_attribute("aria-valuenow")
    print(slider_value)
    changed_sliders_value_in_period_2.append(slider_value)

    #4th slider
def test_period_2_slider_4_manipulation(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    slider = driver.find_element(By.ID, "bucket-1-basic-slider4")
    pixels_to_move = -110
    action_chains = ActionChains(driver)
    action_chains.click_and_hold(slider).move_by_offset(pixels_to_move, 0).release().perform()
    slider_value = slider.get_attribute("aria-valuenow")
    print(slider_value)
    changed_sliders_value_in_period_2.append(slider_value)
    time.sleep(1)

    ##click on submit button
def test_submit_period_2_(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    submit_btn = driver.find_element(By.XPATH,"//div[@id='submit_user_input']")
    submit_btn.click()
    print("Submit Button clicked")

    time.sleep(2)
    ##click yes on popup
    yes_btn = driver.find_element(By.XPATH,"//button[normalize-space()='Yes']")
    yes_btn.click()
    print("Clicked yes button on popup meassage")

    time.sleep(2)
    ##click ok on 2nd popup
    ok_btn = driver.find_element(By.XPATH,"//button[normalize-space()='OK']")
    ok_btn.click()
    print("Clicked ok button on 2nd popup")
    time.sleep(3)


# ************ Period 3 ************** 
def test_period_3_market_share(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("************* Testing in Period 3 ************** ")
    #market share (Month 3)
    time.sleep(2)
    market_share = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/span")
    actual_market_share = float(market_share.text.strip('%'))
    expected_min_market_share = 0
    expected_max_market_share =100
    print(market_share.text)
    if expected_min_market_share <= actual_market_share <= expected_max_market_share:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_3.png'))
        print("Market share is within the expected range")  
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_3.png'))                                      
    assert expected_min_market_share <= actual_market_share <= expected_max_market_share, f"Text verification failed in Period 3. Expected:0% to 100% Actual: '{market_share.text}'"

    #Sliders
def test_period_3_sliders_default_value(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    extracted_values = []
    expected_values = set(changed_sliders_value_in_period_2)
    sliders = driver.find_elements(By.CSS_SELECTOR, '[role="slider"]')
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[role="slider"]')))
    for slider in sliders:
        try:
            #slider = wait.until(EC.visibility_of(slider))
            aria_valuenow = slider.get_attribute('aria-valuenow')
            extracted_values.append(aria_valuenow)
        except Exception as e:
            print(f"Error while processing a slider: {e}")
    non_zero_values = [value for value in extracted_values if value != '0']
    non_zero_set = set(non_zero_values)
    if non_zero_set == expected_values:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_3.png'))
        print("Sliders values matched in period 3")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_3.png'))    
    assert non_zero_set == expected_values, f"Values do not match. Expected: {expected_values}, Actual: {non_zero_set}"

def test_period_3_projected_revenue(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    proj_rev = driver.find_element(By.XPATH,"//div[@class='revenue_value theme-font8']")
    actual_proj_rev = float(''.join(filter(str.isdigit, proj_rev.text)))
    expected_min_proj_rev = 0
    print(actual_proj_rev)
    if actual_proj_rev >= expected_min_proj_rev:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_3.png'))
        print("Projected revenue Testing Passed in Period 3¸") 
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_3.png'))                                       
    assert actual_proj_rev >= expected_min_proj_rev, f"Projected revenue not matched  . Expected: '{expected_min_proj_rev}', Actual: '{actual_proj_rev}'"

    # click on Expand all in Period-3
def test_period_3_expand_all(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    exp_btn = driver.find_element(By.XPATH,"//button[@id='expand_all_report']")
    exp_btn.click()
    print("Expand all clicked")
    time.sleep(5)

    #table 1 (Profit and loss statement)
def test_period_3_table_1(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("* Tabel 1 (Profit and loss statement) *")
    #Month 1
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[3]/div[2]/section/div/div[2]/table/tr[2]/td[4]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_3.png'))
        print("revenue Testing Passed")  
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_3.png'))                                     
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #Month 2
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[3]/div[2]/section/div/div[2]/table/tr[2]/td[3]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_3.png'))
        print("revenue Testing Passed")   
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_3.png'))                                    
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #Month 3(E)
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[3]/div[2]/section/div/div[2]/table/tr[2]/td[2]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_3.png'))
        print("revenue Testing Passed")        
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_3.png'))                               
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"



    #table2 
def test_period_3_table_2(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("* Tabel 2 (Cost structure) *")
    #month 1
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[3]/div[3]/section/div/div/table/tr[2]/td[4]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 100
    print(actual_revenue)
    if actual_revenue == expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_3.png'))
        print("revenue Testing Passed")   
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_3.png'))                                    
    assert actual_revenue == expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"

    #month 2
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[3]/div[3]/section/div/div/table/tr[2]/td[3]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 100
    print(actual_revenue)
    if actual_revenue == expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_3.png'))
        print("revenue Testing Passed")     
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_3.png'))                                  
    assert actual_revenue == expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #month 3(E)
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[3]/div[3]/section/div/div/table/tr[2]/td[2]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 100
    print(actual_revenue)
    if actual_revenue == expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_3.png'))
        print("revenue Testing Passed")     
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_3.png'))                                  
    assert actual_revenue == expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"




    # table 3  - Profit and Loss statement table (company wise)
def test_period_3_table_3(driver):     
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("* Tabel 3 (Profit-loss company-wise) *")
    #ZyngBeanz
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[2]/section/div/div/table/tr[2]/td[2]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_3.png'))
        print("revenue Testing Passed")       
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_3.png'))                                
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #Alpha Corp.
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[2]/section/div/div/table/tr[2]/td[3]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_3.png'))
        print("revenue Testing Passed")    
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_3.png'))                                   
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"

    #Beta Group
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[2]/section/div/div/table/tr[2]/td[4]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_3.png'))
        print("revenue Testing Passed")      
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_3.png'))                                 
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #Gamma Inc.
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[2]/section/div/div/table/tr[2]/td[5]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_3.png'))
        print("revenue Testing Passed")   
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_3.png'))                                    
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #Delta Brothers
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[2]/section/div/div/table/tr[2]/td[6]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_3.png'))
        print("revenue Testing Passed")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_3.png'))                                       
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"

    #Table 4 Market Share Report (Unit Wise)
def test_period_3_table_4(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("*  Table 4 - Market Share Report (Unit Wise) * ")
    table = driver.find_element(By.XPATH, "//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[3]/section/div/div/table")
    table_data = []
    for row in table.find_elements(By.TAG_NAME, "tr"):
        row_data = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
        if row_data:
            table_data.append(row_data)

    market_share_values = table_data[0][1:]
    # Convert the percentage strings to floats and calculate the sum
    percentage_values = [float(value.strip('%')) for value in market_share_values]
    total_percentage = sum(percentage_values)
    tolerance = 1
    # Check if the total percentage equals 100%
    if abs(total_percentage - 100.0) <= tolerance:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_3.png'))
        print("Market Share values(Unit wise) add up to 100%")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_3.png'))    
    assert abs(total_percentage - 100.0) <= tolerance,f"Error : Market Share values(Unit wise) add up to {total_percentage}%"       


    expected_range_min = 0
    expected_range_max = 50

    # Extract and verify the values
    other_values = [float(value.strip('%')) for value in table_data[0][2:]] # Remaining columns for other companies (Leaving ZyngBeanz)

    # Check if the other company values are within the expected range
    for value in other_values:
        if expected_range_min <= value <= expected_range_max:
            assert True
            driver.save_screenshot(os.path.join(screenshot_true, 'Period_3.png'))
            print(f'Value {value} is within the expected range (0% to 50%).')
        else:
            driver.save_screenshot(os.path.join(screenshot_false, 'Period_3.png'))
            assert expected_range_min <= value <= expected_range_max,f'Error : Value {value} is outside the expected range. Expected: 0% to 50%, Actual: {value}'

    #Table 5 Market Share Report (Revenue Wise)
def test_period_3_table_5(driver):   
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("* Table 5 - Market Share Report (Revenue Wise) *")
    table = driver.find_element(By.XPATH, "//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[4]/section/div/div/table")
    table_data = []
    for row in table.find_elements(By.TAG_NAME, "tr"):
        row_data = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
        if row_data:
            table_data.append(row_data)

    market_share_values = table_data[0][1:]
    # Convert the percentage strings to floats and calculate the sum
    percentage_values = [float(value.strip('%')) for value in market_share_values]
    total_percentage = sum(percentage_values)
    tolerance = 1
    # Check if the total percentage equals 100%
    if abs(total_percentage - 100.0) <= tolerance:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_3.png'))
        print("Market Share values(Revenue wise) add up to 100%")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_3.png'))    
    assert abs(total_percentage - 100.0) <= tolerance,f"Error : Market Share values(Revenue wise) add up to {total_percentage}%"      

    expected_range_min = 0
    expected_range_max = 50

    # Extract and verify the values
    other_values = [float(value.strip('%')) for value in table_data[0][2:]] # Remaining columns for other companies (leaving zyngBeanz)

    # Check if the other company values are within the expected range
    for value in other_values:
        if expected_range_min <= value <= expected_range_max:
            assert True
            driver.save_screenshot(os.path.join(screenshot_true, 'Period_3.png'))
            print(f'Value {value} is within the expected range (0% to 50%).')
        else:
            driver.save_screenshot(os.path.join(screenshot_false, 'Period_3.png'))
            assert expected_range_min <= value <= expected_range_max,f'Error : Value {value} is outside the expected range. Expected: 0% to 50%, Actual: {value}'

    #Table 6 Market Report
def test_period_3_table_6(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    table = driver.find_element(By.XPATH, "//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[5]/section/div/div/table")
    prices(table)


    ###Now manipulate the slider 
def test_period_3_slider_1_manipulation(driver):        
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    slider = driver.find_element(By.ID, "bucket-1-basic-slider1")
    pixels_to_move = 160
    action_chains = ActionChains(driver)
    action_chains.click_and_hold(slider).move_by_offset(pixels_to_move, 0).release().perform()
    slider_value = slider.get_attribute("aria-valuenow")
    print(slider_value)
    changed_sliders_value_in_period_3.append(slider_value)

    #Second slider
def test_period_3_slider_2_manipulation(driver):        
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    slider = driver.find_element(By.ID, "bucket-1-basic-slider2")
    pixels_to_move = 70
    action_chains = ActionChains(driver)
    action_chains.click_and_hold(slider).move_by_offset(pixels_to_move, 0).release().perform()
    slider_value = slider.get_attribute("aria-valuenow")
    print(slider_value)
    changed_sliders_value_in_period_3.append(slider_value)

    #3rd slider
def test_period_3_slider_3_manipulation(driver):     
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    slider = driver.find_element(By.ID, "bucket-1-basic-slider3")
    pixels_to_move = -140
    action_chains = ActionChains(driver)
    action_chains.click_and_hold(slider).move_by_offset(pixels_to_move, 0).release().perform()
    slider_value = slider.get_attribute("aria-valuenow")
    print(slider_value)
    changed_sliders_value_in_period_3.append(slider_value)

    #4th slider
def test_period_3_slider_4_manipulation(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    slider = driver.find_element(By.ID, "bucket-1-basic-slider4")
    pixels_to_move = 110
    action_chains = ActionChains(driver)
    action_chains.click_and_hold(slider).move_by_offset(pixels_to_move, 0).release().perform()
    slider_value = slider.get_attribute("aria-valuenow")
    print(slider_value)
    changed_sliders_value_in_period_3.append(slider_value)
    time.sleep(1)

    ##click on submit button
def test_submit_period_3(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    submit_btn = driver.find_element(By.XPATH,"//div[@id='submit_user_input']")
    submit_btn.click()
    print("Submit Button clicked")

    time.sleep(2)
    ##click yes on popup
    yes_btn = driver.find_element(By.XPATH,"//button[normalize-space()='Yes']")
    yes_btn.click()
    print("Clicked yes button on popup meassage")

    time.sleep(2)
    ##click ok on 2nd popup
    ok_btn = driver.find_element(By.XPATH,"//button[normalize-space()='OK']")
    ok_btn.click()
    print("Clicked ok button on 2nd popup")
    time.sleep(3)


# ************ Period 4 ************** 
def test_period_4_market_share(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("************* Testing in Period 4 ************** ")
    #market share (Month 4)
    time.sleep(3)
    market_share = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/span")
    actual_market_share = float(market_share.text.strip('%'))
    expected_min_market_share = 0
    expected_max_market_share =100
    print(market_share.text)
    if expected_min_market_share <= actual_market_share <= expected_max_market_share:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_4.png'))
        print("Market share is within the expected range")   
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_4.png'))                                     
    assert expected_min_market_share <= actual_market_share <= expected_max_market_share, f"Text verification failed in Period 4. Expected:0% to 100% Actual: '{market_share.text}'"

    #Sliders
def test_period_4_sliders_default_value(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    extracted_values = []
    expected_values = set(changed_sliders_value_in_period_3)
    sliders = driver.find_elements(By.CSS_SELECTOR, '[role="slider"]')
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[role="slider"]')))
    for slider in sliders:
        try:
            #slider = wait.until(EC.visibility_of(slider))
            aria_valuenow = slider.get_attribute('aria-valuenow')
            extracted_values.append(aria_valuenow)
        except Exception as e:
            print(f"Error while processing a slider: {e}")
    non_zero_values = [value for value in extracted_values if value != '0']
    non_zero_set = set(non_zero_values)
    if non_zero_set == expected_values:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_4.png'))
        print("Sliders values matched in period 4")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_4.png'))    
    assert non_zero_set == expected_values, f"Values do not match. Expected: {expected_values}, Actual: {non_zero_set}"

def test_period_4_projected_revenue(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    proj_rev = driver.find_element(By.XPATH,"//div[@class='revenue_value theme-font8']")
    actual_proj_rev = float(''.join(filter(str.isdigit, proj_rev.text)))
    expected_min_proj_rev = 0
    print(actual_proj_rev)
    if actual_proj_rev >= expected_min_proj_rev:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_4.png'))
        print("Projected revenue Testing Passed in Period 4")   
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_4.png'))                                     
    assert actual_proj_rev >= expected_min_proj_rev, f"Projected revenue not matched  . Expected: '{expected_min_proj_rev}', Actual: '{actual_proj_rev}'"

    # click on Expand all in Period-3
def test_period_4_expand_all(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    exp_btn = driver.find_element(By.XPATH,"//button[@id='expand_all_report']")
    exp_btn.click()
    print("Expand all clicked")
    time.sleep(2)

    #table 1 (Profit and loss statement)
def test_period_4_table_1(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("* Tabel 1 (Profit and loss statement) *")
    #Month 1
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[3]/div[2]/section/div/div[2]/table/tr[2]/td[5]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_4.png'))
        print("revenue Testing Passed")          
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_4.png'))                             
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #Month 2
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[3]/div[2]/section/div/div[2]/table/tr[2]/td[4]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_4.png'))
        print("revenue Testing Passed")    
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_4.png'))                                   
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #Month 3
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[3]/div[2]/section/div/div[2]/table/tr[2]/td[3]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_4.png'))
        print("revenue Testing Passed") 
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_4.png'))                                      
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #Month 4(E)
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[3]/div[2]/section/div/div[2]/table/tr[2]/td[2]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_4.png'))
        print("revenue Testing Passed")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_4.png'))                                       
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"



    #table2 
def test_period_4_table_2(driver):          
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("* Tabel 2 (Cost structure) *")
    #month 1
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[3]/div[3]/section/div/div/table/tr[2]/td[4]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 100
    print(actual_revenue)
    if actual_revenue == expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_4.png'))
        print("revenue Testing Passed")          
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_4.png'))                         
    assert actual_revenue == expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"

    #month 2
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[3]/div[3]/section/div/div/table/tr[2]/td[4]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 100
    print(actual_revenue)
    if actual_revenue == expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_4.png'))
        print("revenue Testing Passed")   
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_4.png'))                                    
    assert actual_revenue == expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #month 3
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[3]/div[3]/section/div/div/table/tr[2]/td[3]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 100
    print(actual_revenue)
    if actual_revenue == expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_4.png'))
        print("revenue Testing Passed")  
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_4.png'))                                     
    assert actual_revenue == expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #month 4(E)
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[3]/div[3]/section/div/div/table/tr[2]/td[2]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 100
    print(actual_revenue)
    if actual_revenue == expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_4.png'))
        print("revenue Testing Passed")     
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_4.png'))                                  
    assert actual_revenue == expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"



    # table 3  - Profit and Loss statement table (company wise)
def test_period_4_table_3(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("* Tabel 3 (Profit-loss company-wise) *")
    #ZyngBeanz
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[2]/section/div/div/table/tr[2]/td[2]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_4.png'))
        print("revenue Testing Passed")        
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_4.png'))                               
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #Alpha Corp.
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[2]/section/div/div/table/tr[2]/td[3]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_4.png'))
        print("revenue Testing Passed")   
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_4.png'))                                    
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"

    #Beta Group
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[2]/section/div/div/table/tr[2]/td[4]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_4.png'))
        print("revenue Testing Passed") 
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_4.png'))                                      
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #Gamma Inc.
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[2]/section/div/div/table/tr[2]/td[5]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_4.png'))
        print("revenue Testing Passed")  
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_4.png'))                                     
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #Delta Brothers
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[2]/section/div/div/table/tr[2]/td[6]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_4.png'))
        print("revenue Testing Passed")   
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_4.png'))                                    
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"

    #Table 4 Market Share Report (Unit Wise)
def test_period_4_table_4(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("*  Table 4 - Market Share Report (Unit Wise) * ")
    table = driver.find_element(By.XPATH, "//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[3]/section/div/div/table")
    table_data = []
    for row in table.find_elements(By.TAG_NAME, "tr"):
        row_data = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
        if row_data:
            table_data.append(row_data)

    market_share_values = table_data[0][1:]
    # Convert the percentage strings to floats and calculate the sum
    percentage_values = [float(value.strip('%')) for value in market_share_values]
    total_percentage = sum(percentage_values)
    tolerance = 1
    # Check if the total percentage equals 100%
    if abs(total_percentage - 100.0) <= tolerance:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_4.png'))
        print("Market Share values(Unit wise) add up to 100%")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_4.png'))    
    assert abs(total_percentage - 100.0) <= tolerance,f"Error : Market Share values(Unit wise) add up to {total_percentage}%"       


    expected_range_min = 0
    expected_range_max = 50

    # Extract and verify the values
    other_values = [float(value.strip('%')) for value in table_data[0][2:]] # Remaining columns for other companies (Leaving ZyngBeanz)

    # Check if the other company values are within the expected range
    for value in other_values:
        if expected_range_min <= value <= expected_range_max:
            assert True
            driver.save_screenshot(os.path.join(screenshot_true, 'Period_4.png'))
            print(f'Value {value} is within the expected range (0% to 50%).')
        else:
            driver.save_screenshot(os.path.join(screenshot_false, 'Period_4.png'))
            assert expected_range_min <= value <= expected_range_max,f'Error : Value {value} is outside the expected range. Expected: 0% to 50%, Actual: {value}'

    #Table 5 Market Share Report (Revenue Wise)
def test_period_4_table_5(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("* Table 5 - Market Share Report (Revenue Wise) *")
    table = driver.find_element(By.XPATH, "//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[4]/section/div/div/table")
    table_data = []
    for row in table.find_elements(By.TAG_NAME, "tr"):
        row_data = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
        if row_data:
            table_data.append(row_data)

    market_share_values = table_data[0][1:]
    # Convert the percentage strings to floats and calculate the sum
    percentage_values = [float(value.strip('%')) for value in market_share_values]
    total_percentage = sum(percentage_values)
    tolerance = 1
    # Check if the total percentage equals 100%
    if abs(total_percentage - 100.0) <= tolerance:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Period_4.png'))
        print("Market Share values(Revenue wise) add up to 100%")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Period_4.png'))    
    assert abs(total_percentage - 100.0) <= tolerance,f"Error : Market Share values(Revenue wise) add up to {total_percentage}%"        

    expected_range_min = 0
    expected_range_max = 50

    # Extract and verify the values
    other_values = [float(value.strip('%')) for value in table_data[0][2:]] # Remaining columns for other companies (leaving zyngBeanz)

    # Check if the other company values are within the expected range
    for value in other_values:
        if expected_range_min <= value <= expected_range_max:
            driver.save_screenshot(os.path.join(screenshot_true, 'Period_4.png'))
            print(f'Value {value} is within the expected range (0% to 50%).')
        else:
            driver.save_screenshot(os.path.join(screenshot_false, 'Period_4.png'))
            assert expected_range_min <= value <= expected_range_max,f'Error : Value {value} is outside the expected range. Expected: 0% to 50%, Actual: {value}'

    #Table 6 Market Report
def test_period_4_table_6(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    table = driver.find_element(By.XPATH, "//*[@id='sib_gametype_container']/div/div/div[3]/div[3]/div/div/div[4]/div[5]/section/div/div/table")
    prices(table)

    ###Now manipulate the slider 
    
    #first slider-  Manipulate the slider value
def test_period_4_slider_1_manipulation(driver):   
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    slider = driver.find_element(By.ID, "bucket-1-basic-slider1")
    pixels_to_move =130
    action_chains = ActionChains(driver)
    action_chains.click_and_hold(slider).move_by_offset(pixels_to_move, 0).release().perform()
    slider_value = slider.get_attribute("aria-valuenow")
    print(slider_value)
    changed_sliders_value_in_period_4.append(slider_value)

    #Second slider
def test_period_4_slider_2_manipulation(driver):        
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    slider = driver.find_element(By.ID, "bucket-1-basic-slider2")
    pixels_to_move = -90
    action_chains = ActionChains(driver)
    action_chains.click_and_hold(slider).move_by_offset(pixels_to_move, 0).release().perform()
    slider_value = slider.get_attribute("aria-valuenow")
    print(slider_value)
    changed_sliders_value_in_period_4.append(slider_value)

    #3rd slider
def test_period_4_slider_3_manipulation(driver):    
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    slider = driver.find_element(By.ID, "bucket-1-basic-slider3")
    pixels_to_move = -160
    action_chains = ActionChains(driver)
    action_chains.click_and_hold(slider).move_by_offset(pixels_to_move, 0).release().perform()
    slider_value = slider.get_attribute("aria-valuenow")
    print(slider_value)
    changed_sliders_value_in_period_4.append(slider_value)

    #4th slider
def test_period_4_slider_4_manipulation(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    slider = driver.find_element(By.ID, "bucket-1-basic-slider4")
    pixels_to_move = 90
    action_chains = ActionChains(driver)
    action_chains.click_and_hold(slider).move_by_offset(pixels_to_move, 0).release().perform()
    slider_value = slider.get_attribute("aria-valuenow")
    print(slider_value)
    changed_sliders_value_in_period_4.append(slider_value)
    time.sleep(1)

    ##click on submit button
def test_submit_period_4(driver):      
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    submit_btn = driver.find_element(By.XPATH,"//div[@id='submit_user_input']")
    submit_btn.click()
    print("Submit Button clicked")

    time.sleep(2)
    ##click yes on popup
    yes_btn = driver.find_element(By.XPATH,"//button[normalize-space()='Yes']")
    yes_btn.click()
    print("Clicked yes button on popup meassage")

    time.sleep(6)

# ************ Final Report after all periods ************** 
def test_final_reports_content_message(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("************* Testing After Submit all periods ************** ")
    wait = WebDriverWait(driver, 10)
    content = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='sib_gametype_container']/div/div/div[1]/div[1]/div[1]")))
    actual_content = content.text
    expected_content = "Did you hit your targets?"
    print(actual_content)
    if actual_content == expected_content:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Final_report.png'))
        print("Content is matched ")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Final_report.png'))    
    assert actual_content == expected_content, f"content verification failed. Expected: '{expected_content}', Actual: '{actual_content}'"

def test_final_reports_expand_all(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    exp_btn = driver.find_element(By.XPATH,"//button[@id='expand_all_report']")
    exp_btn.click()
    print("Expand all clicked")
    time.sleep(2)

    #table 1 (Profit and loss statement)
def test_final_reports_table_1(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("* Tabel 1 (Profit and loss statement) *")
    #Month 1
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[2]/div[2]/div[2]/section/div/div[2]/table/tr[2]/td[5]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Final_report.png'))
        print("month 1 : revenue Testing Passed")      
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Final_report.png'))                                 
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #Month 2
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[2]/div[2]/div[2]/section/div/div[2]/table/tr[2]/td[4]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Final_report.png'))
        print("month 2 : revenue Testing Passed")  
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Final_report.png'))                                     
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #Month 3
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[2]/div[2]/div[2]/section/div/div[2]/table/tr[2]/td[3]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Final_report.png'))
        print("month 3 : revenue Testing Passed")  
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Final_report.png'))                                     
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #Month 4
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[2]/div[2]/div[2]/section/div/div[2]/table/tr[2]/td[2]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Final_report.png'))
        print("month 4 : revenue Testing Passed")      
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Final_report.png'))                                 
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"



    #table2 
def test_final_reports_table_2(driver):       
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("* Tabel 2 (Cost structure) *")
    #month 1
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[2]/div[2]/div[3]/section/div/div/table/tr[2]/td[5]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 100
    print(actual_revenue)
    if actual_revenue == expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Final_report.png'))
        print("month 1 : revenue Testing Passed")      
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Final_report.png'))                                 
    assert actual_revenue == expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"

    #month 2
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[2]/div[2]/div[3]/section/div/div/table/tr[2]/td[4]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 100
    print(actual_revenue)
    if actual_revenue == expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Final_report.png'))
        print("month 2 : revenue Testing Passed")     
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Final_report.png'))                                  
    assert actual_revenue == expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #month 3
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[2]/div[2]/div[3]/section/div/div/table/tr[2]/td[3]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 100
    print(actual_revenue)
    if actual_revenue == expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Final_report.png'))
        print("month 3 : revenue Testing Passed")    
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Final_report.png'))                                   
    assert actual_revenue == expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #month 4
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[2]/div[2]/div[3]/section/div/div/table/tr[2]/td[2]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 100
    print(actual_revenue)
    if actual_revenue == expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Final_report.png'))
        print("month 4 : revenue Testing Passed")   
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Final_report.png'))                                    
    assert actual_revenue == expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"



    # table 3  - Profit and Loss statement table (company wise)
def test_final_reports_table_3(driver):       
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("* Tabel 3 (Profit-loss company-wise) *")
    #ZyngBeanz
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[2]/div[3]/div[2]/section/div/div/table/tr[2]/td[2]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Final_report.png'))
        print("revenue Testing Passed")      
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Final_report.png'))                                 
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #Alpha Corp.
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[2]/div[3]/div[2]/section/div/div/table/tr[2]/td[3]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Final_report.png'))
        print("revenue Testing Passed")   
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Final_report.png'))                                    
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"

    #Beta Group
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[2]/div[3]/div[2]/section/div/div/table/tr[2]/td[4]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Final_report.png'))
        print("revenue Testing Passed")   
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Final_report.png'))                                    
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #Gamma Inc.
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[2]/div[3]/div[2]/section/div/div/table/tr[2]/td[5]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Final_report.png'))
        print("revenue Testing Passed")   
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Final_report.png'))                                    
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"
    #Delta Brothers
    revenue = driver.find_element(By.XPATH,"//*[@id='sib_gametype_container']/div/div/div[2]/div[3]/div[2]/section/div/div/table/tr[2]/td[6]")
    actual_revenue = float(''.join(filter(str.isdigit, revenue.text)))
    expected_min_revenue = 0
    print(actual_revenue)
    if actual_revenue >= expected_min_revenue:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Final_report.png'))
        print("revenue Testing Passed")   
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Final_report.png'))                                    
    assert actual_revenue >= expected_min_revenue, f"Revenue not matched . Expected: '{expected_min_revenue}', Actual: '{actual_revenue}'"

    #Table 4 Market Share Report (Unit Wise)
def test_final_reports_table_4(driver):         
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("*  Table 4 - Market Share Report (Unit Wise) * ")
    final_market_share = driver.find_element(By.XPATH, "//*[@id='sib_gametype_container']/div/div/div[2]/div[3]/div[3]/section/div/div/table/tr[2]/td[2]").text.strip('%')
    final_market_share = float(final_market_share)
    final_market_share_value.append(final_market_share)

    table = driver.find_element(By.XPATH, "//*[@id='sib_gametype_container']/div/div/div[2]/div[3]/div[3]/section/div/div/table")
    table_data = []
    for row in table.find_elements(By.TAG_NAME, "tr"):
        row_data = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
        if row_data:
            table_data.append(row_data)

    market_share_values = table_data[0][1:]
    # Convert the percentage strings to floats and calculate the sum
    percentage_values = [float(value.strip('%')) for value in market_share_values]
    total_percentage = sum(percentage_values)
    tolerance = 1
    # Check if the total percentage equals 100%
    if abs(total_percentage - 100.0) <= tolerance:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Final_report.png'))
        print("Market Share values(Unit wise) add up to 100%")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Final_report.png'))    
    assert abs(total_percentage - 100.0) <= tolerance,f"Error : Market Share values(Unit wise) add up to {total_percentage}%"       


    expected_range_min = 0
    expected_range_max = 50

    # Extract and verify the values
    other_values = [float(value.strip('%')) for value in table_data[0][2:]] # Remaining columns for other companies (Leaving ZyngBeanz)

    # Check if the other company values are within the expected range
    for value in other_values:
        if expected_range_min <= value <= expected_range_max:
            assert True
            driver.save_screenshot(os.path.join(screenshot_true, 'Final_report.png'))
            print(f'Value {value} is within the expected range (0% to 50%).')
        else:
            driver.save_screenshot(os.path.join(screenshot_false, 'Final_report.png'))    
        assert expected_range_min <= value <= expected_range_max,f'Error : Value {value} is outside the expected range. Expected: 0% to 50%, Actual: {value}'

    #Table 5 Market Share Report (Revenue Wise)
def test_final_reports_table_5(driver):             
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("* Table 5 - Market Share Report (Revenue Wise) *")
    table = driver.find_element(By.XPATH, "//*[@id='sib_gametype_container']/div/div/div[2]/div[3]/div[4]/section/div/div/table")
    table_data = []
    for row in table.find_elements(By.TAG_NAME, "tr"):
        row_data = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
        if row_data:
            table_data.append(row_data)

    market_share_values = table_data[0][1:]
    # Convert the percentage strings to floats and calculate the sum
    percentage_values = [float(value.strip('%')) for value in market_share_values]
    total_percentage = sum(percentage_values)
    tolerance = 1
    # Check if the total percentage equals 100%
    if abs(total_percentage - 100.0) <= tolerance:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Final_report.png'))
        print("Market Share values(Revenue wise) add up to 100%")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Final_report.png'))    
    assert abs(total_percentage - 100.0) <= tolerance,f"Error : Market Share values(Revenue wise) add up to {total_percentage}%"    

    expected_range_min = 0
    expected_range_max = 50

    # Extract and verify the values
    other_values = [float(value.strip('%')) for value in table_data[0][2:]] # Remaining columns for other companies (leaving zyngBeanz)

    # Check if the other company values are within the expected range
    for value in other_values:
        if expected_range_min <= value <= expected_range_max:
            assert True
            driver.save_screenshot(os.path.join(screenshot_true, 'Final_report.png'))
            print(f'Value {value} is within the expected range (0% to 50%).')
        else:
            driver.save_screenshot(os.path.join(screenshot_false, 'Final_report.png'))    
        assert expected_range_min <= value <= expected_range_max,f'Error : Value {value} is outside the expected range. Expected: 0% to 50%, Actual: {value}'

    #Table 6 Market Report
def test_final_reports_table_6(driver):      
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    table = driver.find_element(By.XPATH, "//*[@id='sib_gametype_container']/div/div/div[2]/div[3]/div[5]/section/div/div/table")
    prices(table)


    #click next button
def test_final_reports_next_button(driver):   
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    next_btn = driver.find_element(By.XPATH,value="//*[@id='submit_user_input']")
    print("Next Button clicked")
    next_btn.click()
    time.sleep(5)
    
##### De-brief 

# ************ Target vs Actual ************** 
def test_target_vs_actual_heading(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("************* Target vs Actual ************** ")

    #verify header
    heading = driver.find_element(By.XPATH,value="//*[@id='sib-de-brief-page-1']/div/div[3]")
    actual_heading = heading.text
    expected_heading = "Target vs Actual"
    print(actual_heading)
    if actual_heading == expected_heading:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Target_vs_actual.png'))
        print("Heading is matched ")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Target_vs_actual.png')) 
    assert actual_heading == expected_heading, f"Heading verification failed. Expected: '{expected_heading}', Actual: '{actual_heading}'"

    ###Avg prices
def test_target_vs_actual_your_avg_price(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    your_avg_price_element = driver.find_element(By.XPATH,value="//*[@id='sib-de-brief-page-1']/div/div[5]/div[1]/div[3]/div[1]").text
    your_avg_price = your_avg_price_element.split('USD')[1].strip()
    your_avg_price = int(your_avg_price)
    int_values_zyngBeanz = [int(value) for value in price_zyngBeanz]
    total_price_zyngBeanz = sum(int_values_zyngBeanz)
    zyngbeanz_avg_price = round(total_price_zyngBeanz/4)
    print(your_avg_price)
    print(zyngbeanz_avg_price)
    if your_avg_price == zyngbeanz_avg_price:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Target_vs_actual.png'))
        print("Your Avg price matched ")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Target_vs_actual.png'))
    assert your_avg_price == zyngbeanz_avg_price,"Your avg prices are not matched"  


def test_target_vs_actual_others_avg_price(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    others_avg_price_element = driver.find_element(By.XPATH,value="//*[@id='sib-de-brief-page-1']/div/div[5]/div[1]/div[3]/div[2]").text
    others_avg_price = others_avg_price_element.split('USD')[1].strip()
    others_avg_price = int(others_avg_price)
    int_value_others = [int(value) for value in price_others]
    total_price_others = sum(int_value_others)
    other_comp_avg_price = round(total_price_others/16)
    print(others_avg_price)
    print(other_comp_avg_price)
    if others_avg_price == other_comp_avg_price:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Target_vs_actual.png'))
        print("Others Avg price matched ")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Target_vs_actual.png'))
    assert others_avg_price == other_comp_avg_price,"Others avg prices are not matched"  


    # #verify Kpi1 and kpi2 
def test_target_vs_actual_target_kpi_1(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    expected_target_kpi1 = 27 
    Target_kpi1 =driver.find_element(by=By.XPATH,value="//*[@id='sib-de-brief-page-1']/div/div[5]/div[2]/div[4]/div[1]").text.strip('%')
    Target_kpi1 = float(Target_kpi1)
    if Target_kpi1 == expected_target_kpi1:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Target_vs_actual.png'))
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Target_vs_actual.png'))    
    assert Target_kpi1 == expected_target_kpi1,"Target dismatched"
def test_target_vs_actual_achieved_kpi_1(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    achieved_kpi1 =driver.find_element(by=By.XPATH,value="//*[@id='sib-de-brief-page-1']/div/div[5]/div[2]/div[4]/div[2]").text.strip("%")
    achieved_kpi1 = float(achieved_kpi1)
    if achieved_kpi1 == final_market_share_value[0]:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Target_vs_actual.png'))
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Target_vs_actual.png'))    
    assert achieved_kpi1 == final_market_share_value[0],"Achieved dismatched"

def test_target_vs_actual_difference_in_kpi_1(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    Target_kpi1 =driver.find_element(by=By.XPATH,value="//*[@id='sib-de-brief-page-1']/div/div[5]/div[2]/div[4]/div[1]").text.strip('%')
    Target_kpi1 = float(Target_kpi1)
    achieved_kpi1 =driver.find_element(by=By.XPATH,value="//*[@id='sib-de-brief-page-1']/div/div[5]/div[2]/div[4]/div[2]").text.strip("%")
    achieved_kpi1 = float(achieved_kpi1)
    tolerance = 0.01
    difference_in_kpi1 =driver.find_element(by=By.XPATH,value="//div[contains(@class,'child2')]//div[@class='col-6 heading2 theme-font2']").text.split('%')[0]
    print(difference_in_kpi1)
    difference_in_kpi1 = float(difference_in_kpi1)
    absolute_difference1 = abs(Target_kpi1 - achieved_kpi1)
    print(difference_in_kpi1)
    print(abs(Target_kpi1-achieved_kpi1))
    if math.isclose(difference_in_kpi1, absolute_difference1, rel_tol=tolerance):
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Target_vs_actual.png'))
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Target_vs_actual.png'))    
    assert math.isclose(difference_in_kpi1, absolute_difference1, rel_tol=tolerance),"Difference dismatched"


def test_target_vs_actual_target_kpi_2(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    expected_target_kpi2 = 5
    Target_kpi2 =driver.find_element(by=By.XPATH,value="//*[@id='sib-de-brief-page-1']/div/div[5]/div[3]/div[4]/div[1]").text.strip('%')
    Target_kpi2 = float(Target_kpi2)

    if Target_kpi2 == expected_target_kpi2:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Target_vs_actual.png'))
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Target_vs_actual.png'))    
    assert Target_kpi2 == expected_target_kpi2,"Target dismatched"

def test_target_vs_actual_difference_in_kpi_2(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    achieved_kpi2 =driver.find_element(by=By.XPATH,value="//*[@id='sib-de-brief-page-1']/div/div[5]/div[3]/div[4]/div[2]").text.strip('%')
    achieved_kpi2 = float(achieved_kpi2)
    Target_kpi2 =driver.find_element(by=By.XPATH,value="//*[@id='sib-de-brief-page-1']/div/div[5]/div[3]/div[4]/div[1]").text.strip('%')
    Target_kpi2 = float(Target_kpi2)
    tolerance = 0.01

    difference_in_kpi2 =driver.find_element(by=By.XPATH,value="//*[@id='sib-de-brief-page-1']/div/div[5]/div[3]/div[2]/div[2]").text.split('%')[0]
    difference_in_kpi2 = float(difference_in_kpi2)
    absolute_difference2 = abs(Target_kpi2 - achieved_kpi2)

    if math.isclose(difference_in_kpi2, absolute_difference2, rel_tol=tolerance):
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'Target_vs_actual.png'))
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'Target_vs_actual.png'))    
    assert math.isclose(difference_in_kpi2, absolute_difference2, rel_tol=tolerance),"Difference dismatched"

def test_target_vs_actual_target_message(driver):   
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    expected_final_missed_message = "You missed the target. Use this as a learning & show better results next time."
    expected_final_exceeded_message = "Congratulations, you nailed it! Mission accomplished, great job!"
    real_final_message = driver.find_element(by=By.XPATH,value="//*[@id='sib-de-brief-page-1']/div/div[6]").text
    
    kpi_1 = driver.find_element(by=By.XPATH,value="//body/div[1]/div[2]/div[1]/div[5]/div[2]/div[2]/div[2]/span[1]")
    KPI_1_gettext = kpi_1.text
    print(f"KPI 1 : {KPI_1_gettext}")
    kpi_2 = driver.find_element(by=By.XPATH,value="//body/div[1]/div[2]/div[1]/div[5]/div[3]/div[2]/div[2]/span[1]")
    KPI_2_gettext = kpi_2.text
    print(f"KPI 2 : {KPI_2_gettext}")

    if KPI_1_gettext != KPI_2_gettext:
        if real_final_message == expected_final_missed_message:
            assert True
            driver.save_screenshot(os.path.join(screenshot_true, 'Target_vs_actual.png'))
        else:
            driver.save_screenshot(os.path.join(screenshot_false, 'Target_vs_actual.png'))    
        assert real_final_message == expected_final_missed_message, "message mismatched"

    elif KPI_1_gettext == KPI_2_gettext == 'Missed':
        if real_final_message == expected_final_missed_message:
            assert True
            driver.save_screenshot(os.path.join(screenshot_true, 'Target_vs_actual.png'))
        else:
            driver.save_screenshot(os.path.join(screenshot_false, 'Target_vs_actual.png'))    
        assert real_final_message == expected_final_missed_message, "message mismatched"

    elif KPI_1_gettext == KPI_2_gettext == 'Exceeded':
        if real_final_message == expected_final_exceeded_message:
            assert True
            driver.save_screenshot(os.path.join(screenshot_true, 'Target_vs_actual.png'))
        else:
            driver.save_screenshot(os.path.join(screenshot_false, 'Target_vs_actual.png'))    
        assert real_final_message == expected_final_exceeded_message, "message mismatched"

    else:
        assert False, "something wrong"


    #click on your performance 
def test_target_vs_actual_clicked_your_performance(driver):         
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    second_btn = driver.find_element(By.XPATH,value="//*[@id='sib-de-brief-page-1']/div/div[2]/div[2]/div[1]")
    print("clicked on your performance ")
    second_btn.click()
    time.sleep(3)   

# ************ Your Performance page ************** 
def test_your_performance(driver):
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("************* Your Performance ************** ")

    heading = driver.find_element(By.XPATH,value="//*[@id='sib-de-brief-page-2']/div/div[3]")
    actual_heading = heading.text
    expected_heading = "Your Performance"
    print(actual_heading)
    if actual_heading == expected_heading:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'your_performance.png'))
        print("Heading is matched ")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'your_performance.png'))    
    assert actual_heading == expected_heading, f"Heading verification failed. Expected: '{expected_heading}', Actual: '{actual_heading}'"
    
def test_your_performance_clicked_leaderboard(driver):   
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    #click on Leaderboard
    third_btn = driver.find_element(By.XPATH,value="//*[@id='sib-de-brief-page-2']/div/div[2]/div[3]/div[1]")
    print("clicked on your Leaderboard ")
    third_btn.click()
    time.sleep(3)  

# ************ Leaderboard Page ************** 
def test_leaderboard(driver):   
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.") 
    print("************* Leaderboard ************** ")
    print("* KPI 1 *")

    kpi_1 = driver.find_element(by=By.XPATH,value="//*[@id='sib-de-brief-page-3']/div/div[5]/div[1]/div[2]")
    KPI_1_gettext = kpi_1.text
    expected_kpi_1 = "Final Market Share (Units)"
    print(KPI_1_gettext)
    assert KPI_1_gettext == expected_kpi_1, f"Text verification failed. Expected: '{expected_kpi_1}', Actual: '{KPI_1_gettext}'"


    table_body = driver.find_element(By.XPATH, "//*[@id='sib-de-brief-page-3']/div/div[5]/div[1]/table/tbody")
    rows = table_body.find_elements(By.TAG_NAME, 'tr')
    # Iterate through the rows to find "You"
    name_found = False
    for row in rows:
        name = row.find_elements(By.TAG_NAME, 'td')[1].text
        if 'You' in name:
            assert 'You' in name
            driver.save_screenshot(os.path.join(screenshot_true, 'leaderboard.png'))
            rank = row.find_elements(By.TAG_NAME, 'td')[0].text
            score = row.find_elements(By.TAG_NAME, 'td')[2].text
            name_found = True
            print(f"Name: {name}, Rank: {rank}, Score: {score}")
    if name_found == False:
        driver.save_screenshot(os.path.join(screenshot_false, 'leaderboard.png'))     
    assert name_found,"Something Wrong , Your name is not in leaderboard"

    print("* KPI 2 *")

    kpi_2 = driver.find_element(by=By.XPATH,value="//*[@id='sib-de-brief-page-3']/div/div[5]/div[2]/div[2]")
    KPI_2_gettext = kpi_2.text
    expected_kpi_2 = "Cumulative Operating Margin %"
    print(KPI_2_gettext)
    assert KPI_2_gettext == expected_kpi_2, f"Text verification failed. Expected: '{expected_kpi_2}', Actual: '{KPI_2_gettext}'"


    table_body = driver.find_element(By.XPATH,"//*[@id='sib-de-brief-page-3']/div/div[5]/div[2]/table/tbody")
    rows = table_body.find_elements(By.TAG_NAME, 'tr')
    # Iterate through the rows to find "You"
    name_found = False
    for row in rows:
        name = row.find_elements(By.TAG_NAME, 'td')[1].text
        if 'You' in name:
            assert 'You' in name
            driver.save_screenshot(os.path.join(screenshot_true, 'leaderboard.png'))
            rank = row.find_elements(By.TAG_NAME, 'td')[0].text
            score = row.find_elements(By.TAG_NAME, 'td')[2].text
            name_found = True
            print(f"Name: {name}, Rank: {rank}, Score: {score}")
    if name_found == False:
        driver.save_screenshot(os.path.join(screenshot_false, 'leaderboard.png'))      
    assert name_found,"Something Wrong , Your name is not in leaderboard"


    #click on Market deep-dive
def test_leaderboard_clicked_market_deep_dive(driver: WebDriver):       
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    fourth_btn = driver.find_element(By.XPATH,value="//*[@id='sib-de-brief-page-3']/div/div[2]/div[4]/div[1]")
    print("clicked on Market Deep-Dive ")
    fourth_btn.click()
    time.sleep(3)   

# ************ Market deep-dive Page  ************** 
def test_market_deepdive(driver):    
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    print("************* Market Deep-dive ************** ")

    heading = driver.find_element(By.XPATH,value="//*[@id='sib-de-brief-page-4']/div/div[3]")
    actual_heading = heading.text
    expected_heading = "Market Deep-dive"
    print(actual_heading)
    if actual_heading == expected_heading:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'market_deepdive.png'))
        print("Heading is matched ")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'market_deepdive.png'))
    assert actual_heading == expected_heading, f"Heading verification failed. Expected: '{expected_heading}', Actual: '{actual_heading}'"

    text1 = driver.find_element(By.XPATH,value="//*[@id='sib-de-brief-page-4']/div/div[8]/div[1]")
    actual_text1= text1.text
    expected_text1 = "Final Market Share (Units)"
    print(actual_text1)
    if actual_text1 == expected_text1:
        driver.save_screenshot(os.path.join(screenshot_true, 'market_deepdive.png'))
        assert True
        print("Text is matched ")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'market_deepdive.png')) 
    assert actual_text1 == expected_text1, f"Text verification failed. Expected: '{expected_text1}', Actual: '{actual_text1}'"

    text2 = driver.find_element(By.XPATH,value="//*[@id='sib-de-brief-page-4']/div/div[9]/div[1]")
    actual_text2= text2.text
    expected_text2 = "Cumulative Operating Margin %"
    print(actual_text2)
    if actual_text2 == expected_text2:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'market_deepdive.png'))
        print("Text is matched ")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'market_deepdive.png'))   
    assert actual_text2 == expected_text2, f"Text verification failed. Expected: '{expected_text2}', Actual: '{actual_text2}'"

    #click on next
def test_market_deep_dive_clicked_next(driver):    
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    next_btn = driver.find_element(By.XPATH,value="//*[@id='sib-de-brief-page-4']/div/div[2]/button[2]")
    print("clicked on Next button ")
    next_btn.click()
    time.sleep(5)   


# ************ second last page - ending page ************** 
def test_ending_page(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")  
    heading = driver.find_element(By.XPATH,value="//*[@id='content_video_page1']/div/div[1]")
    actual_heading = heading.text
    expected_heading = "An introduction to pricing"
    print(actual_heading)
    if actual_heading == expected_heading:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'second_last_page.png'))
        print("Heading is matched ")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'second_last_page.png'))
    assert actual_heading == expected_heading, f"Heading verification failed. Expected: '{expected_heading}', Actual: '{actual_heading}'"


def test_ending_page_play_video(driver): 
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")   
    play_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='content_video_page1']/div/div[3]/div/i")))
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
    print("clicked on Video Play")
    play_btn.click()
    time.sleep(6)   
def test_ending_page_close_video(driver): 
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")   
    close_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='video_popup']/div/div/div/button")))
    print("clicked on Video Close")
    close_btn.click()
    time.sleep(3)   
def test_ending_page_video_transcript(driver):    
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    video_transcript = driver.find_element(By.XPATH,value="//*[@id='video_page1_transcript']").text
    expected_textlength = 1809 
    text_length = len(video_transcript)
    print(f"Length of text on the page: {text_length} characters")
    if text_length == expected_textlength:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'second_last_page.png'))
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'second_last_page.png'))    
    assert text_length == expected_textlength,"Video Transcript Length mismatched"   

def test_ending_page_next_button(driver): 
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")   
    next_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='content_video_page1']/div/div[5]/button[2]")))
    print("clicked on Next button ")
    next_btn.click()
    time.sleep(5)   


# ************ Last Page - congratualation message ************** 
def test_end_message(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")  
    print("************* End Message  ************** ")

    msg = driver.find_element(By.CLASS_NAME, 'sub_heading')
    actual_msg= msg.text
    expected_msg= "Congratulations on completing the simulation!\nHere are a few useful links for you."
    print(actual_msg)
    if actual_msg == expected_msg:
        assert True
        driver.save_screenshot(os.path.join(screenshot_true, 'last_page.png'))
        print("Text is matched ")
    else:
        driver.save_screenshot(os.path.join(screenshot_false, 'last_page.png'))    
    assert actual_msg == expected_msg, f"Text verification failed. Expected: '{expected_msg}', Actual: '{actual_msg}'"
def test_click_on_rewatch(driver):
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    play_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='videos_container']/div/div[2]/span")))
    print("clicked on Rewatch")
    play_btn.click()
    time.sleep(6)   

def test_click_on_close_rewatch(driver):
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    close_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='video_popup']/div/div/div/button")))
    print("clicked on Video Close")
    close_btn.click()
    time.sleep(3)   
            
def test_full_screen(driver):
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    full_screen = driver.find_element(By.XPATH,value="//*[@id='header_full_screen_icon']")
    print("clicked on Full Screen")
    full_screen.click()
    time.sleep(3)   

def test_logout(driver):  
    if popup_detected:
        pytest.skip("Invalid User Detected. Skipping this test.")
    logout_btn = driver.find_element(By.XPATH,value="//*[@id='data_for_content_pages']/span")
    print("Logged out")
    logout_btn.click()
    time.sleep(3)   
  


if __name__ == "__main__":
    pytest.main()