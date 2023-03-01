import datetime


def timeToSeconds(time):
    '''
    converts hours, minutes and seconds in datetime object time to seconds
    :param time:
        datetime object
    :return:
        int seconds
    '''
    return time.second + time.minute * 60 + time.hour * 60 * 60


def meanTextingHour(data, column_name):  # TODO: zmienić sygnaturę funkcji(data, column_name)
    '''
    returns mean texting hours from pandas dateframe object df
    :param df:
        pandas dateframe object with 'DateTime' column
    :return:
        datetime.timedelta object
    '''

    time = data['DateTime'].apply(func=timeToSeconds)  # TODO: time = data[column_name].apply(func=timeToSeconds)
    meanTime = time.mean()
    return datetime.timedelta(seconds=meanTime)


def dailyTextingHistogram(df):
    data = df
    weekdaysNames = {'0': 'Monday',
                     '1': 'Tueseday',
                     '2': 'Wedneseday',
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
        tick.set_text(weekdaysNames[tick.get_text()])
    plot.set_xticklabels(xticks)
    return plot


def monthlyTextingHistogram(df):
    data = df
    monthsNames = {'1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June', '7': 'July',
                   '8': 'August',
                   '9': 'September', '10': 'October', '11': 'November', '12': 'December'}
    plot = data.groupby(data["DateTime"].dt.month).count().sender_name.plot(kind="bar", figsize=(15, 4), xlabel='Month',
                                                                            ylabel='messages', rot=45)
    xticks = plot.axes.get_xticklabels()
    for tick in xticks:
        tick.set_text(monthsNames[tick.get_text()])
    plot.set_xticklabels(xticks)
    return plot


def hourlyTextingHistogram(df):
    data = df
    plot = data\
        .groupby(data["DateTime"].dt.hour)\
        .count()\
        .sender_name\
        .plot(kind="bar", figsize=(15, 4), xlabel='Hour')
    return plot


def responseTimes(df, senderName, maxResponseTime):
    data = df
    responseTime = []
    first = True
    for i in data.index:
        if first:
            first = False
            continue
        if (data['sender_name'][i] == senderName) & (data['sender_name'][i] != data['sender_name'][i - 1]):
            difference = data['DateTime'][i] - data['DateTime'][i - 1]
            if difference <= maxResponseTime:
                responseTime.append(difference.seconds)
    return responseTime


def averageResponseTime(responseTime):
    if len(responseTime) > 0:
        avgResponseTime = datetime.timedelta(seconds=int(sum(responseTime) / len(responseTime)))
    else:
        avgResponseTime = 0
    return avgResponseTime


def medianResponseTime(responseTime):
    from statistics import median
    if len(responseTime) > 0:
        medianResponseTime = median(responseTime)
        medianResponseTime = datetime.timedelta(seconds=medianResponseTime)
    else:
        medianResponseTime = 0
    return medianResponseTime


def averageMessageLength(grouped_df, senderName):
    data = grouped_df.get_group(senderName)
    mean = data['content'].apply(lambda x: len(x)).mean()
    return mean


def messageCounter(grouped_df, frequency, senderName):#YAGNI niepotrzebna funkcja
    posFreq = ['min', 'H', 'D', 'M', 'Y']
    if frequency not in posFreq:
        raise Exception(f'Wrong frequency! Allowed: {posFreq}')
    data = grouped_df.get_group(senderName)
    data = data[['sender_name', 'DateTime']].set_index('DateTime')
    return data.resample(frequency).count()


def wordsCounter(grouped_df, senderName, minWordLength):
    import re
    df = grouped_df.get_group(senderName)
    wordsCounts = {}
    for message in df['content']:
        words = re.findall(r'\w+', message)
        for word in words:
            word = word.lower()
            if len(word) > (minWordLength - 1):
                if word in wordsCounts.keys():
                    wordsCounts[word] += 1
                else:
                    wordsCounts[word] = 1
    return wordsCounts


def mostUsedWords(wordsCounts, numberOfWords=1):
    popularWords = []
    words = wordsCounts.copy()
    for i in range(numberOfWords):
        maxWord = max(words, key=words.get)
        popularWords.append((maxWord, words.pop(maxWord)))
    return popularWords


def showMostUsedWords(grouped_df, senderName, minWordLength, numberOfWords=1):
    words = mostUsedWords(wordsCounter(grouped_df, senderName, minWordLength), numberOfWords)
    return words


def whoTextFirst(df, timeOffset):
    data = df
    firstMessageCounter = {}
    first = True
    for i in data.index:
        if first:
            firstMessageCounter[df['sender_name'][i]] = 1
            first = False
            continue
        if (data['DateTime'][i] - data['DateTime'][i - 1] >= timeOffset):
            if df['sender_name'][i] in firstMessageCounter.keys():
                firstMessageCounter[df['sender_name'][i]] += 1
            else:
                firstMessageCounter[df['sender_name'][i]] = 1
    return firstMessageCounter
