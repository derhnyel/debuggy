import sys
import requests
from bs4 import BeautifulSoup as bs4 
from fake_useragent import UserAgent
from search_engine_parser.core.engines.google import Search as GoogleSearch
from  stalkoverflow.color import bcolors


export_code =[]


def StylizeCode(Text,verified_identifier=None,scr_width=None,index=None):
    """Identifies and stylizes code in a question or answer."""
    global export_code
    holder =[]
    # TODO: Handle blockquotes and markdown
    if verified_identifier is not None and verified_identifier not in Text:
        try:
            width = (scr_width-6)//2
            format = "="*width
            text = "\n"+format +'ANSWER'+format+"\n"
            Text.insert(0,text)
        except:
            Text.insert(0,"================ANSWER==============\n")
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

def GSearch(Error):
    """Fetch Results From Google"""
    try:
      print(bcolors.green+"Fetching Results...Please wait..."+bcolors.end)
      gs = GoogleSearch()
      SearchArgs=(Error,2)
      gs.clear_cache()
      SearchDict=gs.search(*SearchArgs)
    except Exception as e:
       sys.stdout.write("\n%s%s%s%s%s" % (bcolors.red,bcolors.underline,bcolors.bold, "DeBuggy was unable to fetch results. "
                                            +str(e)+"\n Try again Later.",bcolors.end))
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

def StackOverflow (url,screen_width=None):
  """Parse Stackoverflow url to extract answers and descriptions"""  
  global export_code  
  HtmlText= ParseUrl(url)#get response text
  if HtmlText in [None,False]:
    return 'Found captcha' if HtmlText==None else 'No internet connection'
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
        format = "="*width
        text = "\n"+format +'ACCEPTED ANSWER'+format+"\n"
    except:
        text = "\n===============ACCEPTED ANSWER============"    
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
    UAgent = UserAgent()#Randomize Fake User Agents

    
    try:
        Response = requests.get(url, headers={"User-Agent": UAgent.random},timeout=10)
        if Response.status_code is not 200:
          sys.stdout.write("\n%s%s%s%s%s" % (bcolors.red,bcolors.underline,bcolors.bold,"DeBuggy was unable to fetch results. "
                                            +Response.reason+"\n Try again Later.", bcolors.end))
          return False
          #input('\nPress Enter to Continue. ')                                  
          #sys.exit(1) 
    except requests.exceptions.RequestException:#ConnectionError
        sys.stdout.write("\n%s%s%s%s%s" % (bcolors.red,bcolors.underline,bcolors.bold,"DeBuggy was unable to fetch results. "
                                            "Please make sure you are connected to the internet.\n", bcolors.end))
        return False
        #input('\nPress Enter to Continue. ')
        #sys.exit(1)
    except (requests.ConnectTimeout, requests.HTTPError, requests.ReadTimeout, requests.Timeout, requests.ConnectionError):                                       
        return False
    if "\.com/nocaptcha" in Response.url: # UrL is a captcha page
        return None
    else:
        return bs4(Response.text, "html.parser")  