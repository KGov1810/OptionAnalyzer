import pandas as pd
import requests
from datetime import datetime
from api.nasdaq.config import DEFAULT_HEADERS

class BaseExtractor:
    def __init__(self, base_url=None, headers=None):
        pass
    def _make_request(self, url, params=None):
        pass

class CmeApi(BaseExtractor):
    
    def __init__(self):
        super().__init__()
        
    def get_option_quotes(self):
        """ 
        Should define asset_class otehrwise doesn't find the option chain
        https://www.cmegroup.com/markets/equities/nasdaq/e-mini-nasdaq-100.quotes.options.html#optionProductId=6745&strikeRange=ALL
        #TODO: Need to find mapping and logic to get dynamic cookies 
        """
        URL = "https://www.cmegroup.com/CmeWS/mvc/atm/strike-prices/10132/2025/3/ALL"

        HEADERS = {
            'accept':'application/json, text/plain, */*',
            'accept-encoding':'gzip, deflate, br, zstd',
            'accept-language':'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control':'no-cache',
            'cookie':'_evga_e567={%22uuid%22:%22a6ecb77cf9c5a104%22}; _sfid_848a={%22anonymousId%22:%22a6ecb77cf9c5a104%22%2C%22consents%22:[{%22consent%22:{%22provider%22:%22Consent%20Provider%22%2C%22purpose%22:%22Personalization%22%2C%22status%22:%22Opt%20In%22}%2C%22lastUpdateTime%22:%222025-03-02T21:26:02.145Z%22%2C%22lastSentTime%22:%222025-03-02T21:26:02.161Z%22}]}; kppid=vFx7HEGd1Yb; bm_ss=ab8e18ef4e; bm_mi=C83DA62254798E7BA657A4529210EA4A~YAAQzthLFzZatEGVAQAAZOXBWBpuUzzCtRPrWLsT5RL22iJpY73RkdixIcTOsp3mM9DJ/PrLNb3XwBmnm/JyNH6srj7nMlY7fcvo8tIdP31RXXb7m2yU24QupnoWEWUf9QDrXo5zPJHYa2xnwGM8zPEbew47Q6H11jYjHyvJnmaZZpq6+FWdTghGxvQ2fkHXb/GTMPRn335v+I3x673ydmi2Tx7wLSw/voGxrVvFPJTlOfeIKoUj06/5aGEDZeDKEzlqa/IrBVH7ivsSm01y6Yde4Nn4n206tObYBvjek4QDL7y/xgJ0S9Ue5fnwh2fPTuwEJ9XpwAVRTxXS0HMbsT6L5uMfnd46fo5JLtdKNP0Afz3kwwCsCCs3PUDae/u7W3s=~1; AKA_A2=A; ak_bmsc=4F16E404986D7EE6A4E4B52E02CA0783~000000000000000000000000000000~YAAQzthLFwlctEGVAQAAtgLCWBq52bL6y8z5/pFRYRIEhP0a6qP9OAP2ULy+2XvBtxRYmKcNZ1qelOOquNn2WTnOYyiez5bSDcUagrVexQTr4bWp2qVBaNOjuDWCFL/lHlNrPdx93qtbwkMGkhQkOU/uz7ldjlrCdXedswQgBLFGjrAIbVDt7PsHS/7cegTQoA3Exwblazo2lRV/y+5LYISouxJs+K/g9UNNXXkJfvTKgzDebQewqnJcwVkKdZSD5gHdnTDOK2tVyAjSulH9OU0egRXZpk20Ic3a0JxJWsBI2n3fCJvxxg4evxKo4Q9LcMCUdCcBXPhSLajYPQLN66dI4xD8xpPSgwtqF4WdD1fe8psEMrZaBjigzzN/pNmQjBVgMqNlQT2XPuc8sLFMlxIQfC/3y9kccSXbNbBSiVYc6hoIiDk4LP8MQ3fAqv1BfhJfv+eTS9814kjy9RZsEWPa3++LXNspiY0kBku2A55yE/8TlkWbgqRfV/qHNnQAWA/8RW+JjtV/ibndXZU2WZeMl4qo9XMkbtMzlJtEiV7EMPs6; OptanonAlertBoxClosed=2025-03-02T21:28:12.268Z; bm_so=73894DF857BC5E938AB0A08C521AF6E9D5AD939690DDB8E406701CC61AA8E618~YAAQzthLFzCTtEGVAQAAj7fJWALIcI30rikLWxYy87bIZCkfo/fgWg7oHFxAMVx/t45mAm4DWGlNFjKuoNw1zu4ppnwTW7gBaTxVxLCTFFh46+NFAt6TnJkNkzkSMJa0HCaQkwG3l71M2vEcn70ddT3g5GLNWgF050orq7XOs8x0EmOcy0X45VRqemt/cFCDrdL5b4sz0YSLc27VK2DIeW8pL3sFgeKsv26HFvozQDxAUv191Wmq0Afo9vsYulBVbUEyvQU3aBUHsVl93nhcisuNCHkDRZuHXgV8MlmaXRSMw3poOdQOpdk1TEUIs9CbtL+FCFAt8R/o8gXAA29mlYIIwcZuwJUkT5c/QStKX1Sbak3eKfS2axVGt5cHS4OxjRN9hsDCCmEgUP7pmNjpYWa9EJPSxdkCthJVe3wsDMI9zfsivmPqIhJzgbgnAloJPH9iGuduzKJ2woHKP7H3N+o=; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Mar+02+2025+22%3A36%3A14+GMT%2B0100+(heure+normale+d%E2%80%99Europe+centrale)&version=202403.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=e0111461-eede-417e-913c-85305fc8b3b1&interactionCount=3&isAnonUser=1&landingPath=NotLandingPage&groups=C0004%3A0%2CC0002%3A0%2CC0001%3A1%2CC0003%3A0&geolocation=FR%3BIDF&AwaitingReconsent=false; bm_lso=73894DF857BC5E938AB0A08C521AF6E9D5AD939690DDB8E406701CC61AA8E618~YAAQzthLFzCTtEGVAQAAj7fJWALIcI30rikLWxYy87bIZCkfo/fgWg7oHFxAMVx/t45mAm4DWGlNFjKuoNw1zu4ppnwTW7gBaTxVxLCTFFh46+NFAt6TnJkNkzkSMJa0HCaQkwG3l71M2vEcn70ddT3g5GLNWgF050orq7XOs8x0EmOcy0X45VRqemt/cFCDrdL5b4sz0YSLc27VK2DIeW8pL3sFgeKsv26HFvozQDxAUv191Wmq0Afo9vsYulBVbUEyvQU3aBUHsVl93nhcisuNCHkDRZuHXgV8MlmaXRSMw3poOdQOpdk1TEUIs9CbtL+FCFAt8R/o8gXAA29mlYIIwcZuwJUkT5c/QStKX1Sbak3eKfS2axVGt5cHS4OxjRN9hsDCCmEgUP7pmNjpYWa9EJPSxdkCthJVe3wsDMI9zfsivmPqIhJzgbgnAloJPH9iGuduzKJ2woHKP7H3N+o=^1740951375453; bm_s=YAAQzthLF/28tEGVAQAAl9jOWAJtBT+VtxW2jyOmCrlUyfzh/bgaCVWzH6MFimjsutGA2nammiqUJkC4J2aLFgWphn09/jfUjNAHpXtDBk99JHey/U9I4OpSH50/wA9UlLScrgEmxp668YInMrYE0A0bQEkjpfASNQjtxnoE7HZRrFzP2n7AKkHmK/Nn25va0Ieu61/T8Bxda6KHF5CezpqGidvynTXIqrSexMQU0qh+RT9LHe6z+skohivcZjF7Tmvm/LitGidCXPumjjQ/y0BIBmUfbOQYV743tjCOO5gPUX0TyVGtKHrieCoWpH19Pg0qVUCQZN54DwOn4e51JaCHZnxJoX215qnK0uWkY709DAgy9WMpvKQ5hCjo4Mu8dK3fH/5NiUXLIg25+nF7PYtUZZmftZRgiWpIlAMCEeHnSit1Xy4uXCHmFl315VsvJ+B4E9z0xmhUgDBclw==; bm_sv=DE13B4326B9BFC4177C44C6904D894A3~YAAQzthLF/68tEGVAQAAl9jOWBrWfOC2UmScVC91cy8Bc5T3q5b44ZXjARhqU5FCthSbaLNszxuo+NjX9AoatGiUoeSkcb+isFv5PZzYzATxwJ++B42R0fOxRBIiXJjFczFmodS/4LlcjHB5i/PXsm7rLcruWWPE3eIObnIW9CeaPyyj9PAVJY2YXa0UiYaWjBiTLDbqjdAMVwhOWTulvmETuu9D4yXNfUw1JdwzYqYHgbrhRM1GWLeN9+WODURDqnupcQ==~1',
            'pragma':'no-cache',
            'priority':'u=1, i',
            'referer':'https://www.cmegroup.com/markets/equities/sp/e-mini-sandp500.quotes.options.html',
            'sec-ch-ua':'"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':"Windows",
            'sec-fetch-dest':'empty',
            'sec-fetch-mode':'cors',
            'sec-fetch-site':'same-origin',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
        }

        PARAMS = {
            "isProtected":"",
            "_t":"1740951706146"
        }

        s = requests.Session()
        r = s.get(URL, headers=HEADERS, params=PARAMS)
        data = r.json()

        # Convert JSON data into a structured DataFrame
        rows = []
        for entry in data['strikePrices']:
            strike_price = entry['strikePrice']
            strike_rank = entry['strikeRank']
            
            for option_type in ('call', 'put'):
                if option_type in entry:
                    option_data = entry[option_type]
                    row = {
                        'Strike Price': strike_price,
                        'Strike Rank': strike_rank,
                        'Type': option_type.capitalize(),
                        **option_data
                    }
                    rows.append(row)

        # Create DataFrame
        df = pd.DataFrame(rows)
        
        return df
        