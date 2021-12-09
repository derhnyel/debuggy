import sys
import requests
from bs4 import BeautifulSoup as bs4 
from fake_useragent import UserAgent
from search_engine_parser.core.engines.google import Search as GoogleSearch
from  stalkoverflow.color import red,underline,bold,end



def StylizeCode(Text):
    """Identifies and stylizes code in a question or answer."""
    # TODO: Handle blockquotes and markdown
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
                    StylizedText.append(("code", u"\n%s" % str(child)))
                    newline = False
                else: # In-line code
                    StylizedText.append(("code", u"%s" % str(child)))
            else: # Plaintext
                newline = child.endswith('\n')
                StylizedText.append(u"%s" % str(child))

    if type(StylizedText[-2]) == tuple:
        # Remove newline from questions/answers that end with a code block
        if StylizedText[-2][1].endswith('\n'):
            StylizedText[-2] = ("code", StylizedText[-2][1][:-1])

    return StylizedText

def GSearch(Error):
    #global Connection
    try:
      gs = GoogleSearch()
      SearchArgs=(Error,1)
      gs.clear_cache()
      SearchDict=gs.search(*SearchArgs)
    except Exception as e:
       sys.stdout.write("\n%s%s%s%s%s" % (red,underline,bold, "DeBuggy was unable to fetch results. "
                                            +str(e)+"\n Try again Later.", end))
       #Connection = False
       #return Connection
       input('\nPress Enter to Continue. ')
       sys.exit(1)
    titles=[]
    descriptions=[]
    urls=[]
    lnks=[]
    for result in SearchDict:
        titles.append(result['title'])
        descriptions.append(result['description'])
        lnks.append(result['link'])
        urls.append(result['raw_url'])
    return (titles,descriptions,lnks,urls)

def StackOverflow (url):
  HtmlText= ParseUrl(url)
  try:
      QTitle = HtmlText.find_all('a', class_="question-hyperlink")[0].get_text()
      QStatus = HtmlText.find("div", attrs={"itemprop": "upvoteCount"}).get_text() # Vote count
      QStatus += " Votes | Asked " + HtmlText.find("time", attrs={"itemprop": "dateCreated"}).get_text() # Date created
      QDescription = StylizeCode(HtmlText.find_all("div", class_="s-prose js-post-body")[0]) # TODO: Handle duplicates

      answers = [StylizeCode(answer) for answer in HtmlText.find_all("div", class_="s-prose js-post-body")][1:]
  except:
      QTitle
      QStatus
      QDescription    
  if len(answers) == 0:
      answers.append(("no answers", u"\nNo answers for this question."))

  return QTitle,QDescription,QStatus, answers


def ParseUrl(url):
    UAgent = UserAgent()
    #global Connection
    """Turns a given URL into a BeautifulSoup object."""
    try:
        Response = requests.get(url, headers={"User-Agent": UAgent.random})
        if Response.status_code is not 200:
          sys.stdout.write("\n%s%s%s%s%s" % (red,underline,bold,"DeBuggy was unable to fetch results. "
                                            +Response.reason+"\n Try again Later.", end))
          #Connection=False
          input('\nPress Enter to Continue. ')                                  
          sys.exit(1) 
    except requests.exceptions.RequestException:
        #Connection=False
        sys.stdout.write("\n%s%s%s%s%s" % (red,underline,bold,"DeBuggy was unable to fetch results. "
                                            "Please make sure you are connected to the internet.\n", end))
        input('\nPress Enter to Continue. ')                                    
        sys.exit(1)
    if "\.com/nocaptcha" in Response.url: # URL is a captcha page
        return None
    else:
        return bs4(Response.text, "html.parser")  