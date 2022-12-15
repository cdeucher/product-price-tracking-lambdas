# https://github.com/awslabs/aws-support-tools/blob/master/Cognito/decode-verify-jwt/decode-verify-jwt.py

import json
import time
import urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode

region = 'us-east-1'
userpool_id = 'REPLACE_WITH_YOUR_USER_POOL_ID'
app_client_id = 'REPLACE_WITH_CLIENT_ID'

keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)


def lambda_handler(event, context):
    token = event['token']
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        print('Public key not found in jwks.json')
        return False
    public_key = jwk.construct(keys[key_index])
    message, encoded_signature = str(token).rsplit('.', 1)
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        print('Signature verification failed')
        return False
    print('Signature successfully verified')
    claims = jwt.get_unverified_claims(token)
    print('Checking claims:',claims)
    if time.time() > claims['exp']:
        print('Token is expired')
        return False
    if 'aud' in claims:
        check_aud = claims['aud']
    else:
        check_aud = claims['client_id']
    if check_aud != app_client_id:
        print('Token was not issued for this audience')
        return False
    return claims

if __name__ == '__main__':
    with urllib.request.urlopen(keys_url) as f:
      response = f.read()
    keys = json.loads(response.decode('utf-8'))['keys']

    event = {'token': ''}
    decrypt = lambda_handler(event, None)
    print('decrypt:', decrypt)

