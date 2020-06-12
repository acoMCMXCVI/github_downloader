import requests
from requests import get
from bs4 import BeautifulSoup

import time
import os
import shutil

s = requests.Session()


class Folder:

    def __init__(self, rootFolder, name, href):
        self.root = rootFolder
        self.name = name
        self.href = href
        self.files = []
        self.folders = []


    def find(self):

        content = simple_get(self.href)


        items = content.findAll('a', class_='js-navigation-open')

        for item in items:
            if len(item['class']) <= 2 and item.text != '..':
                if item['href'].find('tree') != -1:
                    href = 'https://github.com/' + item['href']
                    name = item.text

                    self.folders.append(Folder(self.href, name, href))

                else:
                    href = 'https://github.com/' + item['href']
                    name = item.text

                    if name == 'scripting':
                        continue
                    self.files.append(File(self.href, name, href))


        for folder in self.folders:
            folder.find()


    def tree(self, depth = 0):
        def enumerate_last(xs):
            last_i = len(xs)-1
            for i, x in enumerate(xs):
                yield (i == last_i, x)
        
        b = self.name + '/\n'
        
        for last, f in enumerate_last(self.folders):
            if last and len(self.files) == 0:
                b1 = '└── '
                b2 = '    '
            else:
                b1 = '├── '
                b2 = '│   '
                
            sub_b = f.tree(depth+1).strip().split('\n')
            b += b1 + sub_b[0] + '\n'
            for j, sb in enumerate(sub_b[1:]):
                b += b2 + sb + '\n'
                
        for last, f in enumerate_last(self.files):
            if last:
                b += '└── ' + f.name + '\n'
            else:
                b += '├── ' + f.name + '\n'
        
        return b


    def download(self, path = ''):
        global s

        path = os.path.join(path, self.name)
        if os.path.isdir(path):
            shutil.rmtree(path)

        os.mkdir(path)

        for f in self.folders:
            f.download(path)

        for f in self.files:
            f.download(path)

class File:

    def __init__(self, rootFolder, name, href):
        self.root = rootFolder
        self.name = name
        self.href = href

    def download(self, path = ''):
        global s

        url = self.href.replace('github.com/', 'raw.github.com/').replace('blob/', '')

        r = s.get(url)

        with open(os.path.join(path, self.name), 'wb') as f:
            f.write(r.content)

        print('Preuzet fajl: ' + self.name)

def simple_get(url):
    global s

    resp = s.get(url, stream=True)
    content = BeautifulSoup(resp.text, 'html.parser')

    return content



if __name__ == '__main__':

    repo = Folder(None,'DAPU','https://github.com/acoMCMXCVI/Data-Analysis-and-Processing-Unit')
    repo.find()

    tree = repo.tree()
    print(tree)

    with open('tree.txt', 'w') as f:
        f.write(tree)

    repo.download()
