class Prompt:
    prompt_template = ''
    news_prompt = ''
    seperator_character = '=>'
    identifier_character = '->'
    tools_definition = ['NEWS', 'PARSE', 'SUMMARY']
    def __init__(self):
        self.prompt_template = """
            You are an AI assistant with several tools available to you. The tools are the following:
            {TOOL_DEFINITIONS}

            DO NOT USE TOOLS WITHIN TOOLS! KEEP ALL TOOL CALLS SEPARATE FROM EACH OTHER!

            {TOOL_EXAMPLES}
            User: {USER_INPUT}
            Assistant:
            """
        self.news_prompt = f"""
            User: What's the latest news on technology?
            Assistant: [NEWS{self.seperator_character}Technology] {self.identifier_character} As of March 24, 2023, there are various news sources reporting on technology. CBS News, Reuters, US News, and SciTechDaily are some of the news outlets that provide the latest news on new technology, social media, artificial intelligence, computers, and more[1][2][3][4]. The latest news on technology from US News reports that scandal-plagued Japan tech giant Toshiba has accepted a $15 billion tender offer] As of March 24, 2023, there are various news sources reporting on technology. CBS News, Reuters, US News, and SciTechDaily are some of the news outlets that provide the latest news on new technology, social media, artificial intelligence, computers, and more[1][2][3][4]. The latest news on technology from US News reports that scandal-plagued Japan tech giant Toshiba has accepted a $15 billion tender offer.
            
            User: What's the latest news on svb bank?
            Assistant: [NEWS{self.seperator_character}SVB bank] {self.identifier_character} I'm sorry, but I couldn't find any recent news on SVB Bank. It's possible that no significant events or developments have been reported recently.
            
            User: Can you summarize this paper https://arxiv.org/pdf/2303.13439v1.pdf
            Assistant: [PARSE{self.seperator_character}https://arxiv.org/pdf/2303.13439v1.pdf] {self.identifier_character} I'm sorry, but I couldn't find any recent news on SVB Bank. It's possible that no significant events or developments have been reported recently.
            
            """
        tool_definitions = ''
        for tool in self.tools_definition:
            tool_definitions += tool + " "

        # add news
        tool_examples = ''
        tool_examples += self.news_prompt

        self.prompt_template = self.prompt_template.replace("{TOOL_DEFINITIONS}", tool_definitions)
        self.prompt_template = self.prompt_template.replace("{TOOL_EXAMPLES}", tool_examples)

    def query(self, query):
        self.__init__()
        self.prompt_template = self.prompt_template.replace("{USER_INPUT}", query)
        return self.prompt_template


    
    