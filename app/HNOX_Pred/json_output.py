import json
import pandas as pd
from app.HNOX_Pred.algorithm import header_recognition

address_color = '\\result_color.csv'
address_nonColor = '\\result_noncolored.csv'
address_json_out = '\\web_output.json'


def separation(L_seq, fitPos_set):
    '''
    :param L_seq: single long sequence
    :param fitPos_set: indexes of positions of all fitted sequence
    :return: textlist_:
    '''
    textlist_ = []
    # separate every lines for each line reaching 100 characters
    head, pure_sequence = header_recognition(L_seq)
    head = head.upper()
    pure_sequence = pure_sequence.upper()
    # replace \n
    pure_sequence = pure_sequence.replace('\n', '')
    # bold fitted target
    for j in range(len(fitPos_set)):
        # split start and end
        slist = fitPos_set[j].split('-')
        sStart = int(slist[0])
        sEnd = int(slist[1])
        # pure_sequence = pure_sequence[0:sStart] + \
        #     pure_sequence[sStart:sEnd - 1].lower() + pure_sequence[sEnd - 1:]
        if sStart//100 != sEnd//100:  # 换行
            pure_sequence = pure_sequence[0:sStart-1] + \
                            pure_sequence[sStart-1:sEnd].lower() + \
                            pure_sequence[sEnd:]
        else:  # 不换行
            pure_sequence = pure_sequence[0:sStart-1] + \
                            pure_sequence[sStart-1:sEnd].lower() + \
                            pure_sequence[sEnd:]


    # rough set, splitting 100 characters each
    temp_set = []
    num_line = len(pure_sequence) // 100
    if len(pure_sequence) % 100 != 0:
        num_line = num_line + 1
    for i in range(num_line):
        if i != num_line - 1:
            temp_set.append(pure_sequence[i * 100:(i + 1) * 100])
        else:
            temp_set.append(pure_sequence[i * 100:len(pure_sequence)])

    # determine upper case and lower case, and decide to bold or not bold
    for k in range(num_line):
        final_line_set = []
        # pure sequence of this line
        this_line = temp_set[k]

        for l in range(len(this_line) - 1):
            if this_line[l].isupper() and this_line[l + 1].islower():
                str_q = list(this_line)
                str_q.insert(l + 1, ' ')
                this_line = ''.join(str_q)
            elif this_line[l].islower() and this_line[l + 1].isupper():
                str_q = list(this_line)
                str_q.insert(l + 1, ' ')
                this_line = ''.join(str_q)
        # set of a single 100 sequence that has been split
        this_line_set = this_line.split(' ')

        # process split set of this line
        final_line_set = []
        for m in range(len(this_line_set)):
            single_cell = this_line_set[m]
            # for result line number
            if m == 0:
                # # no bold
                # if single_cell[0].isupper():
                #     tt = {'value': str(k) + ' ' + single_cell.upper(),
                #           'color': 'black', 'bold': False}
                # # bold
                # else:
                #     tt = {'value': str(k) + ' ' + single_cell.upper(),
                #           'color': 'black', 'bold': True}
                # no bold
                if single_cell[0].isupper():
                    if k < 10:
                        tt = {'value': '0'+str(k)+'01'+' ' + single_cell.upper(), 'color': 'black', 'bold': False}
                    else:
                        tt = {'value': str(k)+'01'+' ' + single_cell.upper(), 'color': 'black', 'bold': False}
                # bold
                else:
                    if k < 10:
                        tt = {'value': '0'+str(k)+'01'+' ' + single_cell.upper(), 'color': 'black', 'bold': True}
                    else:
                        tt = {'value': str(k)+'01'+' ' + single_cell.upper(), 'color': 'black', 'bold': True}
                final_line_set.append(tt)
            else:
                # no bold
                if single_cell[0].isupper():
                    tt = {'value': single_cell.upper(), 'color': 'black',
                          'bold': False}
                # bold
                else:
                    tt = {'value': single_cell.upper(), 'color': 'black',
                          'bold': True}
                final_line_set.append(tt)
        textlist_.append(final_line_set)
    return textlist_


def json_run(sequence_set, path_result):
    pd_color = pd.read_csv(path_result + address_color)
    for i in range(pd_color.shape[0]):
        if pd_color.iloc[i, 0] == str(0):
            pd_color.iloc[i - 1, 1] = 'N'
            pd_color.iloc[i - 1, 2] = 'N'
            pd_color.iloc[i - 1, 3] = 'N'
            pd_color.iloc[i - 1, 4] = 'N'
            pd_color.iloc[i - 1, 5] = 'N'
            pd_color.iloc[i - 1, 6] = 'N'
            pd_color.iloc[i, 3] = 'N'
            pd_color.iloc[i, 4] = 'N'
            pd_color.iloc[i, 5] = 'N'
            pd_color.iloc[i, 6] = 'N'

    pd_nonColor = pd.read_csv(path_result + address_nonColor)

    # find row index of all headers
    row_index = []
    for i in range(pd_color.shape[0]):
        if pd_color.iloc[i, 1] == 'N':
            row_index.append(i)
    row_index.append(pd_color.shape[0])

    web_output = []
    for i in range(len(sequence_set)):  # for every long sequence
        L_seq = sequence_set[i]
        head, analyzed_sequence = header_recognition(L_seq)
        this_seq = {}
        this_seq['text'] = {}
        this_seq['table'] = []
        this_seq['text']["title"] = str(head)
        this_seq['text']['textlist'] = []

        # check number of fitted short sequence in this long sequence
        length_s = row_index[i + 1] - row_index[i] - 1

        # solve table
        for j in range(length_s):
            tempR_ind = row_index[i] + j + 1
            fit_info = {"Hit": {"value": str(pd_color.iloc[tempR_ind, 0]), "color": 'black', "bold": False},
                        "Position": {"value": pd_color.iloc[tempR_ind, 1], "color": 'black', "bold": False},
                        "HNOXSequence": {"value": pd_color.iloc[tempR_ind, 2], "color": 'black', "bold": True},
                        "HNOXHydrophobicity": {"value": str(round(pd_nonColor.iloc[tempR_ind, 3], 3)),
                                               "color": pd_color.iloc[tempR_ind, 3], "bold": False},
                        "HNOXMolecularWeight": {"value": str(round(pd_nonColor.iloc[tempR_ind, 4], 3)),
                                                "color": pd_color.iloc[tempR_ind, 4], "bold": False},
                        "HNOXIsoelectricPoint": {"value": str(round(pd_nonColor.iloc[tempR_ind, 5], 3)),
                                                 "color": pd_color.iloc[tempR_ind, 5], "bold": False},
                        "HNOXMean": {"value": str(round(pd_nonColor.iloc[tempR_ind, 6], 3)),
                                     "color": pd_color.iloc[tempR_ind, 6], "bold": False}}
            this_seq['table'].append(fit_info)

        # solve text
        fitPos_set = []
        for k in range(length_s):
            tempR_ind = row_index[i] + k + 1
            fitPos_set.append(pd_color.iloc[tempR_ind, 1])

        textlist_ = separation(L_seq, fitPos_set)
        this_seq['text']['textlist'] = textlist_
        web_output.append(this_seq)

    for i in range(len(web_output)):
        # print(web_output[i])
        if web_output[i]['table'] and web_output[i]['table'][0]['HNOXHydrophobicity']['color'] == 'N':
            web_output[i]['table'] = []
            web_output[i]['text']['textlist'] = []

    return web_output
