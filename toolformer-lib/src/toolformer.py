
import openplayground

import tool.prompt
import tool.news
import tool.parse

import re
from urllib.parse import urlparse
class ToolFormer:
    
    # nat.dev session token, make sure login first before access this lib
    session_token = ''
    client = openplayground.Client
    news = tool.news.News
    prompt = tool.prompt.Prompt
    parse = tool.parse.Parse
    min_to_summarize = 4000

    def __init__(self, session_token, newsapi_apikey):
        self.session_token = session_token
        self.refresh_session()
        self.news = tool.news.News(newsapi_apikey)
        self.prompt = tool.prompt.Prompt()
        self.parse = tool.parse.Parse()

    def refresh_session(self):
        self.client = openplayground.Client(self.session_token)
        self.check_token_valid()
        
    def check_token_valid(self):
        assert len(self.client.get_models()) > 0
    
    def call_open_ai(self, query):
        result = ''
        for chunk in self.client.generate("openai:gpt-3.5-turbo", self.prompt.query(query), maximumLength=1024):        
            if chunk["event"] == "infer":
                result += chunk["message"]
                print(chunk["message"], end="", flush=True)
            if chunk["message"] == "[COMPLETED]":
                self.on_complete(result)

    def call_claude_ai(self, query):
        for chunk in self.client.generate("anthropic:claude-instant-v1.0", query, maximumLength=1024):
            if chunk["event"] == "infer":
                print(chunk["message"], end="", flush=True)
                            
                                            
    def on_complete(self, result):
        match = re.match(f"([[])\S.+?({self.prompt.identifier_character})", result)
        if match:
            extract_tool = match.group(0)
            extract_tool = extract_tool.replace('[', '').replace(']', '').replace(self.prompt.identifier_character, '')
            extract_tool = [x.strip() for x in extract_tool.split(self.prompt.seperator_character)]
            if extract_tool[0] in self.prompt.tools_definition:
                print(self.is_url(extract_tool[1]))
                print(extract_tool[1])
                if self.is_url(extract_tool[1]):
                    self.call_claude_ai(self.parse.parse(extract_tool[1])[:self.min_to_summarize])
                else :
                    match extract_tool[0]:
                        case 'NEWS':
                            combine_text= ''
                            combine_source = '\nSources: '
                            for news in self.news.query(extract_tool[1]):
                                combine_text += self.parse.parse(news.url, news.source['name'])
                                combine_source += '\n' + news.source['name'] + ':' + news.url
                                if len(combine_text) >= self.min_to_summarize:
                                    break
                            self.call_claude_ai(combine_text[:self.min_to_summarize])
                            print(combine_source)


                        case 'PARSE':
                            print(self.parse.parse(extract_tool[1]))

    
    def query(self, query):
        assert len(query) > 0
        print(query)
        self.call_open_ai(query)

    # https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
    def is_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False