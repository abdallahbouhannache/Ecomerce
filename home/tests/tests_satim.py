# Django
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from time import sleep
# DRF
from rest_framework.test import APITestCase
# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
# Home
from home.payments import initilize_create_satim_bill, create_satim_bill
from home.models import Bill
from home.utils import randomize_order_id


class TestCardGame(StaticLiveServerTestCase):
    """ Testing checking created bill for SATIM """
    port = 8000

    def setUp(self):
        # Initilize user
        self.user = User.objects.create_user(username="test", password="test21asf654")
        # Create Bill in SATIM
        self.data = {
            'amount'     : 50000,
            'description': 'Test Fail Description'
        }
        # Create Bill in platform
        self.order_form = {
            'first_name'   : 'first_name',
            'last_name'    : 'last_name',
            'phone_number' : 'phone_number',
            'address'      : 'address',
            'wilaya'       : 'wilaya',
            'commune'      : 'commune',
            'zip_code'     : '43000',
        }
        # Run Selenium
        self.driver = webdriver.Chrome(executable_path=settings.SELENIUM_DRIVER)

    def initilize_test_bill(self):
        data = dict(self.data)
        data['key'] = randomize_order_id()
        # Initilize a Bill
        payment_order_status, payment_order = initilize_create_satim_bill(**data)
        # Check and Populate
        created_bill = create_satim_bill(
            user = self.user,
            key = data['key'],
            form_data = self.order_form,
            satim_response_data = payment_order,
            products_price = 250,
            shipping_price = 250,
            orders = [],
        )
        return payment_order, created_bill

    def update_card_info(self, card_number, cvv2, date):
        """ Update SATIM interface (Payment Page) card informations """
        # Get Fields
        iPAN  = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "iPAN")))
        iCVC  = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "iCVC")))
        month = Select(WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "month"))))
        year  = Select(WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "year"))))
        # Clear & Populate Fields
        iPAN.clear()
        iPAN.send_keys(card_number)
        iCVC.clear()
        iCVC.send_keys(cvv2)
        # Choose Date
        month_code, year_code = date.split('/')
        month.select_by_value(month_code)
        year.select_by_value(year_code)

    def start_proccessing(self, formUrl, card_data):
        """ Start Payment Proccess """
        # Example URL: https://test.satim.dz/payment/merchants/merchant1/payment_ar.html?mdOrder=hPqmEuKWkHrZCMAABGHH
        self.driver.get(formUrl)
        # Update DATA
        if card_data:
            self.update_card_info(card_data['card_number'], card_data['cvv2'], card_data['date'])
        # Click Pay
        pay_now = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "buttonPayment")))
        pay_now.click()
        # Set Password (optional)
        try:
            password  = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "j_idt39")))
            password.send_keys(card_data['password'])
        except:
            pass
        else:
            validate  = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "submitPasswordButton")))
            validate.click()

    def handle_fail_testing_cases(self, action_description_msg):
        # Tests Errors
        error_msg = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "error_msg")))
        error_code = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "error_code")))
        self.assertEqual(error_msg.text, 'Order is not confirmed due to order’s state')
        self.assertEqual(error_code.text, '3')
        # Test Todo
        action_description = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "action_description")))
        self.assertEqual(action_description.text, action_description_msg)

    def handle_success_testing_cases(self, action_description_msg):
        # Test Success
        action_description = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "action_description")))
        self.assertEqual(action_description.text, action_description_msg)

    def test_default_card(self):
        """ Payment done using default credit card """
        # Init
        satim_order, local_bill = self.initilize_test_bill()
        # Start
        self.start_proccessing(satim_order['formUrl'], card_data=None)
        # Test
        self.handle_fail_testing_cases('Your transaction was rejected, you have already entered 3 times password errone for this Your e-payment service is blocked, please contact your bank, Error code: 2003')

    def test_valid_card(self):
        """ Payment done using valid credit card """
        # Init
        satim_order, local_bill = self.initilize_test_bill()
        # Start
        card_data = {
            'card_number':'6280580610026519',
            'cvv2':'984',
            'date':'02/2023',
            'password':'123456',
        }
        self.start_proccessing(satim_order['formUrl'], card_data)
        # Test
        self.handle_success_testing_cases('Your payment was accepted')

    def test_temporary_blocked_card(self):
        """ Payment done using TEMPRORARY BLOCK card """
        # Init
        satim_order, local_bill = self.initilize_test_bill()
        # Start
        card_data = {
            'card_number':'6280580610026618',
            'cvv2':'457',
            'date':'02/2023',
            'password':'123456',
        }
        self.start_proccessing(satim_order['formUrl'], card_data)
        # Test
        self.handle_fail_testing_cases('Your transaction was rejected. please contact your bank. Error code : 37')

    def test_lost_card(self):
        """ Payment done using lost credit card """
        # Init
        satim_order, local_bill = self.initilize_test_bill()
        # Start
        card_data = {
            'card_number':'6280580610026717',
            'cvv2':'680',
            'date':'02/2023',
            'password':'123456',
        }
        self.start_proccessing(satim_order['formUrl'], card_data)
        # Test
        self.handle_fail_testing_cases('Your transaction was rejected, please contact your bank. Error code : 41')

    def test_stolen_card(self):
        """ Payment done using stolen credit card """
        # Init
        satim_order, local_bill = self.initilize_test_bill()
        # Start
        card_data = {
            'card_number':'6280580610026816',
            'cvv2':'517',
            'date':'02/2023',
            'password':'123456',
        }
        self.start_proccessing(satim_order['formUrl'], card_data)
        # Test
        self.handle_fail_testing_cases('Your transaction was rejected, please contact your bank. Error code : 43')

    def test_wrong_expiration_date_card(self):
        """ Payment done using wrong expiration date credit card """
        # Init
        satim_order, local_bill = self.initilize_test_bill()
        # Start
        card_data = {
            'card_number':'6280580610026915',
            'cvv2':'656',
            'date':'08/2023',
            'password':'123456',
        }
        self.start_proccessing(satim_order['formUrl'], card_data)
        # Test
        self.handle_fail_testing_cases('Your transaction was rejected, Please rectify the selected expiration date. Error code: AD')

    def test_not_exist_card(self):
        """ Payment done using not exist credit card """
        # Init
        satim_order, local_bill = self.initilize_test_bill()
        # Start
        card_data = {
            'card_number':'6280581110003927',
            'cvv2':'834',
            'date':'02/2023',
            'password':'123456',
        }
        self.start_proccessing(satim_order['formUrl'], card_data)
        # Test
        self.handle_fail_testing_cases('Your transaction was rejected, please contact your bank. Error code: 62')

    def test_max_allowed_card(self):
        """ Payment done using credit card reach max allowed """
        # Init
        satim_order, local_bill = self.initilize_test_bill()
        # Start
        card_data = {
            'card_number':'6280580610027111',
            'cvv2':'117',
            'date':'02/2023',
            'password':'123456',
        }
        self.start_proccessing(satim_order['formUrl'], card_data)
        # Test
        self.handle_fail_testing_cases('Your transaction was rejected, please enter another amount or contact your bank. Error code: 61')

    def test_sold_not_enough_card(self):
        """ Payment done using not enough sold in credit card """
        # Init
        satim_order, local_bill = self.initilize_test_bill()
        # Start
        card_data = {
            'card_number':'6280580610027210',
            'cvv2':'584',
            'date':'02/2023',
            'password':'123456',
        }
        self.start_proccessing(satim_order['formUrl'], card_data)
        # Test
        self.handle_fail_testing_cases('Your transaction was rejected, insufficient credit bank, please reload your bank account to carry out this operation. Error code : 51')

    def test_cvv2_error_card(self):
        """ Payment done using credit card with error in cvv2 """
        # Init
        satim_order, local_bill = self.initilize_test_bill()
        # Start
        card_data = {
            'card_number':'6280580610027319',
            'cvv2':'526',
            'date':'02/2023',
            'password':'123456',
        }
        self.start_proccessing(satim_order['formUrl'], card_data)
        # Test
        self.handle_fail_testing_cases('Your transaction was rejected, please rectify the entered CVV2. Error code : AB')

    def test_password_exceed_card(self):
        """ Payment done using credit card exceeded password tries """
        # Init
        satim_order, local_bill = self.initilize_test_bill()
        # Start
        card_data = {
            'card_number':'6280580610027418',
            'cvv2':'208',
            'date':'02/2023',
            'password':'666666',
        }
        self.start_proccessing(satim_order['formUrl'], card_data)
        # Test
        self.handle_fail_testing_cases('Your transaction was rejected, you have already entered 3 times password errone for this Your e-payment service is blocked, please contact your bank, Error code: 2003')

    def test_not_authorized_card(self):
        """ Payment done using not authorized credit card """
        # Init
        satim_order, local_bill = self.initilize_test_bill()
        # Start
        card_data = {
            'card_number':'6280580610027517',
            'cvv2':'156',
            'date':'02/2023',
            'password':'123456',
        }
        self.start_proccessing(satim_order['formUrl'], card_data)
        # Test
        self.handle_fail_testing_cases('Your transaction was rejected, you have already entered 3 times password errone for this Your e-payment service is blocked, please contact your bank, Error code: 2003')

    def test_non_active_card(self):
        """ Payment done using credit card not activated """
        # Init
        satim_order, local_bill = self.initilize_test_bill()
        # Start
        card_data = {
            'card_number':'6280581110004014',
            'cvv2':'614',
            'date':'02/2023',
            'password':'123456',
        }
        self.start_proccessing(satim_order['formUrl'], card_data)
        # Test
        self.handle_fail_testing_cases('Your transaction was rejected, please contact your bank. Error code : AE')

    def test_non_accepted_card(self):
        """ Payment done using credit card not accpeted """
        # Init
        satim_order, local_bill = self.initilize_test_bill()
        # Start
        card_data = {
            'card_number':'6280580610027715',
            'cvv2':'601',
            'date':'02/2023',
            'password':'123456',
        }
        self.start_proccessing(satim_order['formUrl'], card_data)
        # Test
        self.handle_fail_testing_cases('Your transaction was rejected, please contact your bank. Error code : 05')

    def test_terminal_reach_max_card(self):
        """ Payment done using credit card with terminal reach max """
        # Init
        satim_order, local_bill = self.initilize_test_bill()
        # Start
        card_data = {
            'card_number':'6280581110003818',
            'cvv2':'938',
            'date':'02/2023',
            'password':'123456',
        }
        self.start_proccessing(satim_order['formUrl'], card_data)
        # Test
        self.handle_fail_testing_cases('Your transaction was rejected, please contact your bank. Error code : 05')

    def test_expired_card(self):
        """ Payment done using expired credit card """
        # Init
        satim_order, local_bill = self.initilize_test_bill()
        # Start
        card_data = {
            'card_number':'6394131100000417',
            'cvv2':'214',
            'date':'06/2020',
            'password':'123456',
        }
        self.start_proccessing(satim_order['formUrl'], card_data)
        # Test
        self.handle_fail_testing_cases('Your transaction was rejected, Your card was expired, please contact your bank. Error code : 33')

    def tearDown(self):
        sleep(1)
        self.driver.quit()
