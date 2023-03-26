from newspaper import Article

class Parse:
    pre_prompt_source = 'According to '
    post_prompt_source = ', '
    def parse(self, url, source = ''):
        try:
            article = Article(url)
            article.download()
            article.parse()
            
            if source:
                source = self.pre_prompt_source + source.strip() + self.post_prompt_source

            return source + article.text.replace('\n','').strip()
        except:
            return ''