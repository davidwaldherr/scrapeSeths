import requests
from bs4 import BeautifulSoup

blogTitles = []
blogPosts = []
blog = []

# Create a nested for loop that iterates through the years 2015-2022 and then the months 1-12
for year in range(2015, 2022):
    for month in range(1, 13):
        # clear the blogTitles list
        blogTitles.clear()
        # clear the blogPosts list
        blogPosts.clear()

        # Create a URL for the specific month and year
        URL = f'https://seths.blog/{year}/{month}/'
        print (URL)
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib')

        #
        ## Get the title of the blog post
        #

        titles = soup.find_all('h2')
        # remove the first 6 titles from the list
        titles = titles[6:]
        # remove the last title from the list
        titles = titles[:-1]

        for title in titles:
            # remove all instances of “ from the title
            title = title.text.replace('“', '')
            title = title.replace('”', '')
            #prepend the title with the {"prompt":"
            title = '&&&' + title
            # append the title with \n\n###\n\n", "completion":"
            title = title + '###'
            # add the title to the list of titles
            blogTitles.append(title)

        #
        ## Get the content of the blog post
        #

        posts = soup.find_all('div', class_='has-content-area')

        for post in posts:
            # remove leading and trailing instances of \n from the post
            post = post.text.strip()
            # remove all empty lines from the post
            post = post.replace('\n\n', ' ')
            post = post.replace('\n', '')
            # remove all instances of " from the post
            post = post.replace('“', '')
            post = post.replace('”', '')
            # substitude non-alphanumeric characters with nothing
            post = post.replace('\u00a0', '')
            post += ' END'
            blogPosts.append(post)

        if len(blogTitles) == len(blogPosts):
            for i in range(len(blogTitles)):
                blog.append(blogTitles[i] + blogPosts[i])   

for i in range(len(blog)):
    #remove all instances of “ from the blog
    blog[i] = blog[i].replace('“', '')
    blog[i] = blog[i].replace('”', '')
    blog[i] = blog[i].replace('"', '')
    # replace all instances of &&& with {"prompt": "
    blog[i] = blog[i].replace('&&&', '{"prompt": "')
    # replace all instances of ### with  ###", "completion":"
    blog[i] = blog[i].replace('###', ' ###", "completion":"')
    # replace all instances of END with  END"}
    blog[i] = blog[i].replace('END', ' END"}')


# Write blog to a text file
with open('blog.txt', 'w') as f:
    for item in blog:
        f.write("%s\n" % item)