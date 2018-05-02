import requests, os, argparse, sys, json
from bs4 import BeautifulSoup
from gtts import gTTS
import moviepy.editor as mp
from urllib.request import Request, urlopen, urlretrieve, HTTPError
import shutil
from sys import argv
url = "http://www.vulture.com/2018/04/thanos-and-avengers-infinity-war-the-5-best-comics-to-read.html"

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')


content = soup.findAll("p")
text_list = []

for element in content:
	x = element.text
	text_list.append(x)

final_text = ''.join(map(str, text_list))

tts = gTTS(text='final_text', lang='en')
tts.save('test.mp3')


def get_soup(url,header):
	request = Request(url, headers=header)
	return BeautifulSoup(urlopen(request),'html.parser')

def main(args):
	parser = argparse.ArgumentParser(description='Scrape Google images')
	parser.add_argument('-s', '--search', default='bananas', type=str, help='search term')
	parser.add_argument('-n', '--num_images', default=3, type=int, help='num images to save')
	parser.add_argument('-d', '--directory', default='/Users/gene/Downloads/', type=str, help='save directory')

	
	args = parser.parse_args()
	query = args.search
	
	image_type="Action"
	query= query.split()
	query='+'.join(query)
	
	url="https://www.google.co.uk/search?q=superman&source=lnms&tbm=isch&sa=X&ved=0ahUKEwizicS88-DaAhXEasAKHU8gBvUQ_AUICigB&biw=943&bih=719"
	header={'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}
	soup = get_soup(url,header)
	
	ActualImages=[]
	links = []
	pic_list = []
	valid = 1
	valido = 1
	counter = 1
	#get image part of HTML
	for a in soup.find_all("div",{"class":"rg_meta"}, limit=10):
	    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]

	  
	    
		   # if len(john) > 1:
		    #	valid = 0
		    #Don't allow gifs to be downloaded
	    if 'gif' in link:
	    	valid = 0
	    	valido = 0


	    ActualImages.append((link,Type))
	    links.append(link)

	    
	    print (link)
	    #test if file will download
	    temp_file = str(counter) + '.png'
	    if valido == 1:


		    try:
		     urlretrieve(link, temp_file)
		     pic_list.append(mp.ImageClip(temp_file))

		    except HTTPError as e:
		    	
		    	if e.code == 403:
		    		print ('403 error, moving onto next image link')
		    		valid = 0
		    		#file = str(counter - 1), '.png'
	     

	    if valid == 1:
	    	file = str(counter) + '.png'
	    	urlretrieve(link, file)
	    	try:
	    		pic_list.append(mp.ImageClip(file))
	    	except:
	    		print ('some error ting init')

	    	counter += 1
	    valid = 1
	    valido = 1
	john = 5
	return pic_list, john


'''if __name__ == '__main__':
    
    try:
        main(argv)
    except KeyboardInterrupt:
        pass'''

pic_list = main(argv)
counter = 0
for x in pic_list:
	x.set_duration(3)
	

final_video = mp.concatenate_videoclips([pic_list], method="compose")
final_video.write_videofile('supes.mp4', codec='libx264', audio='test.mp3',audio_codec='mp3', fps=24)
sys.exit()

