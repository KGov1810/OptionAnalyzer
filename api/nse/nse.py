import pandas as pd
import requests
from datetime import datetime
from api.nasdaq.config import DEFAULT_HEADERS

class BaseExtractor:
    def __init__(self, base_url=None, headers=None):
        pass
    def _make_request(self, url, params=None):
        pass

class NseApi(BaseExtractor):
    
    def __init__(self):
        super().__init__()
        
    def get_option_quotes(self,ticker:str="NIFTY"):
        """ 
        Should define asset_class otehrwise doesn't find the option chain
        https://www.nasdaq.com/market-activity/stocks/tsla/option-chain
        #TODO: Need to format and organize the output
        """
        
        url='https://www.nseindia.com/api/option-chain-indices'

        headers={        
            "accept":"*/*",
            "accept-encoding":"gzip, deflate, br, zstd",
            "accept-language":"fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control":"no-cache",
            "pragma":"no-cache",
            "priority":"u=1, i",
            "referer":"https://www.nseindia.com/option-chain",
            "cookie":'_ga=GA1.1.994048469.1735172257; AKA_A2=A; ak_bmsc=B1E4E407E8CB79A735540011B7292941~000000000000000000000000000000~YAAQrv4WAimps0CVAQAAjvdZVhoaiwb9bglbe20LHpRR25SY7M4PaFCCvgy0fZ6ZNf1GawW8navEGMimw+yOiDSqygyM/d7rZ+fMU/12hqweVCDIhMd9wdKwpwBQgfRCSpDdSl07DWQBQ+J4OEolDn+KwSFqrOIz9oPQ9CDjaJiQ7PW5ltw0E69QNfKfL1EgSEymhemHDi/ArItKvpGiWgLgyNk6Dunij7QC90YVmZhSqmnEZ0RnIFi8nyLFl01pw0ceNRG7/91KF0y1sA0s3+vcJv6pjEdlPVOTcmF+YzIuAKp0uocefDidBUwrTCrr5Lrdh282daBjIqd1hRrHOIagN4NB00yb1splYrDoLk+CoYvBDmXddCFNcsIsRvMXp1i5YiG1QqEd2jYD/+rSxerwdax8sZMn9bEqLIsDmEWIUOpfZIW5KE0lKCfDWuXdPxM1r37scmPQXhdVb7EYEA==; nsit=hR1pig22qTetJpl9_Ocv9s63; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTc0MDkxMDkyMCwiZXhwIjoxNzQwOTE4MTIwfQ.F-KoneO21Fyu0CyFIlG4kWmdqIcaVxRFEZ2xrX3JUw0; bm_sz=98A1E765C2E3201E2F2A9CED6D852F00~YAAQrv4WAnsYtECVAQAAyoZgVhpP1rnakVhwF/P8P7jUQN9yqj6aNYQVIXFLIeVchY6kSlrPgsDhlwpqaR6VeydxJxSVnSUBrPTz4BxVGNE5IofHfJHZePBwQC69wVNvtY3ZEAPs/FTwEUbdfcnwl1pHyXgbLJjf7mz7Ry0o31hG0NqBjZG+KOgNyI2gImcOMJv0LzxOISzpI1u0RBCU0SSjpe9gsUi+pFq3V3LG4LUKb5Pk55elITR/erOi9XGY9XP6+NiS651YdKD/j5JKrxbPEvmkHU1ifijtif8ftkc/ydq26Qr32lekpF7Cf6Jg7HSDcbwzydApuSl64K7sbWfCZbgR+JBC7XwACaenTlqEGVVGBIyQZGHj8Auz5IjP2j7gl9ylQppStUt7DHu3Bbrq85NyYv0m~4272951~4535344; RT="z=1&dm=nseindia.com&si=2b14dec7-3c34-44e4-be4e-8a4e3451587c&ss=m7rh62g7&sl=0&se=8c&tt=0&bcn=%2F%2F0217991e.akstat.io%2F"; _abck=6F460F42897C72D10335F9A8BAFCFFA5~0~YAAQrv4WAqwYtECVAQAA/ohgVg0hLpiY+cwSzRK78KwTWPKu9N7yQu/66tck31lpUkiObBKneheVKc1UxHHRKnG5n4ZVyypwjg4HCFjmB5J8oTv/jusPR08ldfBI9gAdCMYU4EkUmamG1vyDBJEtD6UgwMa16c9d86JJGuedTeErBfieWYRmx0eRvPFuDAaKK2PLJ+yyC3xgG3KuBANvRvaX0kcq6X2C6kxBnCw8WmjcNB8f6q1xP5jmL4voTXEEmx/SpzXtEEb0nsQpVNxnJY2R4NTaAZBEPS3+uPiTjiGZsxwh1jLpXnrs//pxWFAom7wo7XdIdAnJwlENSEH6iKAgB1Lc80Nn4XU2fvg1SnrpLQjb66bfWKxuoNPfXRHB+xsACZf0PJ2HoOCUJJGnVp2AoR09+MqU57AEMMWeUMbZReaa2IvtWTV1C81tkPUSL91opGh9l0RaNFs2ow9EaJncYyqcWLYbSthWMsRgXSlKB02e0lX361GAvPZm~-1~-1~-1; _ga_87M7PJ3R97=GS1.1.1740910512.3.1.1740910945.59.0.0; _ga_WM2NSQKJEK=GS1.1.1740910512.3.1.1740910945.0.0.0; bm_sv=5C46B350706947D36C54FDC019578A07~YAAQrv4WAvAYtECVAQAA9ItgVhqw11g+vBIr9+VGjFa6keLKQlRHPZhB/bh56FUVAQJ+n1GU9lJBTekZDECZGrNOQTVjCGv2x8bakva4WVwXhm2nKgUfxQgTbivsk9zAgy/Vzvy5JSBFnApROxmUEW7hfEjKjmP6RaOmiIcZC4REgwFh0XD579kHrbJpH+fS0XvIw7IBNLOPFZLuJUDfmt4YZ6eX50XUCVsVE613kZqQXrLGJwVTKAOt8y13Jpe6SrG8~1',
            "sec-ch-ua-platform":"Windows",
            "sec-fetch-dest":"empty",
            "sec-fetch-mode":"cors",
            "sec-fetch-site":"same-origin",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        }

        payload={"symbol":ticker}

        s=requests.Session()
        r=s.get(url, headers=headers, params = payload)
        j=r.json()
        j
        # df = pd.DataFrame(j['data']['table']['rows'])
        # return df
        