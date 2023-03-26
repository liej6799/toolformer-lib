import tool.prompt
import tool.news
import tool.parse
import helper.enum

import re
from urllib.parse import urlparse
class ToolFormer:
    _news = tool.news.News
    _prompt = tool.prompt.Prompt
    _parse = tool.parse.Parse

    min_to_summarize = 4000

    def __init__(self, _newsapi_apikey):
        self._news = tool.news.News(_newsapi_apikey)
        self._prompt = tool.prompt.Prompt()
        self._parse = tool.parse.Parse()

    def query(self, query):
        assert len(query) > 0
        match = re.match(f"([[])\S.+?({self._prompt.identifier_character})", query)
       
        if not match:
            self.print_toolFormer('prompt not matched')
            return ToolFormerResult(helper.enum.ModelResult.NONE, '')

        extract_tool = match.group(0)
        extract_tool = extract_tool.replace('[', '').replace(']', '').replace(self._prompt.identifier_character, '')
        extract_tool = [x.strip() for x in extract_tool.split(self._prompt.seperator_character)]
       

        if extract_tool[0] not in self._prompt.tools_definition:   
            self.print_toolFormer('_prompt Tool Definition not matched')
            return ToolFormerResult(helper.enum.ModelResult.NONE, '')
        
        if self.is_url(extract_tool[1]):
            self.print_toolFormer('Matched URL')
            self.print_toolFormer('Parsing: ' + extract_tool[1])
            text = self._parse.parse(extract_tool[1])[:self.min_to_summarize]
            self.print_toolFormer('Done parse.')
            return ToolFormerResult(helper.enum.ModelResult.CLAUDE_INSTANT, text)
        
        match extract_tool[0]:
            case 'NEWS':
                self.print_toolFormer('Matched Tool : NEWS')
                text = ''
                for _news in self._news.query(extract_tool[1]):
                    text += self._parse.parse(_news.url, _news.source['name'])
                    if len(text) >= self.min_to_summarize:
                        break
                return ToolFormerResult(helper.enum.ModelResult.CLAUDE_INSTANT, text)
            

    # https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
    def is_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
        
    def print_toolFormer(self, text):        
        print('ToolFormer: ' + text)

class ToolFormerResult:
    def __init__(self, ModelResult, TextResult):
        self.ModelResult = ModelResult
        self.TextResult = TextResult