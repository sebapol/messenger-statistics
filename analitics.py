import datetime


def time_to_seconds(time):
    """
    Converts hours, minutes and seconds in datetime object time to seconds

    :param time:
        datetime.datetime object
    :return:
        (int) time in seconds
    """
    return time.second + time.minute * 60 + time.hour * 60 * 60


def mean_texting_hour(data, column_name):
    """
    Returns mean texting hours from pandas dataframe object df

    :param data:
        (pandas.Dataframe) object with 'DateTime' column
    :param column_name:
        (str) name of date column in data pandas dataframe object
    :return:
        datetime.timedelta object
    """

    time = data[column_name].apply(func=time_to_seconds)
    mean_time = time.mean()
    return datetime.timedelta(seconds=mean_time)


def daily_texting_histogram(data, fig_size=(15, 4)):
    """
    Returns histogram showing daily texting frequency

    :param data:
        (pandas.Dataframe) object with 'DateTime' column
    :param fig_size:
        (tuple) size of histogram, default = (15,4)
    :return:
        plot object containing weekdays histogram
    """
    weekdays_names = {'0': 'Monday',
                      '1': 'Tuesday',
                      '2': 'Wednesday',
                      '3': 'Thursday',
                      '4': 'Friday',
                      '5': 'Saturday',
                      '6': 'Sunday'}
    plot = data.groupby(data['DateTime'].dt.weekday).count().sender_name.plot(kind="bar",
                                                                              figsize=fig_size,
                                                                              xlabel='Day of week',
                                                                              rot=45)
    xticks = plot.axes.get_xticklabels()
    for tick in xticks:
        tick.set_text(weekdays_names[tick.get_text()])
    plot.set_xticklabels(xticks)
    return plot


def monthly_texting_histogram(data, fig_size=(15, 4)):
    """
    Returns histogram showing monthly texting frequency

    :param data:
        (pandas.Dataframe) object with 'DateTime' column
    :param fig_size:
        (tuple) size of histogram, default = (15,4)
    :return:
        plot object containing months histogram
    """
    months_names = {'1': 'January',
                    '2': 'February',
                    '3': 'March',
                    '4': 'April',
                    '5': 'May',
                    '6': 'June',
                    '7': 'July',
                    '8': 'August',
                    '9': 'September',
                    '10': 'October',
                    '11': 'November',
                    '12': 'December'}
    plot = data \
        .groupby(data["DateTime"].dt.month) \
        .count() \
        .sender_name \
        .plot(kind="bar", figsize=fig_size, xlabel='Month', ylabel='messages', rot=45)
    xticks = plot.axes.get_xticklabels()
    for tick in xticks:
        tick.set_text(months_names[tick.get_text()])
    plot.set_xticklabels(xticks)
    return plot


def hourly_texting_histogram(data, fig_size=(15, 4)):
    """
    Returns histogram showing monthly texting frequency

    :param data:
        (pandas.Dataframe) object with 'DateTime' column
    :param fig_size:
        (tuple) size of histogram, default = (15,4)
    :return:
        plot object containing hourly histogram
    """
    plot = data \
        .groupby(data["DateTime"].dt.hour) \
        .count() \
        .sender_name \
        .plot(kind="bar", figsize=fig_size, xlabel='Hour')
    return plot


def response_times(data, sender_name, max_response_time):
    """
    Function counts all response times of given sender and returns list of times that are smaller than given max time.

    :param data:
        (pandas.Dataframe) object with 'DateTime' and 'sender_name' column
    :param sender_name:
        (str)
    :param max_response_time:
        (datetime.timedelta) maximum response time that will be considered as response
    :return:
        (List[int]) list contains response times in seconds smaller than max
    """
    response_time = []
    first = True
    for i in data.index:
        if first:
            first = False
            continue
        if (data['sender_name'][i] == sender_name) & (data['sender_name'][i] != data['sender_name'][i - 1]):
            difference = data['DateTime'][i] - data['DateTime'][i - 1]
            if difference <= max_response_time:
                response_time.append(difference.seconds)
    return response_time


def average_response_time(response_time):
    """
    Counts average response time of given response times list

    :param response_time:
        (List[int]) list contains response times in seconds
    :return:
        (datetime.timedelta) arithmetic average response time in seconds
    """
    if len(response_time) > 0:
        avg_response_time = datetime.timedelta(seconds=int(sum(response_time)/len(response_time)))
    else:
        avg_response_time = 0
    return avg_response_time


def median_response_time(response_time):
    """
    Counts median of response time of given response times list

    :param response_time:
        (List[int]) list contains response times in seconds
    :return:
        (datetime.timedelta) median of response time in seconds
    """
    from statistics import median
    if len(response_time) > 0:
        median_time = median(response_time)
        median_time = datetime.timedelta(seconds=median_time)
    else:
        median_time = 0
    return median_time


def average_message_length(grouped_df, sender_name):
    """
    Counts average message length of given sender

    :param grouped_df:
        (pandas.groupby) object that contains information about the senders
    :param sender_name:
        (str) name of sender
    :return:
        (int) average message length of sender
    """
    data = grouped_df.get_group(sender_name)
    mean = data['content'].apply(lambda x: len(x)).mean()
    return mean


def count_words(grouped_df, sender_name, min_word_length):
    """
    Counts times of appearance of every word in all messages of sender

    :param grouped_df:
        (pandas.groupby) object that contains information about the senders
    :param sender_name:
        (str) name of sender
    :param min_word_length:
        (int) minimal length of word
    :return:
        (Dict[str, int]) dictionary - word : times word appeared
    """
    import re
    df = grouped_df.get_group(sender_name)
    words_counts = {}
    pattern = r'\w{' + str(min_word_length) + r',}'
    for message in df['content']:
        # searching for only alphabetical string of characters
        words = re.findall(pattern, message.lower())
        for word in words:
            if word in words_counts.keys():
                words_counts[word] += 1
            else:
                words_counts[word] = 1
    return words_counts


def most_used_words(words_counts, number_of_words=1):
    """
    Returns the most used words from given dictionary - word : times word appeared

    :param words_counts:
        (Dict[str, int]) dictionary - word : times word appeared
    :param number_of_words:
        (int) number of words which have to be returned
    :return:
        (List[(int,str)]) list of tuples that contains number of appearances (int) and word (str)
    """
    popular_words = []
    words = words_counts.copy()
    for i in range(number_of_words):
        max_word = max(words, key=words.get)
        popular_words.append((max_word, words.pop(max_word)))
    return popular_words


def give_most_used_words(grouped_df, sender_name, min_word_length, number_of_words=1):
    """
    Returns given number of words of sender

    :param grouped_df:
        (pandas.groupby) object that contains information about the senders
    :param sender_name:
        (str) name of sender
    :param min_word_length:
        (int) minimal length of word
    :param number_of_words:
        (int) number of words which have to be returned
    :return:
        (List[(int,str)]) list of tuples that contains number of appearances (int) and word (str)
    """
    words = most_used_words(count_words(grouped_df, sender_name, min_word_length), number_of_words)
    return words


def who_text_first(data, time_offset):
    """
    Counts times each member of chat texted after given time offset

    :param data:
        (pandas.Dataframe) object with 'DateTime' and 'sender_name' column
    :param time_offset:
        (datetime.timedelta) time offset that determines when can consider if message is not an answer to previous
    :return:
        (Dict[str, int]) dictionary - sender name : times sender texted firs
    """
    first_message_counter = {data['sender_name'][data.index[0]]: 1}
    for i in data.index[1:]:
        if data['DateTime'][i] - data['DateTime'][i - 1] >= time_offset:
            if data['sender_name'][i] in first_message_counter.keys():
                first_message_counter[data['sender_name'][i]] += 1
            else:
                first_message_counter[data['sender_name'][i]] = 1
    return first_message_counter
