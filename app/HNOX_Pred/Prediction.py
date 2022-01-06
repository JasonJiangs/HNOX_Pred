#!/usr/bin/env python3
# coding=UTF-8
'''
Date: 2021-12-06 21:53:46
LastEditTime: 2021-12-13 01:13:39
Description: file content
'''
from app.HNOX_Pred.run_function import *
from app.HNOX_Pred.color_assigning import *
from app.HNOX_Pred.json_output import *
import os


def run(path_result, hash, input_text):
    if not os.path.exists(path_result):
        os.makedirs(path_result)
    # dataframe initialization of template for raw output
    raw_output_template = pd.DataFrame({
        'Hit-No': [0],
        'Position Start': [0],
        'Position End': [0],
        'Sequence': [0],
        'Hydrophobicity': [0],
        'Molecular Weight': [0],
        'Isoelectric Point': [0],
        'Mean': [0],
        'Header': ['']
    })

    # For txt file as input
    # f_path = 'txt Input/H-NOX (true).txt'
    f_path = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), "txt Input", f"{hash}.txt")
    with open(f_path, 'w', encoding='utf8') as f:
        f.write(input_text)
    interim_res_pd, pure_sequence_set, sequence_set = main_func_txt_input(
        f_path, raw_output_template)

    # process results pd for output, 1. delete line breaker  2. delete last row
    interim_res_pd = process_lineBreaker(interim_res_pd)

    # CSV file Converting
    df_final_convertion(interim_res_pd, path_result)

    # Color converting
    color_assign_web_run(path_result)
    threshold_assigning_csv(path_result)
    res = json_run(sequence_set, path_result)
    return res


if __name__ == '__main__':
    # 储存写出表格的地址
    path_result = ''
    # run(path_result, 'txt Input/H-NOX (true).txt')
