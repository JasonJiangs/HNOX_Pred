import pandas as pd
from collections import OrderedDict
import xlsxwriter

# -------------------------------------------- Global Variable ----------------------------------

# Threshold of Hp
Green_Hp = 0.967
Black_Hp = 0.770

# Threshold of Mw
Green_Mw = 0.960
Black_Mw = 0.815

# Threshold of Ip
Green_Ip = 0.987
Black_Ip = 0.780

# Threshold of Mean
Green_Mean = 0.946
Black_Mean = 0.860

# color assigning
GREEN = 'Green'
BLACK = 'Black'
RED = 'Red'

# storing addresses of color and non color
noncolored_address = '\\result_noncolored.csv'
color_rough_address = '\\result_color.csv'


# -------------------------------------------- Functions ----------------------------------------


# determine colors
def color_determine(Hp, Mw, Ip, Me):
    """
    :param Hp: Hydrophobicity
    :param Mw: Molecular Weight
    :param Ip: Isoelectric Point
    :param Me: Mean
    :return: Colors of four parameters
    """
    # for Hydrophobicity
    if Hp >= Green_Hp:
        co_Hp = GREEN
    elif Hp >= Black_Hp:
        co_Hp = BLACK
    else:
        co_Hp = RED
    # for Molecular Weight
    if Mw >= Green_Mw:
        co_Mw = GREEN
    elif Mw >= Black_Mw:
        co_Mw = BLACK
    else:
        co_Mw = RED
    # for Isoelectric Point
    if Ip >= Green_Ip:
        co_Ip = GREEN
    elif Ip >= Black_Ip:
        co_Ip = BLACK
    else:
        co_Ip = RED
    # for mean
    if Me >= Green_Mean:
        co_Me = GREEN
    elif Me >= Black_Mean:
        co_Me = BLACK
    else:
        co_Me = RED

    return co_Hp, co_Mw, co_Ip, co_Me


def assi_inter(start, end, uncolored_pd, map_pd):
    """
    :param start: start column index
    :param end: end column index
    :param uncolored_pd: processed dataframe with raw
    :param map_pd: put color assign here
    :return: map_pd
    """
    # assign color
    interval = end - start - 1
    for i in range(interval):
        ind = start + i
        Hp = uncolored_pd.iloc[ind, 3]
        Mw = uncolored_pd.iloc[ind, 4]
        Ip = uncolored_pd.iloc[ind, 5]
        Me = uncolored_pd.iloc[ind, 6]
        co_Hp, co_Mw, co_Ip, co_Me = color_determine(Hp, Mw, Ip, Me)
        map_pd.iloc[ind, 3] = co_Hp
        map_pd.iloc[ind, 4] = co_Mw
        map_pd.iloc[ind, 5] = co_Ip
        map_pd.iloc[ind, 6] = co_Me

    return map_pd


# web color assigning
def threshold_assigning_web(uncolored_pd):
    # prepare a same sized dataframe for color assign
    map_pd = uncolored_pd.copy()
    for i in range(map_pd.shape[0]):
        for j in range(map_pd.shape[1]):
            map_pd.iloc[i, j] = 'N'

    # get indexes of all hit 1
    i_ind = []
    for i in range(len(uncolored_pd)):
        if uncolored_pd.iloc[i, 0] == '1':
            i_ind.append(i)
    i_ind.append(len(uncolored_pd) + 1)

    # loop i_ind to get the processed parameters
    for i in range(len(i_ind) - 1):
        ind_st = i_ind[i]
        ind_en = i_ind[i + 1]
        map_pd = assi_inter(ind_st, ind_en, uncolored_pd, map_pd)

    # assign header
    for i in range(len(i_ind) - 1):
        temp_ind = i_ind[i]
        head_ind = temp_ind - 1
        map_pd.iloc[head_ind, 0] = uncolored_pd.iloc[head_ind, 0]

    # assign hit, position, and sequence
    for i in range(len(i_ind) - 1):
        ind_st = i_ind[i]
        ind_en = i_ind[i + 1]
        ran = ind_en - ind_st - 1
        for j in range(ran):
            temp_i = ind_st + j
            map_pd.iloc[temp_i, 0] = uncolored_pd.iloc[temp_i, 0]
            map_pd.iloc[temp_i, 1] = uncolored_pd.iloc[temp_i, 1]
            map_pd.iloc[temp_i, 2] = uncolored_pd.iloc[temp_i, 2]

    # 对于第一个no matched 的sequence
    if str(uncolored_pd.iloc[1, 0]) == '0':
        map_pd.iloc[0, 0] = uncolored_pd.iloc[0, 0]
        for p in range(map_pd.shape[1]):
            map_pd.iloc[1, p] = uncolored_pd.iloc[1, p]

    return map_pd


# csv file color assigning
def threshold_assigning_csv(path_result):
    data = pd.read_csv(path_result + noncolored_address)
    lend = len(data)
    data = data.fillna(" ")

    # Use an OrderedDict to maintain the order of the columns
    data = OrderedDict((k, data.get(k)) for k in data.keys())
    # Open an Excel workbook
    workbook = xlsxwriter.Workbook(path_result + '\\result_colored.xlsx')
    # Set up a format
    book_format_red = workbook.add_format(properties={
        'bold': False,
        'font_color': 'red'
    })
    book_format_green = workbook.add_format(properties={
        'bold': True,
        'font_color': 'green'
    })
    book_format_black = workbook.add_format(properties={
        'bold': False,
        'font_color': 'black'
    })
    # Create a sheet
    worksheet = workbook.add_worksheet('dict_data')
    # Write the headers
    for col_num, header in enumerate(data.keys()):
        worksheet.write(0, col_num, header)

    for i in range(lend):
        cell_data = data['Hit-No'][i]
        if cell_data == ' ':
            continue
        else:
            worksheet.write(i + 1, 0, cell_data, book_format_black)

        cell_data = data['Position'][i]
        if cell_data == ' ':
            continue
        else:
            worksheet.write(i + 1, 1, cell_data, book_format_black)

        cell_data = data['H-NOX Sequence'][i]
        if cell_data == ' ':
            continue
        else:
            worksheet.write(i + 1, 2, cell_data, book_format_black)

        cell_data = data['H-NOX Hydrophobicity'][i]
        if cell_data == ' ':
            continue
        else:
            if float(cell_data) >= 0.967:
                worksheet.write(i + 1, 3, round(cell_data, 3),
                                book_format_green)
            elif float(cell_data) >= 0.770:
                worksheet.write(i + 1, 3, round(cell_data, 3),
                                book_format_black)
            elif float(cell_data) == 0:
                worksheet.write(i + 1, 3, round(cell_data, 3), book_format_black)
            elif float(cell_data) < 0.770:
                worksheet.write(i + 1, 3, round(cell_data, 3), book_format_red)

        cell_data = data['H-NOX Molecular Weight'][i]
        if cell_data == ' ':
            continue
        else:
            if float(cell_data) >= 0.960:
                worksheet.write(i + 1, 4, round(cell_data, 3), book_format_green)
            elif float(cell_data) >= 0.815:
                worksheet.write(i + 1, 4, round(cell_data, 3), book_format_black)
            elif float(cell_data) == 0:
                worksheet.write(i + 1, 4, round(cell_data, 3), book_format_black)
            elif float(cell_data) < 0.815:
                worksheet.write(i + 1, 4, round(cell_data, 3), book_format_red)

        cell_data = data['H-NOX Isoelectric Point'][i]
        if cell_data == ' ':
            continue
        else:
            if float(cell_data) >= 0.987:
                worksheet.write(i + 1, 5, round(cell_data, 3),
                                book_format_green)
            elif float(cell_data) >= 0.780:
                worksheet.write(i + 1, 5, round(cell_data, 3),
                                book_format_black)
            elif float(cell_data) == 0:
                worksheet.write(i + 1, 5, round(cell_data, 3), book_format_black)
            elif float(cell_data) < 0.780:
                worksheet.write(i + 1, 5, round(cell_data, 3), book_format_red)

        cell_data = data['H-NOX Mean'][i]
        if cell_data == ' ':
            continue
        else:
            if float(cell_data) >= 0.946:
                worksheet.write(i + 1, 6, round(cell_data, 3),
                                book_format_green)
            elif float(cell_data) >= 0.860:
                worksheet.write(i + 1, 6, round(cell_data, 3),
                                book_format_black)
            elif float(cell_data) == 0:
                worksheet.write(i + 1, 6, round(cell_data, 3), book_format_black)
            elif float(cell_data) < 0.860:
                worksheet.write(i + 1, 6, round(cell_data, 3), book_format_red)

    # Close the workbook
    workbook.close()


def color_assign_web_run(path_result):
    pd_t = pd.read_csv(path_result + noncolored_address)
    # print(pd_t)
    pd_c = threshold_assigning_web(pd_t)
    pd_c.to_csv(path_result + color_rough_address, sep=',', index=False, header=True)
