

def renderUserConfig(privatekey, userIpLastDigit, SERVER_PUBLIC_KEY, SERVER_IP):
    text = f'''
    [Interface]
    PrivateKey = {privatekey.strip()}
    Address = 10.0.0.{userIpLastDigit.strip()}/32
    DNS = 8.8.8.8

    [Peer]
    PublicKey = {SERVER_PUBLIC_KEY.strip()}
    Endpoint = {SERVER_IP.strip()}:51830
    AllowedIPs = 0.0.0.0/0
    PersistentKeepalive = 20
    '''.split('\n')

    return '\n'.join([i.strip() for i in text[1::]])

def renderServerConfigAddition(publickey, userIpLastDigit):
    text = f"""
    [Peer]
    PublicKey = {publickey.strip()}
    AllowedIPs = 10.0.0.{userIpLastDigit.strip()}/32
    """.split('\n')
    
    return '\n'.join(i.strip() for i in text)

if __name__ == '__main__':
    print(renderUserConfig('a','b','c','d'))
    print(renderServerConfigAddition('a','b'))