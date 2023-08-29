import os
from wireguardLib.cfg import *
from wireguardLib.utils.renderConfig import renderUserConfig, renderServerConfigAddition
import json
import time
import re


class userConfigCreator():


    def __init__(self, userId = False, configPath = CFG_PATH):

        self.keysCreated = False
        self.configCreated = False
        self.configPath = configPath

        if not userId:
            self.userId = len([i for i in os.listdir(configPath) if i.startswith('userConfig') and not os.path.isfile(i)])
        else:
            self.userId = userId

        clientId = self.userId
        
        userKeysPath = {'privatekey': f'user_{clientId}_privatekey', 
                        'publickey': f'user_{clientId}_publickey'}
        self.userKeysPath = userKeysPath

        userConfigPath = f'{configPath}/userConfig_{clientId}'
        os.system(f'mkdir "{userConfigPath}"')
        self.userConfigPath = userConfigPath

        self.userIpLastDigit = str(self.userId + 2)


    def createKeys(self) -> None:

        userConfigPath = self.userConfigPath
        userKeysPath = self.userKeysPath

        os.system(f'wg genkey | tee "{userConfigPath}"/{userKeysPath["privatekey"]} | wg pubkey | tee "{userConfigPath}"/{userKeysPath["publickey"]}')

        privatekeyPath, publickeyPath = f"{userConfigPath}/{userKeysPath['privatekey']}", f"{userConfigPath}/{userKeysPath['publickey']}"
        with open(publickeyPath) as publickey:
            self.publickey = publickey.read().strip()
        
        with open(privatekeyPath) as privatekey:
            self.privatekey = privatekey.read().strip()
        
        renderedServerConfig = renderServerConfigAddition(self.publickey, self.userIpLastDigit)
        self.renderedServerConfig = renderedServerConfig

        renderedUserConfig = renderUserConfig(self.privatekey, self.userIpLastDigit, SERVER_PUBLIC_KEY, SERVER_IP)
        self.renderedUserConfig = renderedUserConfig

        self.keysCreated = True


    def createConfig(self) -> None:

        if not self.keysCreated:
            raise 'KeysNotCreatedError. You should create keys for user before creating config'

        userConfigPath = self.userConfigPath
        userConfigFilePath = f"{userConfigPath}/userConfig_{self.userId}.conf"
        
        with open(userConfigFilePath, 'w') as userConfig:
            userConfig.write(self.renderedUserConfig)

        self.userConfigFilePath = userConfigFilePath
        self.configCreated = True


    def saveAllUserConfiguration(self) -> None:

        if not(self.keysCreated * self.configCreated):
            raise 'Keys and Config not created'

        config = {"userId": self.userId,
                  "userIpLastDigit": self.userIpLastDigit,
                  "privatekey": self.privatekey,
                  "publickey": self.publickey,
                  "renderedServerConfig":self.renderedServerConfig,
                  "timestamp": time.time()}
        
        userConfigPath = self.userConfigPath

        with open(f'{userConfigPath}/allConfig.json', 'w') as allConfig:
            json.dump(config, allConfig, indent=4)
    


class userConfigManipulator():

    def __init__(self, userId, configsPath = CFG_PATH):

        self.userId = userId
        self.configsPath = configsPath
        with open(f'{configsPath}/userConfig_{userId}/allConfig.json') as userConfig:
            self.userConfig = json.load(userConfig)


    def addUserToServerConfig(self) -> None:

        publickey = self.userConfig['publickey']
        userIpLastDigit = self.userConfig['userIpLastDigit']
        renderedServerConfig = self.userConfig['renderedServerConfig']

        with open(f'{self.configsPath}/serverConfig.conf', 'a') as serverConfig:
            serverConfig.write(renderedServerConfig)

    def deleteUserFromServerConfig(self) -> None:

        userConfig = self.userConfig
        renderedServerConfig = self.userConfig['renderedServerConfig']

        with open(f'{self.configsPath}/serverConfig.conf', 'r') as serverConfig:
            serverConfigData = serverConfig.read()

        serverConfigData = serverConfigData.replace(renderedServerConfig, "")

        with open(f'{self.configsPath}/serverConfig.conf', 'w') as serverConfig:
            serverConfig.write(serverConfigData)





if __name__ == '__main__':

    user = userConfigCreator()

    user.createKeys()
    user.createConfig()
    user.saveAllUserConfiguration()

    time.sleep(5)

    admin1 = userConfigManipulator(0)
    admin2 = userConfigManipulator(1)
    admin3 = userConfigManipulator(2)
    admin4 = userConfigManipulator(3)
    admin5 = userConfigManipulator(4)

    admin1.deleteUserFromServerConfig()
    admin2.deleteUserFromServerConfig()
    admin3.deleteUserFromServerConfig()
    admin4.deleteUserFromServerConfig()
    
    admin5.addUserToServerConfig()

