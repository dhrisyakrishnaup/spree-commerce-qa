import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytest_html
from pytest_html import extras



@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_product_listing_page(driver):
    driver.get("https://demo.spreecommerce.org/us/en/products")

    products = driver.find_elements(By.CSS_SELECTOR, "a[href*='/us/en/products/']")
    assert len(products) > 0, "No products are displayed"
    time.sleep(2)

def test_select_product(driver):
    driver.get("https://demo.spreecommerce.org/us/en/products")

    # Click first product
    product = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a[href='/us/en/products/digital-air-fryer-6l']")
        )
    )
    product.click()
    # print("URL after click:", driver.current_url)
    WebDriverWait(driver, 10).until(
        EC.url_contains("/us/en/products/digital-air-fryer-6l")
    )
    assert driver.current_url.startswith(
        "https://demo.spreecommerce.org/us/en/products/digital-air-fryer-6l"
    )

    #
    # Verify product name
    product_name = driver.find_element(By.TAG_NAME, "h1")
    assert product_name.text != ""

    # Verify product price
    price = driver.find_element(By.CSS_SELECTOR, "span.text-3xl.font-bold")
    assert price.text != ""
    time.sleep(1)

def test_add_product_to_cart(driver):
    driver.get("https://demo.spreecommerce.org/us/en/products/digital-air-fryer-6l")


    # Click Add to cart
    add_to_cart = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Add to Cart')]")
        )
    )


    add_to_cart.click()
    time.sleep(2)

    # Wait for Checkout link to appear


    checkout = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[normalize-space()='Checkout']")
        )
    )

    print("Checkout button displayed")

    # Click Checkout
    checkout.click()

    # Verify checkout page
    WebDriverWait(driver, 20).until(
      EC.url_contains("/checkout/")
    )

    assert "/checkout/" in driver.current_url

    print("Checkout page loaded successfully")
    print("Current URL:", driver.current_url)

    time.sleep(2)

