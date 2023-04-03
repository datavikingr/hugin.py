# Daily News Digest
This is a Python script that pulls weather data from OpenWeatherMaps and RSS feeds from various news sources, aggregates them, and sends them to your Kindle's email address. You can use this script to get a daily digest of news articles from sources you care about to enjoy on your epaper screen, ostensibly over some nice coffee. 

## Getting Started
### Prerequisites
To run this script, you'll need [Python 3](https://www.python.org/) and the following packages:
- [feedparser](https://pypi.org/project/feedparser/)
- [smtplib](https://docs.python.org/3/library/smtplib.html)
- [requests](https://pypi.org/project/requests/)
- [bs4](https://pypi.org/project/beautifulsoup4/)
- [email](https://docs.python.org/3/library/email.examples.html)

### If you don't have Python installed:
```sudo apt install python3 python3-pip -y```

### Then you can install these packages using pip:
```pip install feedparser smtplib requests bs4 email```

## Installing Hugin.py
0. I'm assuming Debian-family of distros (`python3`). If you're on another distro/OS `python` should work. If you don't know, simply punch `which python && which python3` into your terminal. It'll tell you where it's installed (and thereby, which command to use; if both show up, defer to python3)
1. Clone this repository to your local machine.
2. Open `hugin.py` in the text editor of your choice
3. Update the configuration variables throughout the file (sorry, I grouped blobs by function: weather, news, email, in that order), denoted by [VARIABLE DESCRIPTION] formatting. Pay special attention to the kindle's email address.
4. Save the file.
5. Run the script using the command `python3 hugin.py`.
6. Hit sync on your kindle and wait for it. 

## If you'd like to see this on your kindle daily, do the following:
In a console/terminal, `crontab -e` and paste `0 6 * * * /usr/bin/python3 [PATH TO REPOSITORY]/hugin.py` on the bottom line. Save and exit. If that makes you a little nervous, you can check out [this introduction to crontab here](https://www.howtogeek.com/101288/how-to-schedule-tasks-on-linux-an-introduction-to-crontab-files/)!

## Don't see it, after multiple sends and syncs?
>Your Kindle email address will only accept emailed files from your manually authorized email addresses. You can find this list, called the “Approved Personal Document E-mail List” under [the “Preferences” tab for your devices](https://www.amazon.com/hz/mycd/myx#/home/settings/payment) when logged into your Amazon account. On mobile it’s located in the same place as the general Devices section we highlighted in the previous section.

[Source](https://www.howtogeek.com/867324/how-to-email-books-and-documents-to-your-kindle/)

## Pictures
<img src="https://user-images.githubusercontent.com/43792895/229621431-bae694d6-0013-4dd4-a958-53ec25807484.jpg" width=35% height=35%><img src="https://user-images.githubusercontent.com/43792895/229621454-7bda3160-5689-4b19-b2ca-18340ecabc3f.jpg" width=35% height=35%>

(sorry for the quality, but I really wanted to showcase it actually on the kindle)
