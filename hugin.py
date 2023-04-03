import feedparser, smtplib, os, requests, json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Define the RSS feeds to parse
# World News, so I'm not living under a rock in this backwater corner of the Earth that likes to pretend it's a proverbial island and the rest of the world doesn't matter.
world_news = {
    'BBC World': 'http://feeds.bbci.co.uk/news/world/rss.xml',
    'Al Jazeera': 'https://www.aljazeera.com/xml/rss/all.xml',
    'AP World News': 'https://www.pipes.digital/feed/1NjYgr9z'}
# National headlines, even from Fox, just to ensure I know what the hell those idiots are putting out into the world
national_news = {
    'NPR': 'https://feeds.npr.org/1001/rss.xml',
    'NY Times': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
    'CNN': 'http://rss.cnn.com/rss/cnn_us.rss',
    'Fox': 'https://moxie.foxnews.com/google-publisher/latest.xml'}
# News that matters because it's local
local_news = {
    'Baltimore Sun': 'https://www.baltimoresun.com/arcio/rss/',
    'Baltimore Brew': 'https://content.baltimorebrew.com/feed/',
    'Baltimore Fishbowl': 'https://baltimorefishbowl.com/feed/'}
# News I want because I like it
nerd_news = {
    'Ars Technica': 'https://feeds.arstechnica.com/arstechnica/index',
    'LifeHacker': 'https://lifehacker.com/rss',
    'Hackaday': 'https://hackaday.com/blog/feed/',
    'IGN': 'https://feeds.feedburner.com/ign/news'}
# Setting up the output and styles - optimized for viewing on a kindle
html = '<html><head><style>.article {border-radius: 16px; border: 2px solid black; margin: 16px auto; padding: 8px;} h1 {text-align: center;} .grid-container {display: grid; grid-template-columns: 1fr 1fr; width: 100%;} .ascii {text-align: center; font-size: 12px} #weather {font-size: 4px;}</style></head><body>'
# ASCII Art, because I'm 1337 like that
ascii_art = '''
 ____ ____ ____ _________ ____ ____ ____ ____ ____ ____ 
||T |||H |||E |||       |||D |||I |||G |||E |||S |||T ||
||__|||__|||__|||_______|||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|/__\|/__\|/__\|
'''

html += f'<div class="ascii" id="top"><pre>{ascii_art}</pre></div><br><br>'

###### WEATHER
html += f'<div class="article"><h1>### weather ###</h1>'
# Set up API call
url = 'https://api.openweathermap.org/data/2.5/onecall'
params = {
    'lat': '[YOUR LATITUDE COORDINATE]',
    'lon': '[YOUR LONGITUDE COORDINATE]',
    'exclude': 'current,minutely,hourly,alerts',
    'units': 'imperial',
    'appid': '[YOUR OPENWEATHERMAPS API KEY]'
}
# Make API call
response = requests.get(url, params=params)
# Parse response and extract data
data = response.json()
# extract first three days
for i in range(1, 4):
    # Get date for the forecast
    date = datetime.fromtimestamp(data['daily'][i]['dt']).strftime('%Y-%m-%d')

    # Get morning and evening temperature
    morning_temp = data['daily'][i]['temp']['morn']
    evening_temp = data['daily'][i]['temp']['eve']
    
    # Get morning and evening condition
    morning_condition = data['daily'][i]['weather'][0]['description']
    evening_condition = data['daily'][i]['weather'][0]['description']

    html += f'{date}: Morning: {morning_temp}°F, {morning_condition} | Evening: {evening_temp}°F, {evening_condition}<br><br>'
html += f'</div>'

# Section links for easy navigation
html += f'<div class="article"><h1>### sections ###</h1><div class="grid-container"><div><a href="#world_news"><h1>world_news</h1></a></div><div><a href="#national_news"><h1>national_news</h1></a></div><div><a href="#local_news"><h1>local_news</h1></a></div><div><a href="#nerd_news"><h1>nerd_news</h1></a></div></div></div><br><br>'
# Loop through the RSS feeds and print the title and summary of each article
for section_heading, whole_feed in [('world_news', world_news), ('national_news', national_news), ('local_news', local_news), ('nerd_news', nerd_news)]:
    # Section Header
    html += f'<h1 id={section_heading}>### {section_heading} ###</h1>'
    for feed_name, feed_url in whole_feed.items():
        article_count = 0
        # Source Header
        html += f'<h2># {feed_name}</h2>'
        # Begin cleaning and parsing the data
        feed = feedparser.parse(feed_url)
        for i, entry in enumerate(feed.entries):
            if article_count >= 15:
                break  # Break out of loop if we've printed 25 articles
            if 'summary' not in entry and 'description' not in entry and 'content' not in entry:
                continue  # Skip this entry if there's no summary or description; because dirty data!!
            if 'summary' in entry:
                summary = entry.summary
            elif 'description' in entry:
                summary = entry.description
            elif 'content' in entry:
                summary = entry.content
            else:
                continue
            #No really, this data is DIRTY; I even have to scrub the titles. This does return a warning, but it's not an error, and I need that scrub.
            title_text = BeautifulSoup(entry.title, features="html.parser").get_text()
            summary_text = BeautifulSoup(summary, features="html.parser").get_text()
            link_text = entry.link
            # Append the article to the list
            html += f'<div class="article"><h2>{title_text}</h2><p>{summary_text}</p><a href="{link_text}">Read More...</a></div>'
            article_count += 1
    # Give some space after each section
    if section_heading != 'nerd_news':
        html += f'<br><br>'
    #Easy navigation button
    html += f'<a href="#top"><h2>back_to_top...</h2></a>'
# Seal the HTML and write it to file
html += '</body></html>'
with open('the_digest.html', 'w') as f:
    f.write(html)

#Set up email parameters
email_from = '[YOU OUTBOUND EMAIL HERE]'
email_to = '[YOUR KINDLE EMAIL HERE]'
email_subject = 'The Digest'

#Send email
msg = MIMEMultipart()
msg['From'] = email_from
msg['To'] = email_to
msg['Subject'] = email_subject

#Attach HTML file to email
with open('the_digest.html', 'rb') as f:
    file_content = f.read()
attachment = MIMEApplication(file_content, _subtype='html')
attachment.add_header('content-disposition', 'attachment', filename='the_digest.html')
msg.attach(attachment)


#Send email using SMTP server
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login('[OUTBOUND EMAIL HERE]', '[APP SPECIFIC PASSWORD]')
    server.sendmail(email_from, email_to, msg.as_string())
