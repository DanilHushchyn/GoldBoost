# -*- coding: utf-8 -*-
# import instaloader
#
# # Initialize Instaloader
# L = instaloader.Instaloader()
#
# # Define the username of the account you want to fetch photos from
# username = 'liza_piavka'
#
# # Fetch the profile of the specified username
# profile = instaloader.Profile.from_username(L.context, username)
#
# # Fetch the most recent posts
# recent_posts = profile.get_posts()
#
# # Print the URLs of the recent photos
# for post in recent_posts:
#     print(post.url)
import httpx
httpx_client = httpx.Client()

url = 'http://134.209.230.39/api/registration/'
data = {'email': 'user10@example.com', 'password': 'sword123', 'notify_me': True}

response = httpx_client.post(url, data=data)
print(response.content)

if response.status_code == 200:
    print(response.json())
    # Process the data
    print(response)
else:
    print(f"Failed to fetch data: {response.status_code} - {response.reason_phrase}")
