import requests
from requests import get
from bs4 import BeautifulSoup

import time
import os
import shutil

s = requests.Session()

# folders class
class Folder:

    root_name = 'tmp'           # root folder for downloading

    # class constructor
    def __init__(self, rootFolder, name, href):
        self.root = rootFolder
        self.name = name
        self.href = href
        self.files = []
        self.folders = []
        self.size = None


    # function find structure of repository
    def find(self):
        global s

        resp = s.get(self.href, stream=True)
        content = BeautifulSoup(resp.text, 'html.parser')

        items = content.findAll('a', class_='js-navigation-open')

        for item in items:
            if len(item['class']) <= 2 and item.text != '..':
                name = item.text
                if item['href'].find('tree') != -1:
                    href = 'https://github.com' + item['href']

                    self.folders.append(Folder(self.href, name, href))

                    print(name)
                else:
                    # create file link redy for downloading
                    href = 'https://raw.githubusercontent.com/' + item['href']
                    href = href.replace('blob/', '')

                    self.files.append(File(self.href, name, href))

        for f in self.folders:
            f.find()


    # function count # of files
    def get_number_of_files(self):
        n = len(self.files)
        for f in self.folders:
            n += f.get_number_of_files()
        return n


    # function make visualisation of repository structure
    def tree(self, depth = 0):

        # function return info does file last in the folder
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

    # function downloads files
    def download(self, type = 'full'):
        global s

        path = self.href[self.href.find('master') + 7:]
        path = os.path.join(self.root_name, path)

        # if there is path
        if os.path.isdir(path):
            if type == 'full':
                shutil.rmtree(path)
                os.makedirs(path)

                files_download = True

            elif type == 'skip':
                # check does all files is here
                if len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]) == len(self.files):
                    print('Folder exist - ' + path)
                    files_download = False
                else:
                    files_download = True

        else:
            os.makedirs(path)
            files_download = True


        for f in self.folders:
            f.download(type)

        if files_download:
            print('Downloading folder - ' + path)

            for f in self.files:
                f.download(path)



# folders class
class File:

    # class constructor
    def __init__(self, rootFolder, name, href):
        self.root = rootFolder
        self.name = name
        self.href = href
        self.size = None


    # function download file
    def download(self, path = ''):
        global s

        url = self.href
        r = s.get(url)

        with open(os.path.join(path, self.name), 'wb') as f:
            f.write(r.content)

        print('\tFile: ' + self.name + 'is downloaded.')



if __name__ == '__main__':

    #repo = Folder(None, '', 'https://github.com/acoMCMXCVI/Unit-for-Visualization-of-Expressions-UE4/tree/master/')
    repo = Folder(None, 'Unity', 'https://github.com/sebastianstarke/AI4Animation/tree/master/AI4Animation/SIGGRAPH_Asia_2019/Unity/Assets/MotionCapture')

    repo.find()
    print('Number of files: ', repo.get_number_of_files())
    tree = repo.tree()

    with open('tree.txt', 'w', encoding="utf-8") as f:
        f.write(tree)

    repo.download('skip')
