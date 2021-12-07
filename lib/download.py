import wget


class Download:

    def __init__(self,url:str):
        self.file=wget.download(url)

    def file(self,url):
        return wget.download(url)



        
