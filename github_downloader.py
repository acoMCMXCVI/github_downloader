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

        self.print_childs()

        self.stack_of_folders = self.folders

        while self.stack_of_folders != []:
            folder = self.stack_of_folders.pop()
            folder.find()


    def print_childs(self):
        print('*************** Ja sam folder: ' + str(self.name))
        print('****Folders:')
        for folder in self.folders:
            print(folder.name)

        print('****Files:')
        for file in self.files:
            print(file.name)


class File:

    def __init__(self, rootFolder, name, href):
        self.root = rootFolder
        self.name = name
        self.href = href

if __name__ == '__main__':

    repo = Folder(None,'AI4Animation','https://github.com/sebastianstarke/AI4Animation/tree/master/')
    repo.find()
