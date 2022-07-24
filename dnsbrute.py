import argparse
import sys
import os
try:
    import daemon
except:
    os.system("pip3 install python-daemon")
    os.system("echo 'run the program again!'")
    sys.exit(0)



class dnsbrute:
    def __init__(self, site=None, wordlist=None, silent=0):
        self.silent = silent
        self.site = site
        self.goFlag = False
        self.massDnsFlag = False
        self.shuffleDnsFlag = False
        self.subfinderFlag = False
        self.dnsGenFlag = False
        self.wordlist = wordlist
    def dnsShuffle(self):
        os.system('shuffledns -list dnsgen{} -massdns $(pwd)/massdnsApp -o shuffledns{} -silent '.format(self.site, self.site))
    def dnsGen(self):
        os.system('dnsgen subfinder{} -w {} >> dnsgen{}'.format(self.site, self.wordlist, self.site))
    def dnsx(self):
        os.system('for domain in $(cat shuffledns{} | dnsx -a -resp -silent) ; do echo $domain | cut -d" " -f2 >> ip{} ; echo $domain |cut -d" " -f1 >> subdomain{}; done '.format(self.site, self.site, self.site))
    def dynamicDns(self):
            os.system('while read -r site ;do subfinder -d $site -o subfinder{} -rL resolver -silent -timeout 5; done<"{}" '.format(self.site, self.site))
    def install(self):
        if self.goFlag:
            go = os.system("git clone https://github.com/caltechlibrary/install-golang.git; cd install-golang ; ./setup-golang.bash")
            if go != 0 :
                os.system("echo '[X] go installation failed , please install go manually .'")
                sys.exit(0)
        if self.massDnsFlag:
            massDnsLink = os.system("ls massdnsApp")
        if self.shuffleDnsFlag:
            shuffleDnsLink = os.system('go install -v github.com/projectdiscovery/shuffledns/cmd/shuffledns@latest')
        if self.subfinderFlag:
            subfinder = os.system('go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest')
        if self.dnsGenFlag:
            dnsgen = os.system('git clone https://github.com/ProjectAnte/dnsgen ; cd dnsgen ; pip3 install -r requirements.txt ; python3 setup.py install')
    def checkInstall(self):
        if not os.path.isfile('resolver'):
            with open("resolver", 'a+') as re:
                re.write("8.8.8.8\n8.8.4.4")
                re.close()
        checkGo = os.system("which go ")
        checkSubFinder = os.system("which subfinder ")
        checkShuffleDns = os.system("which shuffledns ")
        checkDnsGen = os.system("which dnsgen ")
        checkMassDns = os.system("which massdns ")
        if checkGo == 0:
            self.goFlag = False
        elif checkGo != 0:
            self.goFlag = True

        if checkSubFinder == 0:
            self.subfinderFlag = False
        elif checkSubFinder != 0:
            self.subfinderFlag = True

        if checkShuffleDns == 0:
            self.shuffleDnsFlag = False
        elif checkShuffleDns != 0:
            self.shuffleDnsFlag = True

        if checkDnsGen == 0:
            self.dnsGenFlag = False
        elif checkDnsGen != 0:
            self.dnsGenFlag = True

        if checkMassDns == 0:
            self.massDnsFlag = False
        elif checkMassDns != 0:
            self.massDnsFlag = True

    def engine(self):
        self.checkInstall()
        self.install()
        self.dynamicDns()
        self.dnsGen()
        self.dnsShuffle()
        self.dnsx()
    def run(self):
        self.daemon()
    def daemon(self):
        if self.silent == 0 :
            with daemon.DaemonContext():
                self.engine()
        else:
            self.engine()

#end of the dnsbrute class

#getting argument from terminal
parser = argparse.ArgumentParser()
parser.add_argument('-w', '--wordlist', help="wordlist for brute forcing the dns .", required=True)
parser.add_argument('-d', '--domain', help="file contain the domain list to brute force Note: copy the file in the working directory and named it as the same name as the site name .", required=True)
parser.add_argument('-s', '--silent', help="if silent 0 then program is going to be a daemon else (1) will be verbose in the output ", choices=['0', '1'], default='0')
arg = parser.parse_args()
site = arg.domain
wordlist = arg.wordlist
silent = int(arg.silent)
app = dnsbrute(wordlist=wordlist, site=site, silent=silent)
app.run()
















