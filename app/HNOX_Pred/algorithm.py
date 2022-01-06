import pandas as pd
import statistics
import cmath
import nltk
import os

# ------------------------------ Global Variables (Address & Template) ----------------------

# address for a plant database
address_database = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "Data", "H-NOX plant list(Plant).csv")
database_pd = pd.read_csv(address_database, header=None)
# address for name of each amino acids and their three parameters
address_checklist = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), 'Data', 'CheckList.csv')
checklist_pd = pd.read_csv(address_checklist)

# address for processed means of three parameters based on the data from the database
storing_address = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), 'Data', 'Final mean results(Plant).csv')
# load calculated mean file
calculated_mean_pd = pd.read_csv(storing_address)


# ---------------------------------- Function ---------------------------------------


# input preprocess
def prepro_input(input):
    res = ''
    input = input.upper()
    for i in range(len(input)):
        if input[i] != ' ':
            res = res + input[i]
    res = res.replace('\n', '')
    return res


# Return maximum and minimum of Hydrophobic, pl, MW
def maxmin_return(checklist_pd):
    return checklist_pd.max()['hydrophobic'], checklist_pd.min()['hydrophobic'], checklist_pd.max()['pi'], \
           checklist_pd.min()['pi'], checklist_pd.max()[
               'weight'], checklist_pd.min()['weight']


# preprocessing database, capitalize all characters
def prepro_database(database_pd):
    database_pd = database_pd.dropna()
    for j in range(len(database_pd)):
        database_pd.iloc[j, 1] = database_pd.iloc[j, 1].upper()
    return database_pd


# calculate the mean of three according to the database
def mean_calculation(database_pd, checklist_pd, results_pd, storing_address):
    """
    :param database_pd: dataframe of original database
    :param checklist_pd: dataframe of original checklist
    :param results_pd: results dataframe format
    :param storing_address: address to store
    :return:
    """
    # results_pd has 33 rows
    for j in range(31):  # for this j loop, solve  x{27,31}
        set_MW = []
        set_pI = []
        set_Hy = []
        frequency = 0
        total_MW = 0
        total_pI = 0
        total_Hy = 0
        target_index = j + 1
        for i in range(len(database_pd)):
            GCC_Sequence = database_pd.iloc[i, 1]
            target = GCC_Sequence[target_index]
            if target != '.':
                frequency = frequency + 1
            # find the row index in checklist using target
            for k in range(len(checklist_pd)):
                if checklist_pd.iloc[k, 0] == target:
                    total_MW = total_MW + checklist_pd.iloc[k, 1]
                    set_MW.append(checklist_pd.iloc[k, 1])
                    total_Hy = total_Hy + checklist_pd.iloc[k, 2]
                    set_Hy.append(checklist_pd.iloc[k, 2])
                    total_pI = total_pI + checklist_pd.iloc[k, 3]
                    set_pI.append(checklist_pd.iloc[k, 3])
        if frequency == 0:
            mean_MW = 0
            SD_MW = 0
            SEM_MW = 0
            mean_pI = 0
            SD_pI = 0
            SEM_pI = 0
            mean_Hy = 0
            SD_Hy = 0
            SEM_Hy = 0
        else:
            mean_MW = total_MW / frequency
            SD_MW = statistics.stdev(set_MW)
            SEM_MW = SD_MW / cmath.sqrt(frequency)
            mean_pI = total_pI / frequency
            SD_pI = statistics.stdev(set_pI)
            SEM_pI = SD_pI / cmath.sqrt(frequency)
            mean_Hy = total_Hy / frequency
            SD_Hy = statistics.stdev(set_Hy)
            SEM_Hy = SD_Hy / cmath.sqrt(frequency)
        results_pd.iloc[j, 1] = mean_MW
        results_pd.iloc[j, 4] = SD_MW
        results_pd.iloc[j, 7] = SEM_MW
        results_pd.iloc[j, 2] = mean_pI
        results_pd.iloc[j, 5] = SD_pI
        results_pd.iloc[j, 8] = SEM_pI
        results_pd.iloc[j, 3] = mean_Hy
        results_pd.iloc[j, 6] = SD_Hy
        results_pd.iloc[j, 9] = SEM_Hy

    # Calculation for last two columns
    frequency = len(database_pd)
    set_MW = []
    set_pI = []
    set_Hy = []
    total_MW = 0
    total_pI = 0
    total_Hy = 0
    target_index = 33
    for i in range(len(database_pd)):
        GCC_Sequence = database_pd.iloc[i, 1]
        target = GCC_Sequence[target_index]
        for k in range(len(checklist_pd)):
            if checklist_pd.iloc[k, 0] == target:
                total_MW = total_MW + checklist_pd.iloc[k, 1]
                set_MW.append(checklist_pd.iloc[k, 1])
                total_Hy = total_Hy + checklist_pd.iloc[k, 2]
                set_Hy.append(checklist_pd.iloc[k, 1])
                total_pI = total_pI + checklist_pd.iloc[k, 3]
                set_pI.append(checklist_pd.iloc[k, 1])
    mean_MW = total_MW / frequency
    SD_MW = statistics.stdev(set_MW)
    SEM_MW = SD_MW / cmath.sqrt(frequency)
    mean_pI = total_pI / frequency
    SD_pI = statistics.stdev(set_MW)
    SEM_pI = SD_MW / cmath.sqrt(frequency)
    mean_Hy = total_Hy / frequency
    SD_Hy = statistics.stdev(set_MW)
    SEM_Hy = SD_MW / cmath.sqrt(frequency)
    results_pd.iloc[31, 1] = mean_MW
    results_pd.iloc[31, 4] = SD_MW
    results_pd.iloc[31, 7] = SEM_MW
    results_pd.iloc[31, 2] = mean_pI
    results_pd.iloc[31, 5] = SD_pI
    results_pd.iloc[31, 8] = SEM_pI
    results_pd.iloc[31, 3] = mean_Hy
    results_pd.iloc[31, 6] = SD_Hy
    results_pd.iloc[31, 9] = SEM_Hy
    set_MW = []
    set_pI = []
    set_Hy = []
    total_MW = 0
    total_pI = 0
    total_Hy = 0
    target_index = 33
    for i in range(len(database_pd)):
        GCC_Sequence = database_pd.iloc[i, 1]
        target = GCC_Sequence[target_index]
        for k in range(len(checklist_pd)):
            if checklist_pd.iloc[k, 0] == target:
                total_MW = total_MW + checklist_pd.iloc[k, 1]
                set_MW.append(checklist_pd.iloc[k, 1])
                total_Hy = total_Hy + checklist_pd.iloc[k, 2]
                set_Hy.append(checklist_pd.iloc[k, 1])
                total_pI = total_pI + checklist_pd.iloc[k, 3]
                set_pI.append(checklist_pd.iloc[k, 1])
    mean_MW = total_MW / frequency
    SD_MW = statistics.stdev(set_MW)
    SEM_MW = SD_MW / cmath.sqrt(frequency)
    mean_pI = total_pI / frequency
    SD_pI = statistics.stdev(set_MW)
    SEM_pI = SD_MW / cmath.sqrt(frequency)
    mean_Hy = total_Hy / frequency
    SD_Hy = statistics.stdev(set_MW)
    SEM_Hy = SD_MW / cmath.sqrt(frequency)
    results_pd.iloc[32, 1] = mean_MW
    results_pd.iloc[32, 4] = SD_MW
    results_pd.iloc[32, 7] = SEM_MW
    results_pd.iloc[32, 2] = mean_pI
    results_pd.iloc[32, 5] = SD_pI
    results_pd.iloc[32, 8] = SEM_pI
    results_pd.iloc[32, 3] = mean_Hy
    results_pd.iloc[32, 6] = SD_Hy
    results_pd.iloc[32, 9] = SEM_Hy
    # Write back to csv
    results_pd.to_csv(storing_address, sep=',', index=False, header=True)


# apply function when mean calculation==needed
def mean_calculation_function(storing_address):
    # pre-process database, all capitalized
    database = prepro_database(database_pd)

    # dataframe initialization of template for mean calculation
    l1 = list(range(1, 34))
    l2 = [0] * 33
    # read result file which==an empty template, process means
    mean_cal_template = pd.DataFrame({
        'X': l1,
        'MW_Means': l2,
        'pI_Means': l2,
        'Hydo_Means': l2,
        'MW_SD': l2,
        'pl_SD': l2,
        'Hy_SD': l2,
        'MW_SEM': l2,
        'pl_SEM': l2,
        'Hy_SEM': l2
    })
    results = mean_cal_template
    mean_calculation(database, checklist_pd, results, storing_address)


# decide the interval of value, which means to determine the flag
def deci_flag(mean, input):
    if mean > input:
        return -1
    else:
        return 0


# normalization
def normalization(flag, mean, max, min, input):
    """
    :param flag: true / false, left / right side
    :param mean: 0 / middle metrics
    :param max: 1 / right metrics
    :param min: 1 / left metrics
    :param input: number evaluated
    :return:
    """
    if flag == -1:  # means input==between min and mean
        interval = mean - min
        score = (input - min) / interval
    else:
        interval = max - mean
        score = 1 - ((input - mean) / interval)
    return score


# sub-function for detector, a box detector checking fitted mode: YxSxR
def box_detector(a, c, e, flag):
    if flag:
        return True
    else:  # to check the mode,==right return True, otherwise, return False
        if a == 'Y' and c == 'S' and e == 'R':
            return True
        else:
            return False


# test the position of the first H
def position_test(i, sequence):  # i: index of H
    len_seq = len(sequence)
    temp_i = i + 1
    if temp_i + 36 <= len_seq:  # if H can extract a complete sequence at least 37, return -1
        return -1
    else:
        box_range = len_seq - (temp_i + 32)  # 32
        return box_range


# find the fitted mode from a long string of input
def detector(input):
    # create a dataframe to store position intervals, 2 columns
    d = {0: {0: 0}, 1: {0: 0}}
    position_pd = pd.DataFrame(d, dtype='double')
    input = input.upper()  # all convert to upper
    for i in range(len(input) - 32):
        flag = False
        if input[i] == 'H':  # checking box from 28th to 32th
            num_flag = position_test(i, input)
            if num_flag == -1:
                box_range = 5
            else:
                box_range = num_flag

            # if fitting mode YxSxR
            for j in range(box_range):
                flag = box_detector(input[i + 28 + j], input[i + 30 + j],
                                    input[i + 32 + j], flag)
        if flag:  # if==true, fitting the mode
            for k in range(box_range):
                k = k + 1
                if input[i + 27 + k] == 'Y' and input[
                    i + 29 + k] == 'S' and input[i + 31 + k] == "R":
                    left_position = i
                    right_position = i + 31 + k
                    # add the position to the dataframe
                    last_rowIndex = len(position_pd) - 1
                    position_pd.iloc[last_rowIndex, 0] = left_position
                    position_pd.iloc[last_rowIndex, 1] = right_position
                    position_pd.loc[len(position_pd)] = [
                        0, 0
                    ]  # initialize next row
    return position_pd


# return chemicals from position interval
def chem_retrival(right_position, left_position, input):
    chem_string = ''
    for i in range(int(left_position - right_position + 1)):
        temp_index = int(right_position + i)
        chem_string = chem_string + input[temp_index]
    return chem_string


# Single HNOX sequence process
def HNOX_Calculation(HNOX_sequence, checklist):
    # calculate three means of GCC sequence
    len_GCC = len(HNOX_sequence
                  )  # check the length of the sequence to see if and x missing
    distance = 37 - len_GCC  # distance==between 0 and 4
    sum_MW = 0
    sum_pI = 0
    sum_Hy = 0
    for i in range(31 - int(distance)):
        temp_index = i + 1
        this_x = HNOX_sequence[
            temp_index]  # get the x component of this certain component
        for j in range(
                len(checklist)):  # check the place of x in the checklist
            if checklist.iloc[
                j, 0] == this_x:  # find the target, add their parameters
                sum_MW = sum_MW + checklist.iloc[j, 1]
                sum_Hy = sum_Hy + checklist.iloc[j, 2]
                sum_pI = sum_pI + checklist.iloc[j, 3]

    # dealing with the last two Xs
    index_last1 = len_GCC - 2
    target_last1 = HNOX_sequence[index_last1]
    index_last2 = len_GCC - 4
    target_last2 = HNOX_sequence[index_last2]
    for k in range(len(checklist)):
        if checklist.iloc[k, 0] == target_last1:
            sum_MW = sum_MW + checklist.iloc[k, 1]
            sum_Hy = sum_Hy + checklist.iloc[k, 2]
            sum_pI = sum_pI + checklist.iloc[k, 3]
    for k in range(len(checklist)):
        if checklist.iloc[k, 0] == target_last2:
            sum_MW = sum_MW + checklist.iloc[k, 1]
            sum_Hy = sum_Hy + checklist.iloc[k, 2]
            sum_pI = sum_pI + checklist.iloc[k, 3]
    mean_MW = sum_MW / (len_GCC - 4)
    mean_Hy = sum_Hy / (len_GCC - 4)
    mean_pI = sum_pI / (len_GCC - 4)

    # determines the interval of mean lies on
    max_Hy, min_Hy, max_pI, min_pI, max_MW, min_MW = maxmin_return(checklist)
    outMean_MW = calculated_mean_pd['MW_Means'].mean()
    outMean_pI = calculated_mean_pd['pI_Means'].mean()
    outMean_Hy = calculated_mean_pd['Hydo_Means'].mean()
    flag_MW = deci_flag(outMean_MW, mean_MW)
    flag_Hy = deci_flag(outMean_Hy, mean_Hy)
    flag_pI = deci_flag(outMean_pI, mean_pI)
    score_MW = normalization(flag_MW, outMean_MW, max_MW, min_MW, mean_MW)
    score_Hydro = normalization(flag_Hy, outMean_Hy, max_Hy, min_Hy, mean_Hy)
    score_pI = normalization(flag_pI, outMean_pI, max_pI, min_pI, mean_pI)
    return score_Hydro, score_MW, score_pI


# split long sequence according to headers and return sequence set
def intersection(long_seq):
    sequence_set = []
    location_set = []
    # store the location of start of each single long sequence input
    for i in range(len(long_seq)):
        if long_seq[i] == '>':
            location_set.append(i)
    # take the last position
    location_set.append(int(len(long_seq)))

    if len(location_set) == 1:
        # distinguish if there==no '>' discovered
        sequence_set.append(long_seq)
    else:
        if location_set[0] != 0:
            sig_loc = location_set[0]
            # test if there==a sequence before if there==only one >
            sequence_set.append(long_seq[0:sig_loc])
            for k in range(len(location_set) - 1):
                st = location_set[k + 0]
                en = location_set[k + 1]
                sequence_set.append(long_seq[st:en])
        else:
            # use location_set to find every sequence and store them in sequence_set
            for j in range(len(location_set) - 1):
                sta = int(location_set[j])
                end = int(location_set[j + 1])
                sequence = long_seq[sta:end]
                sequence_set.append(sequence)

    return sequence_set


def strip_point(sequence):
    out = ''
    for j in range(len(sequence)):
        if sequence[j] != '.':
            out = out + sequence[j]
    return out


# check if string s1 exist in string s2 and find its location
def index_of_str(s1, s2):
    res = []
    len1 = len(s1)
    len2 = len(s2)
    if s1 == "" or s2 == "":
        return -1
    for i in range(len1 - len2 + 1):
        if s1[i] == s2[0] and s1[i:i + len2] == s2:
            res.append(i)
    return res if res else -1


# recognize the single input sequence and return its header and real sequence
def header_recognition(sequence):
    tokens = nltk.word_tokenize(sequence)
    seq_index = -1
    for i in range(len(tokens)):
        if len(tokens[i]) >= 33:
            if i < len(tokens) - 1:
                if len(tokens[i + 1]) >= 33:  # fail safe
                    seq_index = i
                    break
            else:
                seq_index = i
                break
    start_index = index_of_str(sequence, tokens[seq_index])[0]
    header = sequence[0:start_index].strip()
    analyzed = sequence[start_index:]
    return header, analyzed


# process line break in sequence column, and delete the last row.
def process_lineBreaker(interim_res_pd):
    # delete last row
    interim_res_pd = interim_res_pd[:-1]
    for i in range(len(interim_res_pd)):
        interim_res_pd.iloc[i, 3] = str(
            interim_res_pd.iloc[i, 3]).replace('\n', '')
    return interim_res_pd


# single sequence process, return a head sequence, and dataframe with fitted sequence and their parameters
def main_process(header, analyzed_sequence, checklist, raw_output_template):
    """
    :param header: string sequence of head
    :param analyzed_sequence: sequence needed to be analyzed
    :param checklist: each amino acid and their parameters
    :return:
    """
    # Strip /n and while space, all capitalized
    pre_input = prepro_input(analyzed_sequence)

    # detect the strings that are the fitted mode
    position_pd = detector(pre_input)

    # print(header, ', sequence length is', len(position_pd))
    # print(position_pd[0])

    # position_pd==a dataset which contains fitted strings' interval
    # “-1” means the last position==initialization, which==empty

    R_i = len(raw_output_template)
    # print(L_i)
    if len(position_pd) == 1:
        raw_output_template.iloc[R_i - 1, 0] = 0
        raw_output_template.iloc[R_i - 1, 1] = 0
        raw_output_template.iloc[R_i - 1, 2] = 0
        raw_output_template.iloc[R_i - 1, 3] = 0
        raw_output_template.iloc[R_i - 1, 4] = 0
        raw_output_template.iloc[R_i - 1, 5] = 0
        raw_output_template.iloc[R_i - 1, 6] = 0
        raw_output_template.iloc[R_i - 1, 7] = 0
        raw_output_template.iloc[R_i - 1, 8] = header
        # Initialize the next result row
        raw_output_template.loc[len(raw_output_template)] = [
            0, 0, 0, 0, 0, 0, 0, 0, '']
    else:
        for i in range(len(position_pd) - 1):
            index_t = len(raw_output_template)
            raw_output_template.iloc[index_t - 1, 0] = i + 1

            # The position and interval of the hit
            start_index = position_pd.iloc[i, 0]
            end_index = position_pd.iloc[i, 1]
            raw_output_template.iloc[index_t - 1, 1] = start_index+1 ##########
            raw_output_template.iloc[index_t - 1, 2] = end_index + 1 #############

            # The GCC Sequence of the hit
            GCC_Sequence = chem_retrival(start_index, end_index, pre_input)
            raw_output_template.iloc[index_t - 1, 3] = GCC_Sequence

            # Calculation the score of three parameter of each hit
            Hydro, MW, Ip = HNOX_Calculation(GCC_Sequence, checklist)
            avg = (Hydro + MW + Ip) / 3
            raw_output_template.iloc[index_t - 1, 4] = Hydro
            raw_output_template.iloc[index_t - 1, 5] = MW
            raw_output_template.iloc[index_t - 1, 6] = Ip
            raw_output_template.iloc[index_t - 1, 7] = avg
            raw_output_template.iloc[index_t - 1, 8] = header
            # Initialize the next result row
            raw_output_template.loc[len(raw_output_template)] = [
                0, 0, 0, 0, 0, 0, 0, 0, '']

    # raw_output_template.to_csv('test.csv')
    return raw_output_template
