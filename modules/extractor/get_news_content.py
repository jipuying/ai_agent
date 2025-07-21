from newspaper import Article

url = 'https://www.businessinsider.com/bought-rental-property-instead-of-primary-residence-making-money-2025-6'

# Initialize the Article object
article = Article(url)

# Download and parse
article.download()
article.parse()

# Print results
print("Title:", article.title)
print("\nFull Text:\n", article.text)