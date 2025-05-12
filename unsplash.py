import requests
import os

def download_unsplash_image(keyword, save_path="image.jpg", ):
    access_key = "FdicL9bMbhvsdGQSsJKi1Np_073g5zjVspv6qKyCWeU"
    """
    Download an image from Unsplash based on a keyword.
    
    Args:
        keyword (str): The search term to find the image.
        save_path (str): Path to save the downloaded image (default: 'image.jpg').
        access_key (str): Unsplash API access key.
    
    Returns:
        bool: True if download is successful, False otherwise.
    """
    # Unsplash API search endpoint
    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": keyword,
        "per_page": 1,  # Get only the first (most relevant) result
        "client_id": access_key
    }
    
    try:
        # Make API request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Parse JSON response
        data = response.json()
        if not data["results"]:
            print(f"No images found for keyword: {keyword}")
            return False
        
        # Get the URL of the first image (regular size)
        image_url = data["results"][0]["urls"]["regular"]
        
        # Download the image
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        
        # Save the image to the specified path
        with open(save_path, "wb") as file:
            file.write(image_response.content)
        
        print(f"Image downloaded successfully to {save_path}")
        
        return image_response
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return False

# Example usage
# if __name__ == "__main__":
    # Replace 'YOUR_UNSPLASH_ACCESS_KEY' with your actual Unsplash API key
    # access_key = "FdicL9bMbhvsdGQSsJKi1Np_073g5zjVspv6qKyCWeU"
    
    # Download an image for the keyword "sunset"
    # download_unsplash_image("sunset", "sunset.jpg", access_key)

