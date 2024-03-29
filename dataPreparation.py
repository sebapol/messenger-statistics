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


def load_message_file_from_directory(path):
    """
    Function loads Facebook .json files from the given path and returns pd.Dataframe object.
    Returned object contains data from .json 'messages' object.

    :param path:
        (str) path to folder where are .json Facebook files with 'messages' object
    :return:
        (pandas.Dataframe) object with columns=['sender_name', 'timestamp_ms', 'content']
    :exception DirectoryException:
        exception raised when given path do not exist
    """
    # checking if path exists
    if not exists(path):
        raise DirectoryException(path)
    # creating list containing paths to json files in path
    only_json_files = [join(path, f) for f in listdir(path) if (isfile(join(path, f)) and
                                                                f.startswith('message') and
                                                                f.endswith('.json'))]
    # creating empty data frame
    messages = pd.DataFrame()
    # filling dataframe with all json files data from list olyJsonFiles
    for filePath in only_json_files:
        with open(filePath) as file:
            chat_history = json.load(file)
        chat = pd.DataFrame(chat_history['messages'],
                            columns=['sender_name', 'timestamp_ms', 'content'])
        messages = pd.concat([messages, chat], ignore_index=True)
    return messages


def format_data(messages):
    """
    Function formatting pandas Dataframe object

    :param messages:
        (pandas.Dataframe) object with columns=['sender_name', 'timestamp_ms', 'content']
    :return:
        (pandas.Dataframe) formatted object with columns=['sender_name', 'timestamp_ms', 'content', 'DateTime',
                                                          'response_time', 'is_response']
    """
    messages.fillna(value={'content': '0'}, inplace=True)
    # decoding messages
    messages['content'] = messages['content'].apply(lambda content: content.encode('latin1').decode('utf8'))
    # decoding names
    messages['sender_name'] = messages['sender_name'].apply(lambda name: name.encode('latin1').decode('utf8'))
    # changing type of sender_name column to category
    messages['sender_name'] = messages['sender_name'].astype('category')
    messages['DateTime'] = pd.to_datetime(messages['timestamp_ms'], unit='ms').dt.ceil(freq='s')  # date_time
    # sorting by date from older to newer
    messages.sort_values('DateTime', inplace=True)
    messages.reset_index(inplace=True)
    messages['response_time'] = messages['DateTime'].diff()
    messages['is_response'] = messages['sender_name'].shift(periods=1) != messages['sender_name']
    return messages


def group_data_by_users(df):
    """
    Groups pd.Dataframe object df by sender_name column values

    :param df:
         (pandas.Dataframe) object with sender_name column
    :return:
         (pandas.groupby) object that contains information about the groups
    """
    user_group = df.groupby(by='sender_name')
    return user_group


def filter_data_by_date(data, start_date, end_date):
    """
    Filters pd.Dataframe object data by dates: from start_date to end_date

    :param data:
        (pandas.Dataframe) object
    :param start_date:
        datetime.datetime object
    :param end_date:
        datetime.datetime object
    :return:
        (pandas.Dataframe) object df by dates
    :exception ValueError:
        exception raised when start date is later than end date
    :exception KeyError:
        exception raised when there is no messages between start and end date
    """
    # including messages sent till end of the end_date day
    end_date = end_date + datetime.timedelta(hours=23, minutes=59, seconds=59)
    if start_date > end_date:
        raise ValueError('Start date later than end date!')
    data = data[(data['DateTime'] >= start_date) & (data['DateTime'] <= end_date)]
    if len(data) == 0:
        raise KeyError(f'No messages between {start_date} and {end_date}!')
    return data


def give_chat_members(path):
    """
    Returns dictionary with all chats members and paths to its .json files

    :param path:
        (str) path to folder where are Facebook message folder
    :return:
        (dict) dictionary with chats members names as keys and path to each chat .json file as values
    """
    mypath = join(path, 'messages/inbox')
    # checking if path exists
    if not exists(mypath):
        raise DirectoryException(mypath)
    # creating list containing paths to .json chat file of each member
    file_paths = [join(mypath, f, 'message_1.json') for f in listdir(mypath) if isdir(join(mypath, f))]
    # creating dictionary containing chat members and paths to chats
    names = {}
    for file_path in file_paths:  # try
        with open(file_path) as file:
            chat_history = json.load(file)
        name_data = chat_history['title']
        # decoding names
        name = name_data.encode('latin1').decode('utf8')
        names[name] = file_path
    return names


def get_dates_range(df):
    """
    Returns dates range, from first to last day when there was texting

    :param df:
        (pandas.Dataframe) object with 'DateTime' column
    :return:
        datetime.timedelta object
    """
    minimum = df['DateTime'].min()
    maximum = df['DateTime'].max()
    step = maximum - minimum
    step = step.days
    dates_range = [(minimum + datetime.timedelta(days=x)).date() for x in range(step)]
    return dates_range
