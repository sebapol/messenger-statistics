import datetime


def time_to_seconds(time):
    """
    converts hours, minutes and seconds in datetime object time to seconds
    :param time:
        datetime object
    :return:
        int seconds
    """
    return time.second + time.minute * 60 + time.hour * 60 * 60


def mean_texting_hour(data, column_name):
    """
    returns mean texting hours from pandas dataframe object df
    :param data:
        pandas dataframe object with 'DateTime' column
    :param column_name:
        (str) name of date column in data pandas dataframe object
    :return:
        datetime.timedelta object
    """

    time = data[column_name].apply(func=time_to_seconds)
    mean_time = time.mean()
    return datetime.timedelta(seconds=mean_time)


def daily_texting_histogram(df):
    data = df
    weekdays_names = {'0': 'Monday',
                      '1': 'Tuesday',
                      '2': 'Wednesday',
                      '3': 'Thursday',
                      '4': 'Friday',
                      '5': 'Saturday',
                      '6': 'Sunday'}
    plot = data.groupby(data['DateTime'].dt.weekday).count().sender_name.plot(kind="bar",
                                                                              figsize=(15, 4),
                                                                              xlabel='Day of week',
                                                                              rot=45)
    xticks = plot.axes.get_xticklabels()
    for tick in xticks:
        tick.set_text(weekdays_names[tick.get_text()])
    plot.set_xticklabels(xticks)
    return plot


def monthly_texting_histogram(df):
    data = df
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
    plot = data.groupby(data["DateTime"].dt.month).count().sender_name.plot(kind="bar",
                                                                            figsize=(15, 4),
                                                                            xlabel='Month',
                                                                            ylabel='messages', rot=45)
    xticks = plot.axes.get_xticklabels()
    for tick in xticks:
        tick.set_text(months_names[tick.get_text()])
    plot.set_xticklabels(xticks)
    return plot


def hourly_texting_histogram(df):
    data = df
    plot = data \
        .groupby(data["DateTime"].dt.hour) \
        .count() \
        .sender_name \
        .plot(kind="bar", figsize=(15, 4), xlabel='Hour')
    return plot


def response_times(df, sender_name, max_response_time):
    data = df
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
    if len(response_time) > 0:
        avg_response_time = datetime.timedelta(seconds=int(sum(response_time) / len(response_time)))
    else:
        avg_response_time = 0
    return avg_response_time


def median_response_time(response_time):
    from statistics import median
    if len(response_time) > 0:
        median_time = median(response_time)
        median_time = datetime.timedelta(seconds=median_time)
    else:
        median_time = 0
    return median_time


def average_message_length(grouped_df, sender_name):
    data = grouped_df.get_group(sender_name)
    mean = data['content'].apply(lambda x: len(x)).mean()
    return mean


def count_messages(grouped_df, frequency, sender_name):  # YAGNI niepotrzebna funkcja
    pos_freq = ['min', 'H', 'D', 'M', 'Y']
    if frequency not in pos_freq:
        raise Exception(f'Wrong frequency! Allowed: {pos_freq}')
    data = grouped_df.get_group(sender_name)
    data = data[['sender_name', 'DateTime']].set_index('DateTime')
    return data.resample(frequency).count()


def count_words(grouped_df, sender_name, min_word_length):
    import re
    df = grouped_df.get_group(sender_name)
    words_counts = {}
    for message in df['content']:
        words = re.findall(r'\w+', message)
        for word in words:
            word = word.lower()
            if len(word) > (min_word_length - 1):
                if word in words_counts.keys():
                    words_counts[word] += 1
                else:
                    words_counts[word] = 1
    return words_counts


def most_used_words(words_counts, number_of_words=1):
    popular_words = []
    words = words_counts.copy()
    for i in range(number_of_words):
        max_word = max(words, key=words.get)
        popular_words.append((max_word, words.pop(max_word)))
    return popular_words


def give_most_used_words(grouped_df, sender_name, min_word_length, number_of_words=1):
    words = most_used_words(count_words(grouped_df, sender_name, min_word_length), number_of_words)
    return words


def who_text_first(df, time_offset):
    data = df
    first_message_counter = {}
    first = True
    for i in data.index:
        if first:
            first_message_counter[df['sender_name'][i]] = 1
            first = False
            continue
        if data['DateTime'][i] - data['DateTime'][i - 1] >= time_offset:
            if df['sender_name'][i] in first_message_counter.keys():
                first_message_counter[df['sender_name'][i]] += 1
            else:
                first_message_counter[df['sender_name'][i]] = 1
    return first_message_counter
