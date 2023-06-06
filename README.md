# Webscapy: Selenium Configured for Webscraping

## Introduction

Webscapy is a Python package that extends the capabilities of the Selenium framework, originally designed for web testing, to perform web scraping tasks. It provides a convenient and easy-to-use interface for automating browser interactions, navigating through web pages, and extracting data from websites. By combining the power of Selenium with the flexibility of web scraping, Webscapy enables you to extract structured data from dynamic websites efficiently.

## Features

1. <b>Automated Browser Interaction:</b> Webscapy enables you to automate browser actions, such as clicking buttons, filling forms, scrolling, and navigating between web pages. With a user-friendly interface, you can easily simulate human-like interactions with the target website.

2. <b>Undetected Mode:</b> Webscapy includes built-in mechanisms to bypass anti-bot measures, including Cloudflare protection. It provides an undetected mode that reduces the chances of detection and allows for seamless scraping even from websites with strict security measures.

   |                                         Undetected Mode (Off)                                          |                                          Undetected Mode (On)                                          |
   | :----------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------: |
   | ![image](https://github.com/dusklight00/webscapy/assets/71203637/d8325500-3793-4f26-b7dd-15e5da7ee100) | ![image](https://github.com/dusklight00/webscapy/assets/71203637/7344470a-6924-4556-a72e-a27638e410bd) |

3. <b>Headless Browsers:</b> Webscapy supports headless browser operations, allowing you to scrape websites without displaying the browser window. This feature is useful for running scraping tasks in the background or on headless servers.

4. <b>Element Load Waiting:</b> The package offers flexible options for waiting until specific elements are loaded on the web page. You can wait for elements to appear, disappear, or become interactable before performing further actions. This ensures that your scraping script synchronizes with the dynamic behavior of websites.

5. <b>Execute JavaScript Code:</b> Webscapy allows you to execute custom JavaScript code within the browser. This feature enables you to interact with JavaScript-based functionalities on web pages, manipulate the DOM, or extract data that is not easily accessible through traditional scraping techniques.

6. <b>Connect with Remote Browsers:</b> SeleniumWebScraper provides a simplified method to connect with remote browsers using just one line of code. This feature allows you to distribute your scraping tasks to remote nodes or cloud-based Selenium Grid infrastructure. By specifying the remote URL, you can easily connect to a remote browser and leverage its capabilities for efficient scraping.

## Installation

You can install Webscapy using pip, the Python package manager. Open your command-line interface and execute the following command:

```python
pip install webscapy
```

## Getting Started

Following are the ways to create a driver

1. Simple Driver (headless)

```python
from webscapy import Webscapy

driver = Webscapy()

driver.get("https://google.com")
```

2. Turn off headless

```python
from webscapy import Webscapy

driver = Webscapy(headless=False)

driver.get("https://google.com")
```

3. Make the driver undetectable

```python
from webscapy import Webscapy

driver = Webscapy(headless=False, undetectable=True)

driver.get("https://google.com")
```

4. Connect to a remote browser

```python
from webscapy import Webscapy

REMOTE_URL = "..."
driver = Webscapy(remote_url=REMOTE_URL)

driver.get("https://google.com")
```

## Element Interaction

Following are the ways to interact with DOM Element

1. Wait for the element to load

```python
driver.load_wait(type, selector)
```

2. Load the element

```python
element = driver.load_element(type, selector)
```

3. Load all the possible instance of the selector (outputs an array)

```python
elements = driver.load_elements(type, selector)

# Exmaple
elements = driver.load_elements("tag-name", "p")

# Output:
# [elem1, elem2, elem3, ...]
```

3. Wait and load element

```python
element = driver.wait_load_element(type, selector)
```

4. Interact / Click the element

```python
element = driver.load_element(type, selector)
element.click()
```

## Different Type of Selectors

Take the following sample HTML code as example

```html
<html>
  <body>
    <h1>Welcome</h1>
    <p>Site content goes here.</p>
    <form id="loginForm">
      <input name="username" type="text" />
      <input name="password" type="password" />
      <input name="continue" type="submit" value="Login" />
      <input name="continue" type="button" value="Clear" />
    </form>
    <p class="content">Site content goes here.</p>
    <a href="continue.html">Continue</a>
    <a href="cancel.html">Cancel</a>
  </body>
</html>
```

Following are different selector types

|       Type        |         Example         |
| :---------------: | :---------------------: |
|        id         |       `loginForm`       |
|       name        | `username` / `password` |
|       xpath       |  `/html/body/form[1]`   |
|     link-text     |       `Continue`        |
| partial-link-text |         `Conti`         |
|     tag-name      |          `h1`           |
|    class-name     |        `content`        |
|   css-selector    |       `p.content`       |

Following is some usecase examples

```python
content = driver.wait_load_element("css-selector", 'p.content')
content = driver.wait_load_element("class-name", 'content')
content = driver.wait_load_element("tag-name", 'p')
```

## Execute Javascript Code

You can execute any javascript code on the site using the following method

```python
code = "..."
driver.execute_script(code)
```

## Network Activity Data

You can get network activity data after waiting for a while using commands like `time.sleep(...)`

```python
network_data = driver.get_network_data()

print(network_data)
```

## Cookie Handling

You can add cookies using the following method

1. Add a single cookie

```python
cookie = {
   "name": "cookie1",
   "value": "value1"
}
driver.add_cookie(cookie)
```

2. Get a single cookie

```python
driver.get_cookie("cookie1")
```

3. Delete a single cookie

```python
driver.delete_cookie("cookie1")
```

4. Import cookie from JSON

```
driver.load_cookie_json("cookie.json")
```

## Close the driver

Always close the driver after using it to save memory, or avoid memory leaks

```python
driver.close()
```
