# Custom-eNews

Custom eNews is a script which will read through CBC pages that you specify and see if any articles match a list of words you have flagged. If any do, it will send you an email using the sendgrid api with the article details and a link to the article. It keeps track of the articles you've read so that the next time it is run, you will not get the same articles.

For my personal setup, I have put this project on a server and scheduled a cron job to run every few minutes, meaning that I am constatnly up-to-date with events that I'm interested in.


### Using this project for yourself
Using this script yourself is simple. Just follow these steps:

1. Download the project files.

2. If you don't have a Sendgrid account, [sign up for a free one](https://sendgrid.com/user/signup).

3. In the "Current implementation" folder, rename "example_settings.py" to "news_settings.py", and fill in the correct information in the file.

4. Create the file "articles.data" in the "Current implementation" folder.

5. Install the python package "requests" if you don't have it already (`pip install requests`).

6. Run xnews.py using Python 2 (`python xnews.py`).



### Running on a server
I set up this project for myself on a QNAP NAS device, and I have full documentation for everything you'll need to also do so in the file "Documentation.rtf". Essentially what you need to do is set up your python environment on your server and then schedule a cron job to run the script however often you want.
