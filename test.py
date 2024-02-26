import instaloader

# Initialize Instaloader
L = instaloader.Instaloader()

# Define the username of the account you want to fetch photos from
username = 'liza_piavka'

# Fetch the profile of the specified username
profile = instaloader.Profile.from_username(L.context, username)

# Fetch the most recent posts
recent_posts = profile.get_posts()

# Print the URLs of the recent photos
for post in recent_posts:
    print(post.url)
