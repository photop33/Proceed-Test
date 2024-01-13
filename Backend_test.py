import requests

try:
    # Send a GET request to the server
    response = requests.get('http://localhost:5001')

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print("Request was successful!")
        print("Server Response:")
        print(response.text)  # Display the server's response content
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Server Response:")
        print(response.text)  # Display the server's response content for further inspection

except requests.exceptions.RequestException as e:
    print(f"Error during request: {e}")
