import numpy as np
from selenium import webdriver

class Root:

    browser = webdriver.Chrome()
    repo = None
    folders = []
    files = []
    stack_of_f = []

    def __init__(self, repository):
        self.repo = repository

    def find(self):
        # otvara link
        self.browser.get(self.repo)
        #self.browser.implicitly_wait(1)

        # pronalazi sve iteme u folderu
        items = self.browser.find_elements_by_class_name('js-navigation-open ')

        for item in items:

            if item.get_attribute('href') != '':

                if item.get_attribute('href').find('tree') != -1:

                    href = item.get_attribute('href')
                    name = item.text
                    # print(href)


                    folder = Folder(self.repo, name, href)
                    self.folders.append(folder)

                else:

                    href = item.get_attribute('href')
                    name = item.text
                    # print(href)


                    self.files.append(File(self.repo, name, href))

        self.print_childs()

        self.stack_of_f = self.folders.copy()

        while self.stack_of_f != []:
            folder = self.stack_of_f.pop()
            folder.find(self.browser)



    def print_childs(self):
        print('//////////Ja sam folder: ' + str(self.repo))
        print('****Folders:')
        for folder in self.folders:
            print(str(folder.name))

        print('****Files:')
        for file in self.files:
            print(str(file.name))

class Folder:

    root = None
    name = None
    folders = []
    files = []
    href = None

    stack_of_folders = []

    def __init__(self, rootFolder, name, href):
        self.root = rootFolder
        self.name = name
        self.href = href
        files = []


    def find(self, browser):
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

        self.print_childs()

        self.stack_of_folders = self.folders.copy()

        while self.stack_of_folders != []:
            folder = self.stack_of_folders.pop()
            folder.find(browser)


    def print_childs(self):
        print('*************** Ja sam folder: ' + str(self.name))
        print('****Folders:')
        for folder in self.folders:
            print(str(folder.name))

        print('****Files:')
        for file in self.files:
            print(str(file.name))


class File:

    root = None
    name = None
    href = None

    def __init__(self, rootFolder, name, href):
        self.root = rootFolder
        self.name = name
        self.href = href



if __name__ == '__main__':

    repo = Root('https://github.com/sebastianstarke/AI4Animation/tree/master/')
    repo.find()
