# # Replace 'username' with the username of the profile you want to fetch posts from
# profile = instaloader.Profile.from_username(loader.context, '@thegutstuff')
#
# # Iterate over the posts and print their URLs
# for post in profile.get_posts():
#     print(post.url)

def make_sale(price: float, sale: int):
    sale = (price * sale) / 100
    return price - sale


print(make_sale(0, 0))