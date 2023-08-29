import time
import datetime

def generateNewTimeStamp(daysToAdd):
    return time.time() + 60 * 60 * 24 * daysToAdd


if __name__ == '__main__':
    dt = datetime.datetime.fromtimestamp(generateNewTimeStamp(7))
    print(dt)