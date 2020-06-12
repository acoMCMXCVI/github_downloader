import numpy as np
from selenium import webdriver

browser = webdriver.Chrome()


class Folder:

    #root = None
    #name = None
    #folders = []
    #files = []
    #href = None
    #stack_of_folders = []

    def __init__(self, rootFolder, name, href):
        self.root = rootFolder
        self.name = name
        self.href = href
        self.files = []
        self.folders = []


    def find(self):
        global brower
        browser.get(self.href)
        #print(self.files)
        #print('usao')
        #print('moj root je ' + str(self.root))
        #print('moj link je ' + str(self.href))
        # pronalazi sve iteme u folderu
        items = browser.find_elements_by_class_name('js-navigation-open ')

        #print([item.get_attribute('title') for item in items])
        for item in items:

            if item.get_attribute('href') != '' and item.text != '..':

                if item.get_attribute('href').find('tree') != -1:

                    href = item.get_attribute('href')
                    name = item.text

                    self.folders.append(Folder(self.href, name, href))

                    #folder.find(browser)

                else:
                    href = item.get_attribute('href')
                    name = item.text
                    # print(href)

                    self.files.append(File(self.href, name, href))

                    #print('Fajl dodat: ' + str(href))

        #self.print_childs()


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

    root = None
    name = None
    href = None

    def __init__(self, rootFolder, name, href):
        self.root = rootFolder
        self.name = name
        self.href = href



if __name__ == '__main__':

    repo = Folder(None,'AI4Animation','https://github.com/sebastianstarke/AI4Animation/tree/master/')
    repo.find()
    print(repo.tree())
