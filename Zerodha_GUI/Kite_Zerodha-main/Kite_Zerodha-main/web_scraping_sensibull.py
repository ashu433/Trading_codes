import requests

Path_backtest_Report="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/Back_Test_Files_Report/"

def get_website_content(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the content of the webpage
            return response.json()
        else:
            print("Failed to fetch the URL:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None

# URL of the website
url = "https://oxide.sensibull.com/v1/compute/cache/live_derivative_prices/256265"

# Call the function to get the content of the website
website_content = get_website_content(url)

# Print the content (you can process it further as needed)
if website_content:
    print(website_content['data']['per_expiry_data']['2024-04-04']['options'][0])
    # with open(Path_backtest_Report+"website_content.txt", "w") as file:
    #     file.write(str(website_content))
