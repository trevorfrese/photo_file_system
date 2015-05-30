import flickrapi
import webbrowser
import json
import urllib
 
flickr = flickrapi.FlickrAPI('f995167d658b6572aecd4d937b29a656', '5771bf75ffb63f73', format='json')
raw_json = flickr.photosets.getList(user_id='131877242@N02')


print('Step 1: authenticate')

# Only do this if we don't have a valid token already
if not flickr.token_valid(perms='read'):

    # Get a request token
    flickr.get_request_token(oauth_callback='oob')

    # Open a browser at the authentication URL. Do this however
    # you want, as long as the user visits that URL.
    authorize_url = flickr.auth_url(perms='delete')
    webbrowser.open_new_tab(authorize_url)
    print "opened up a new tab"
    # Get the verifier code from the user. Do this however you
    # want, as long as the user gives the application the code.
    verifier = unicode(raw_input('Verifier code: '), "utf-8")
    print "we got verifier", type(verifier)

    # Trade the request token for an access token
    flickr.get_access_token(verifier)

    print "we got access!!"


print('Step 2: use Flickr')
block_list = open("block_list.txt", "r")
count = 1
for line in block_list:
    file_id = line.split('\n')[0]
    resp = flickr.photos.getSizes(photo_id=file_id)
    jason =json.loads(resp)
    if jason['stat'] == 'fail':
        continue
    file_url = jason['sizes']['size'][7]['source']
    urllib.urlretrieve(file_url, filename="lena_" +str(count)+ ".jpg")
    count += 1

#resp = flickr.photos.getSizes(photo_id='18256576605')
#jason =json.loads(resp)
#file_url = jason['sizes']['size'][7]['source']
#urllib.urlretrieve(file_url, filename="lena_1.jpg")



#print resp


#print raw_json
 
 


 
#params['fileobj'] = FileWithCallback(params['lena.jpg'], callback)
#rsp = flickr.upload(filename = "lena.jpg")
 
 
#print raw_json