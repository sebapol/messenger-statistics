import pandas as pd
import json
from os import listdir
from os.path import isfile, isdir, join, exists
import datetime


class DirectoryException(Exception):
    def __init__(self, path):
        super().__init__('No such directory')
        self.path = path

    def __str__(self):
        return f'{super().__str__()} :{self.path}'


def loadMessageFilesFromDirectory(path):
    '''
    Function loads Facebook .json files from the given path and returns pd.Dataframe object.
    Returned object contains data from .json 'messages' object.

    :param path:
        (str) path to folder where are .json Facebook files with 'messages' object
    :return:
        pandas Dataframe object with columns=['sender_name', 'timestamp_ms', 'content']
    :exception DirectoryException:
        exception raised when given path do not exist
    '''
    # checking if path exists
    if not exists(path):
        raise DirectoryException(path)
    # creating list containing paths to json files in path
    onlyJsonFiles = [join(path, f) for f in listdir(path) if (isfile(join(path, f)) and
                                                              f.startswith('message') and
                                                              f.endswith('.json'))]  # funkcja glob()
    # creating empty data frame
    messages = pd.DataFrame()
    # filling dataframe with all json files data from list olyJsonFiles
    for filePath in onlyJsonFiles:
        with open(filePath) as file:
            chat_history = json.load(file)
        chat = pd.DataFrame(chat_history['messages'],
                            columns=['sender_name', 'timestamp_ms', 'content'])
        messages = pd.concat([messages, chat], ignore_index=True)
    return messages


def formatData(messages):
    '''
    Function formatting pandas Dataframe object
    :param messages:
        pandas Dataframe object with columns=['sender_name', 'timestamp_ms', 'content']
    :return:
        pandas Dataframe formatted object with columns=['sender_name', 'timestamp_ms', 'content']
    '''
    messages.fillna(value={'content': '0'}, inplace=True)
    # decoding messages
    messages['content'] = messages['content'].apply(lambda content: content.encode('latin1').decode('utf8'))
    # decoding names
    messages['sender_name'] = messages['sender_name'].apply(lambda name: name.encode('latin1').decode('utf8'))
    # changing type of sender_name column to category
    messages['sender_name'] = messages['sender_name'].astype('category')
    # creating new datetime column accurate to seconds
    messages['DateTime'] = pd.to_datetime(messages['timestamp_ms'], unit='ms').dt.ceil(freq='s')  # date_time
    # sorting by date from older to newer
    messages.sort_values('DateTime', inplace=True)
    # resetting index
    messages.reset_index(inplace=True)

    return messages


def groupDataByUsers(df):
    '''
    Groups pd.Dataframe object df by sender_name column values
    :param df:
         pd.Dataframe object with sender_name column
    :return:
         Pandas groupby object that contains information about the groups
    '''
    user_group = df.groupby(by='sender_name')
    return user_group


def filterDataByDate(data, startDate, endDate):
    '''
    Filters pd.Dataframe object df by dates: from startDate to endDate
    :param df:
        pd.Dataframe object
    :param startDate:
        datetime.datetime object
    :param endDate:
        datetime.datetime object
    :return:
        pd.Dataframe object df by dates
    :exception ValueError:
        exception raised when start date is later than end date
    :exception KeyError:
        exception raised when there is no messages between start and end date
    '''
    endDate = endDate + datetime.timedelta(hours=23, minutes=59, seconds=59)
    if startDate > endDate:
        raise ValueError('Start date later than end date!')
    data = data[(data['DateTime'] >= startDate) & (data['DateTime'] <= endDate)]
    if len(data) == 0:
        raise KeyError(f5'No messages between {startDate} and {endDate}!')  # todo: uodpornic inne funkcje
    return data


def giveChatMembers(path):
    mypath = join(path, 'messages/inbox')
    # checking if path exists
    if not exists(mypath):
        raise DirectoryException(mypath)
    # creating list containing paths to .json chat file of each member
    filePaths = [join(mypath, f, 'message_1.json') for f in listdir(mypath) if (isdir(join(mypath, f)))]
    # creating dictionary containing chat members and paths to chats
    names = {}
    for filePath in filePaths:  # try
        with open(filePath) as file:
            chat_history = json.load(file)
        # creating dataframe wich contains chat members names
        data = chat_history['title']
        # decoding names
        name = data.encode('latin1').decode('utf8')
        names[name] = filePath
    return names


def getDatesRange(df):
    min = df['DateTime'].min()
    print('min=', min)
    max = df['DateTime'].max()
    print('max=', max)
    step = max - min
    step = step.days
    print('days=', step)
    datesRange = [(min + datetime.timedelta(days=x)).date() for x in range(step)]
    return datesRange
