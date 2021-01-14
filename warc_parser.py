import warcat.model
import warcat.tool
import re
import base64
import os
from bs4 import BeautifulSoup

warc = warcat.model.WARC()


def delete_duplicate_lines_in_file(filename):
    inputfile = open(filename, "r")
    cachefile = open('outputfile.txt', 'w')
    newtxt = set(inputfile.readlines())
    cachefile.writelines(newtxt)
    cachefile.close()
    inputfile.close()

#if you want to remove all occurances of a string from a file
def delete_string_occurances_from_file(filename, string):
    inputfile = open(filename, 'rt')
    data = inputfile.read()
    data = data.replace(string, "")
    inputfile.close()
    outputfile = open(filename, 'w')
    outputfile.write(data)
    outputfile.close()


#this method finds all usernames from a warc and spits them out into a txtfile
#it also eliminates duplicates
def get_usernames_from_warc(warc_records):

    txtfile = open("profile_urls.txt", "a+")

    profile_regex = "/profile/\w+"

    x = True
    while x:
        record_tup = warc.read_record(warc_records)
        x = record_tup[1]

        try:
            if record_tup[0].content_block.payload.length > 30:
                record_content = bytes(record_tup[0].content_block.payload)
                profile_urls = re.findall(profile_regex, str(record_content))
                if len(profile_urls) > 0:
                    print("found profile")
                for url in profile_urls:
                    txtfile.write(url + '\n')
        except AttributeError:
            print("AttributeError: BinaryBlock record")
    warc_records.close()
    txtfile.close()

# Searches for posts by the user and extracts the linked author photo
def return_profile_photo_link(username, warc_records):

    matcher_string = '<span class="author--username">@'+username+'</span>'

    x = True
    while x:
        record_tup = warc.read_record(warc_records)
        x = record_tup[1]

        try:
            if record_tup[0].content_block.payload.length > 30:
                record_content = bytes(record_tup[0].content_block.payload)
                record_str = str(record_content)
                if record_str.find(matcher_string) != -1:
                    print("found post from user")
                    record_html = BeautifulSoup(record_str, 'html.parser')
                    return get_author_photo_from_post(find_post_from_author(username, record_html))

        except AttributeError:
            print("BinaryBlock record, ignored")

    warc_records.close()

# finds the associated reblock post and returns the html div
def find_reblock_post_from_author(usern, raw_record_html):
    post_list = raw_record_html.find_all('span', class_="reblock parent-and-post--wrapper")

    for post in post_list:
        print(post)
        author_username = post.find('span', class_="author--username").contents[0].replace("@", "")
        print(author_username)
        if author_username == usern:
            print("found author username")

            return post

# extracts the author photo from reblock post html
def get_author_photo_from_post(post):
    print("finding photo link")
    return post.find('img', alt="Post Author Profile Pic")['src']

#creates media output dirs
def verify_output_dirs():
    if not os.path.isdir('img'):
        os.mkdir('img')
    if not os.path.isdir('vid'):
        os.mkdir('vid')

# pass the profile photos URI (url/link) to this method
def extract_file_at_link(link):
    f = open(warcpath, 'rb')

    def get_extension(line):
        fextension = 'unknown.bin'
        if b'jpeg' or b'jpg' in line:
            fextension = 'jpg'
        elif b'png' in line:
            fextension = 'png'
        elif b'gif' in line:
            fextension = 'gif'
        return fextension

    while True:
        line = f.readline()

        if not line: break
        if b'WARC-Target-URI' in line:
            base64uri = base64.encodebytes(line.split(b' ')[1].strip()).decode().replace('\n', '')
            target_uri = line.split(b' ')[1].strip().decode('UTF-8')
            # this is where it matches the given URI to each found URI
            if link.strip() == target_uri:
                extension = get_extension(line)
                filename = 'img/%s.%s' % (base64uri, extension)

                size = 0
                is_image = False
                while True:
                    nextline = f.readline()
                    if b'Content-Length:' in nextline:
                        size = int(nextline.split(b' ')[1].replace(b'\r\n', b''))
                    if b'Content-Type: image' in nextline:
                        is_image = True
                    if nextline == b'\r\n':
                        if not is_image: continue
                        contents = f.read(size)
                        img = open(filename, 'wb')
                        img.write(contents)
                        img.close()
                        print(filename)
                        break




warcpath = "parler_20210110180312_ab60bbf5.megawarc.warc"
records = warc.open(warcpath)
user = ""

verify_output_dirs()
photo_uri = return_profile_photo_link(user, records)
extract_file_at_link(photo_uri)
