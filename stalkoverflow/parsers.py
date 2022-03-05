import sys
import requests
from bs4 import BeautifulSoup as bs4 
from fake_useragent import UserAgent
from  stalkoverflow.color import bcolors
import re
from urllib.parse import urlencode, urlparse
from urllib.parse import urljoin
import random
#from search_engine_parser.core.engines.google import Search as GoogleSearch 

export_code =[]

USER_AGENTS = [
    "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Firefox/59",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
]

def gen_user_agent() :
    user_agent = random.choice(USER_AGENTS)
    try:
        user_agent = UserAgent().random
    except Exception:
       pass
    return user_agent

def StylizeCode(Text,verified_identifier=None,scr_width=None,index=None):
    """Identifies and stylizes code in a question or answer."""
    global export_code
    holder = []
    # TODO: Handle blockquotes and markdown
    if verified_identifier is not None and verified_identifier not in Text:
        try:
            width = (scr_width-6)//2
            #format = "="*width
            #text = "\n"+format +'ANSWER'+format+"\n"
            text = "\n(^__^) ANSWER (^__^)\n"
            Text.insert(0,text)
        except:
            Text.insert(0,"(^__^) ANSWER (^__^)\n")
    StylizedText = []
    CodeBlocks = [block.get_text() for block in Text.find_all("code")]
    BlockQuotes = [block.get_text() for block in Text.find_all("blockquote")]
    newline = False
    for child in Text.recursiveChildGenerator():
        name = getattr(child, "name", None)
        if name is None: # Leaf (terminal) node
            if child in CodeBlocks:
                if newline: # Code block
                    #if code_blocks.index(child) == len(code_blocks) - 1: # Last code block
                        #child = child[:-1]
                    if verified_identifier is not None and verified_identifier in Text :
                        
                        holder.append(u"\n%s" % str(child))  
                    elif verified_identifier is not None and verified_identifier not in Text and index!=0:
                        holder.append(u"\n%s" % str(child))   
                    StylizedText.append(("code", u"\n%s" % str(child)))
                    newline = False
                else: # In-line code
                    if verified_identifier is not None and verified_identifier in Text:
                        holder.append(u"\n%s" % str(child))  
                    elif verified_identifier is not None and verified_identifier not in Text and index!=0:
                        holder.append(u"\n%s" % str(child))   
                    StylizedText.append(("code", u"%s" % str(child)))
            else: # Plaintext
                newline = child.endswith('\n')   
                StylizedText.append(u"%s" % str(child))

    if type(StylizedText[-2]) == tuple:
        # Remove newline from questions/answers that end with a code block
        if StylizedText[-2][1].endswith('\n'):
            if verified_identifier is not None and verified_identifier in Text:
                holder.append(StylizedText[-2][1][:-1])  
            elif verified_identifier is not None and verified_identifier not in Text and index!=0:
                 holder.append(StylizedText[-2][1][:-1])
            StylizedText[-2] = ("code", StylizedText[-2][1][:-1])
    if verified_identifier is not None and verified_identifier in Text:
        holder.insert(0,'#**Verified Answer**\n')              
    export_code.append("".join(holder)) if holder!=[] and index!=0 else holder       
             
    return StylizedText

# def GSearch(Error):
#     """Fetch Results From Google Using search_engine_parser"""
#     try:
#       print(bcolors.green+"Fetching Results...Please wait..."+bcolors.end)
#       gs = GoogleSearch()
#       SearchArgs=(Error,2)
#       gs.clear_cache()
#       SearchDict=gs.search(*SearchArgs)
#     except Exception as e:
#        sys.stdout.write("\n%s%s%s%s%s" % (bcolors.red,bcolors.underline,bcolors.bold, "DeBuggy was unable to fetch results. "
#                                             +str(e)+"\n Try again Later.",bcolors.end))
#        input('\nPress Enter to Continue. ')
#        sys.exit(1)
#     titles=[]
#     descriptions=[]
#     urls=[]
#     lnks=[]
#     for result in SearchDict:
#         titles.append(result['title'])
#         descriptions.append(result['description'])
#         lnks.append(result['link'])
#         urls.append(result['raw_url'])
#     return (titles,descriptions,lnks,urls)

def StackOverflow (url,screen_width=None):
  """Parse Stackoverflow url to extract answers and descriptions"""  
  global export_code  
  HtmlText= ParseUrl(url)#get response text
  if HtmlText in [None,False]:
    return 'Found captcha' if HtmlText==None else 'No Response ... Try Again ... (o_o)'
  try:
    QTitle = HtmlText.find_all('a', class_="question-hyperlink")[0].get_text()
    QStatus = HtmlText.find("div", attrs={"itemprop": "upvoteCount"}).get_text() # Vote count
    QStatus += " Votes | Asked " + HtmlText.find("time", attrs={"itemprop": "dateCreated"}).get_text() # Date created
    QDescription = StylizeCode(HtmlText.find_all("div", class_="s-prose js-post-body")[0])
    answers = [soup.get_text() for soup in HtmlText.find_all("div", class_="js-post-body")][
                1:]
  except:
      return 'Sorry Page cannot be Parsed. Try Another Link'              
  try:
      accepted_answer  = HtmlText.find_all("div",class_="accepted-answer")[0].find_all("div",class_="js-post-body")[0]#.get_text()
  except:
      accepted_answer = None
      text='answers'
  else:    
    if accepted_answer in answers:
        answers.remove(accepted_answer)
    try:
        width = (screen_width-15)//2
        #format = "="*width
        #text = "\n"+format +'ACCEPTED ANSWER'+format+"\n"
        text = "\n( ͡° ͜ʖ ͡°) ACCEPTED ANSWER ( ͡° ͜ʖ ͡°)\n"
    except:
        text = "\n( ͡° ͜ʖ ͡°) ACCEPTED ANSWER ( ͡° ͜ʖ ͡°)"    
    accepted_answer.insert(0,text)
    answers.insert(0,accepted_answer)
  finally:
    answers = [StylizeCode(answer,text,screen_width,ind) for ind,answer in enumerate(HtmlText.find_all("div", class_="s-prose js-post-body"))][1:]
    if len(answers) == 0:
        answers.append(("no answers", u"\nNo answers for this question."))
  exp = export_code.copy()
  export_code = []
  return QTitle,QDescription,QStatus, answers,exp


def ParseUrl(url):
    """Turns a given URL into a BeautifulSoup object."""
    #UAgent = UserAgent()#Randomize Fake User Agents
    try:
        Response = requests.get(url, headers={"User-Agent": gen_user_agent()},timeout=15)
        if Response.status_code is not 200:
          sys.stdout.write("\n%s%s%s%s%s" % (bcolors.red,bcolors.underline,bcolors.bold,"DeBuggy was unable to fetch results. "
                                            +Response.reason+"\n Try again Later. (o_o)", bcolors.end))
          return False
          #input('\nPress Enter to Continue. ')                                  
          #sys.exit(1) 
    except requests.exceptions.RequestException:#ConnectionError
        sys.stdout.write("\n%s%s%s%s%s" % (bcolors.red,bcolors.underline,bcolors.bold,"DeBuggy was unable to fetch results. "
                                            "Could be due to a Flag for Too many requests or Your Internet connection.\n", bcolors.end))
        
        return False
        #input('\nPress Enter to Continue. ')
        #sys.exit(1)
    except (requests.ConnectTimeout, requests.HTTPError, requests.ReadTimeout, requests.Timeout, requests.ConnectionError):                                       
        return False
    if "\.com/nocaptcha" in Response.url: # UrL is a captcha page
        return None
    else:
        return bs4(Response.text, "html.parser")  

def GSearch(query,page=1):
    """GOOGLE SEARCH PARSER WITHOUT DEPENDECY PACKAGE"""
    ran = 1 if page <= 0 else page
    # if page <= 0:
    #     page = 1
    titles=[]
    descriptions=[]
    urls=[]
    lnks=[]
    query=query+" site:stackoverflow.com"
    print(bcolors.green+"Debuggy is Fetching Results ... Please wait ... (>'-')> "+bcolors.end)
    for i in range(0,ran):
        titles.append("______ PAGE : "+ str(i+1) +" __________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________")
        lnks.append(None)
        #gquery =query.replace(" ","+")
        #gquery_url = "https://www.google.com/search?q="
        #softag_specifier = "+site%3Astackoverflow.com&page={}".format(i*10)
        #gurl = gquery_url+gquery+softag_specifier
        gurl=get_search_url(query,i)
        gsoup = ParseUrl(gurl)
        if not gsoup:
            input("Hit Enter to Continue: ")
            sys.exit(1)

        header_link_elem = gsoup.select('div[class="egMi0 kCrYT"] a')
        #description_elem = gsoup.select('div[class="BNeawe s3v9rd AP7Wnd"]')
        re_pattern='http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        for index in range(len(header_link_elem)):
                hl_element = header_link_elem[index]
                titles.append("**Parsable** "+hl_element.h3.text) if 'https://stackoverflow.com' in hl_element['href']  else titles.append(hl_element.h3.text)
                lnks.append(re.findall(re_pattern,hl_element['href'])[-1])#use regex
                #descriptions.append(description_elem[index].text)      
        if len(titles)==1:
            break
    return (titles,descriptions,lnks,urls)   


base_url = "https://www.google.com/"
search_url = urljoin(base_url, "search")

def get_search_url(query=None, page=None):
        """
        Return a formatted search url
        """
        # Some URLs use offsets
        offset = (page * 10) - 9
        params = get_params(
            query=query, page=page, offset=offset)
        url = urlparse(search_url)
        parsed_url = url._replace(query=urlencode(params))
        return parsed_url.geturl()


def get_params(query=None, offset=None, page=None):
        params = {}
        params["start"] = (page) * 10
        params["q"] = query
        params["gbv"] = 1
        return params               