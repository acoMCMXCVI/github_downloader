import requests
from requests import get
from bs4 import BeautifulSoup

import time
import os
import shutil

s = requests.Session()
num_of_files = 0


class Folder:

    def __init__(self, rootFolder, name, href):
        self.root = rootFolder
        self.name = name
        self.href = href
        self.files = []
        self.folders = []


    def find(self):
        global num_of_files

        content = simple_get(self.href)


        items = content.findAll('a', class_='js-navigation-open')

        for item in items:
            if len(item['class']) == 1 and item.text != '..':
                if item['href'].find('tree') != -1:
                    href = 'https://github.com/' + item['href']
                    name = item.text

                    print(href.replace('https://github.com/', '').replace('sebastianstarke/AI4Animation/tree/master/AI4Animation/SIGGRAPH_Asia_2019/Unity', ''))

                    self.folders.append(Folder(self.href, name, href))

                else:
                    href = 'https://github.com/' + item['href']
                    name = item.text

                    self.files.append(File(self.href, name, href))

                    num_of_files = num_of_files + 1

        for folder in self.folders:
            folder.find()


    def tree(self, depth = 0):
        s = ('\t'*depth) + self.name + '/\n'
        for folder in self.folders:
            s += folder.tree(depth+1)

        for file in self.files:
            s += ('\t'*(depth+1)) + file.name + '\n'

        return s


    def download(self, path = ''):
        global s
        global num_of_files

        path = os.path.join(path,self.name)
        if os.path.isdir(path):
            shutil.rmtree(path)

        os.mkdir(path)

        for folder in self.folders:
            folder.download(path)


        for file in self.files:
            url = file.href.replace('github.com/', 'raw.github.com/').replace('blob/', '')

            r = s.get(url)

            with open(os.path.join(path, file.name), 'wb') as f:
                f.write(r.content)

            num_of_files = num_of_files - 1
            print(str(num_of_files) + '\tPreuzet fajl: ' + file.name)

class File:

    def __init__(self, rootFolder, name, href):
        self.root = rootFolder
        self.name = name
        self.href = href


def simple_get(url):
    global s

    resp = s.get(url, stream=True)
    content = BeautifulSoup(resp.text, 'html.parser')

    return content



if __name__ == '__main__':

    repo = Folder(None,'Unity','https://github.com/sebastianstarke/AI4Animation/tree/master/AI4Animation/SIGGRAPH_Asia_2019/Unity')
    repo.find()

    print('Number of files: ' + str(num_of_files))

    tree = repo.tree()
    print(tree)

    with open('tree.txt', 'w') as f:
        f.write(tree)

    repo.download()
