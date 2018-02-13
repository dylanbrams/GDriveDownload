import re
import requests

# This is a simple script that takes an e-mail text, pulls out all the http and https links,
# finds all the google drive links in said e-mail, and downloads them to a series of files
# named with sequential integers.  EG: 1.jpg
# download_file_from_google_drive, get_confirm_token, and save_response_content functions unabashedly stolen from
# https://stackoverflow.com/questions/38511444/python-download-files-from-google-drive-using-url

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

filenamein = "urls.txt"
data = ''
# Note: UTF8 was required because the origination language was Hebrew.
with open(filenamein, 'r', encoding='utf8') as myfile:
    data=myfile.read()
# This finds all http: and https: links in the email string provided.
pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

i = 0
for (match) in re.findall(pattern, data):
    # This matches any string starting with
    if match[:20] == 'https://drive.google':
        i = i + 1
        print(match)
        idstart = match.find('/d/')
        idend = match.find('/view?')
        id = match[idstart+3:idend]
        print(id)
        filenametosave = 'files/' + str(i) + '.jpg'
        download_file_from_google_drive(id, filenametosave)