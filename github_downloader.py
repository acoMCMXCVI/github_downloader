import numpy as np
from selenium import webdriver

browser = webdriver.Chrome()


class Folder:


    def __init__(self, rootFolder, name, href):
        self.root = rootFolder
        self.name = name
        self.href = href
        self.files = []
        self.folders = []


    def find(self):
        global brower
        browser.get(self.href)


        items = browser.find_elements_by_class_name('js-navigation-open ')


        for item in items:

            if item.get_attribute('href') != '' and item.text != '..':

                if item.get_attribute('href').find('tree') != -1:

                    href = item.get_attribute('href')
                    name = item.text

                    self.folders.append(Folder(self.href, name, href))

                else:
                    href = item.get_attribute('href')
                    name = item.text

                    self.files.append(File(self.href, name, href))


        for folder in self.folders:
            folder.find()


    def tree(self, depth = 0):
        s = ('\t'*depth) + self.name + '/\n'
        for folder in self.folders:
            s += folder.tree(depth+1)

        for file in self.files:
            s += ('\t'*(depth+1)) + file.name + '\n'
        
        return s



class File:

    def __init__(self, rootFolder, name, href):
        self.root = rootFolder
        self.name = name
        self.href = href

if __name__ == '__main__':

    repo = Folder(None,'AI4Animation','https://github.com/sebastianstarke/AI4Animation/tree/master/')
    repo.find()
    print(repo.tree())
