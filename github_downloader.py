from requests import get
from bs4 import BeautifulSoup


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
            if len(item['class']) == 1 and item.text != '..':
                if item['href'].find('tree') != -1:
                    href = 'https://github.com/' + item['href']
                    name = item.text

                    self.folders.append(Folder(self.href, name, href))

                else:
                    href = 'https://github.com/' + item['href']
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


def simple_get(url):
    resp = get(url, stream=True)
    content = BeautifulSoup(resp.text, 'html.parser')

    return content



if __name__ == '__main__':

    repo = Folder(None,'Unity','https://github.com/sebastianstarke/AI4Animation/tree/master/AI4Animation/SIGGRAPH_Asia_2019/Unity')
    repo.find()
    print(repo.tree())
