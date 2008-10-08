from cheshire3.normalizer import SimpleNormalizer
from cheshire3.web import www_utils
from cheshire3.web.www_utils import multiReplace

class FormatNormalizer(SimpleNormalizer):


    
    def process_string(self, session, data):
        string = data.replace('4~~', '4to').replace('8~~', '8vo').replace('f~~', 'fo').replace('bdsde', 'Broadside').replace('Bdsde', 'Broadside').replace('~~', 'mo')
        return string
    
    
class LanguageNormalizer(SimpleNormalizer):
    def __init__(self, session, config, parent):
        self.dict = {"eng":'English',             
                     "bre":'Breton',
                     "cat":'Catalan',
                     "chu":'Church Slavonic',
                     "cze":'Czech',
                     "dan":'Danish',
                     "dut":'Dutch',
                     "fri":'Frisian',
                     "fre":'French',
                     "ger":'German',
                     "ita":'Italian',
                     "lat":'Latin',
                     "por":'Portuguese',
                     "sar":'Sardinian',
                     "spa":'Spanish',
                     "swe":'Swedish'
                     }
    
    def process_string(self, session, data):       
        return multiReplace(data, self.dict).replace("heb",'Hebrew')
            
        