import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# ouo url
# eg: https://ouo.io/HxFVfD
url = ""

# -------------------------------------------
# RECAPTCHA v3 BYPASS
# code from https://github.com/xcscxr/Recaptcha-v3-bypass

def RecaptchaV3(ANCHOR_URL):
    url_base = 'https://www.google.com/recaptcha/'
    post_data = "v={}&reason=q&c={}&k={}&co={}"
    client = requests.Session()
    client.headers.update({
        'content-type': 'application/x-www-form-urlencoded'
    })
    matches = re.findall('([api2|enterprise]+)\/anchor\?(.*)', ANCHOR_URL)[0]
    url_base += matches[0]+'/'
    params = matches[1]
    res = client.get(url_base+'anchor', params=params)
    token = re.findall(r'"recaptcha-token" value="(.*?)"', res.text)[0]
    params = dict(pair.split('=') for pair in params.split('&'))
    post_data = post_data.format(params["v"], token, params["k"], params["co"])
    res = client.post(url_base+'reload', params=f'k={params["k"]}', data=post_data)
    answer = re.findall(r'"rresp","(.*?)"', res.text)[0]    
    return answer

ANCHOR_URL = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lcr1ncUAAAAAH3cghg6cOTPGARa8adOf-y9zv2x&co=aHR0cHM6Ly9vdW8uaW86NDQz&hl=en&v=1B_yv3CBEV10KtI2HJ6eEXhJ&size=invisible&cb=4xnsug1vufyr'

# -------------------------------------------
# OUO BYPASS

def ouo_bypass(url):
    client = requests.Session()
    p = urlparse(url)
    id = url.split('/')[-1]
    
    res = client.get(url)
    
    bs4 = BeautifulSoup(res.content, 'lxml')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }
    
    ans = RecaptchaV3(ANCHOR_URL)
    data['x-token'] = ans
    
    h = {
        'content-type': 'application/x-www-form-urlencoded'
    }
    
    url = f"{p.scheme}://{p.hostname}/go/{id}"
    res = client.post(url, data=data, headers=h, allow_redirects=False)
    
    return {
        'original_link': url,
        'bypassed_link': res.headers.get('Location')
    }
    
# -------------------------------------------

out = ouo_bypass(url)
print(out)

'''
SAMPLE OUTPUT

{
    'original_link': 'https://ouo.io/go/HxFVfD',
    'bypassed_link': 'https://some-link.com'
}

'''
