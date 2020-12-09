from bs4 import BeautifulSoup
from pathlib import Path
import os
import sys
import getopt

def copyright():
    copyright = """
    The FreeBSD Copyright

    Copyright 1992-2020 The FreeBSD Project.
    
    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the 
    following conditions are met:
    
        1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
        1. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following 
            disclaimer in the documentation and/or other materials provided with the distribution.
    
    THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL 
    THE AUTHOR OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
    INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    
    The views and conclusions contained in the software and documentation are those of the authors and should not be interpreted as 
    representing official policies, either expressed or implied, of the FreeBSD Project.

    """





def getSearchInfo(url,service):
    fname = "{}_Activity.csv".format(service)
    header = "\"DATE\",\"Activity\",\"Action\",\"Url\""
    f = open(fname,"w+")
    f.write("{}\n".format(header))
    html = Path(url).read_text()
    soup = BeautifulSoup(html,'lxml')
    lines=0
    for d in soup.find_all("div",class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"):
        lines += 1
        try:
            url = d.find("a")['href']
            link = url
            date = str(d.prettify).split('>')[4].split('<')[0]
            action = str(d.prettify).split('>')[1].split('\xa0')[0]

            if 'Visited' in action and 'http' in url:
                link = url[url.find('=',0)+1:]
            try:
                f.write("\"{}\",{},{},{}\n".format(date,service,action,link))
            except OSError:
                print('Error: {}'.format(d.prettify))
                print(OSError)
                break
        except:
            link = "No Url"
            pass
    print("Processed {} lines: {} file created".format(lines,fname))
    f.close()

def help():
    help  = """
    MyActivity.py -h -p PathToGoogeTakeout directory eg ./GoogleTakeOut
    This will generate a single csv file for each Section , ie Books, Ads, Search etc
                Ads_Activity.csv
                Books_Activity.csv
                Chrome_Activity.csv
                Developers_Activity.csv
                Drive_Activity.csv
                Finance_Activity.csv
                Gmail_Activity.csv
                Google_Apps_Activity.csv
                Google_Play_Books_Activity.csv
                Google_Play_Store_Activity.csv
                Help_Activity.csv
                Image_Search_Activity.csv
                Maps_Activity.csv
                News_Activity.csv
                Search_Activity.csv
                Shopping_Activity.csv
                Takeout_Activity.csv
                Video_Search_Activity.csv
                YouTube_Activity.csv
    """
    print(help)

def main(argv):

    TakeOutPath = ''
    try:
        opts, args = getopt.getopt(argv,'hHp:P:',["Path="])
    except getopt.GetoptError:
        help()
        sys.exit(-1)
    for opt, arg in opts:
        if opt in ("-h","-H"):
            help()
            sys.exit()
        elif opt in ("-p","-P","-Path="):
            TakeOutPath = arg

    for i in sorted(Path(TakeOutPath).glob("**/My Activity.html")):

        dirname = os.path.basename(os.path.dirname(i)).replace(" ","_")
        getSearchInfo(i,dirname)


if __name__  == "__main__":
    main(sys.argv[1:])