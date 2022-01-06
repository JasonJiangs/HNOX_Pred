#!/usr/bin/env python3
# coding=UTF-8
'''
Date: 2021-12-06 21:53:46
LastEditTime: 2021-12-06 23:08:48
Description: file content
'''

from app.HNOX_Pred.algorithm import *
import sys

# storing addresses of color and non color
noncolored_address = '\\result_noncolored.csv'


def main_func():

    lines = sys.stdin.read()

    # Split the sequence groups, return a set to store all sequences
    sequence_set = intersection(lines.upper())

    pure_sequence_set = []

    # Process multiple sequence one by one
    for i in range(len(sequence_set)):
        # get original sequence with header and analyzed sequence
        raw_seq = sequence_set[i]
        # Split the single sequence into head sequence and substance sequence (analyzed sequence)
        head, analyzed_sequence = header_recognition(raw_seq)
        pure_sequence_set.append(analyzed_sequence)
        analyzed_sequence = analyzed_sequence + '\n'  # fail-safe
        raw_output_template = main_process(head, analyzed_sequence, checklist_pd, raw_output_template)
    return raw_output_template, pure_sequence_set, sequence_set


# read txt.file as input
def main_func_txt_input(f_path, raw_output_template):

    f = open(f_path)
    lines = f.read()

    # Split the sequence groups, return a set to store all sequences
    sequence_set = intersection(lines.upper())

    pure_sequence_set = []

    # Process multiple sequence one by one
    for i in range(len(sequence_set)):
        # get original sequence with header and analyzed sequence
        raw_seq = sequence_set[i]
        # Split the single sequence into head sequence and substance sequence (analyzed sequence)
        head, analyzed_sequence = header_recognition(raw_seq)
        pure_sequence_set.append(analyzed_sequence)
        analyzed_sequence = analyzed_sequence + '\n'  # fail-safe
        raw_output_template = main_process(head, analyzed_sequence, checklist_pd, raw_output_template)
    return raw_output_template, pure_sequence_set, sequence_set


# File Converting for Final CSV file output
def df_final_convertion(df, path_result):
    # create dataframe for final result
    final_pd = pd.DataFrame({
        'Hit-No': [],
        'Position': [],
        'H-NOX Sequence': [],
        'H-NOX Hydrophobicity': [],
        'H-NOX Molecular Weight': [],
        'H-NOX Isoelectric Point': [],
        'H-NOX Mean': []
    })
    for i in range(len(df)):
        if df.iloc[i, 0] == 0:
            final_pd.loc[len(final_pd)] = ['', '', '', '', '', '', '']
            final_pd.iloc[len(final_pd) - 1, 0] = df.iloc[i, 8]
        # assign header
        if df.iloc[i, 0] == 1:
            final_pd.loc[len(final_pd)] = ['', '', '', '', '', '', '']
            final_pd.iloc[len(final_pd) - 1, 0] = df.iloc[i, 8]
        # Initialize one row
        final_pd.loc[len(final_pd)] = [0, '', '', 0, 0, 0, 0]
        # combine position
        cpos = str(int(df.iloc[i, 1])) + '-' + str(int(df.iloc[i, 2]))
        # assign values
        final_pd.iloc[len(final_pd) - 1, 0] = df.iloc[i, 0]
        final_pd.iloc[len(final_pd) - 1, 1] = cpos
        final_pd.iloc[len(final_pd) - 1, 2] = df.iloc[i, 3]
        final_pd.iloc[len(final_pd) - 1, 3] = df.iloc[i, 4]
        final_pd.iloc[len(final_pd) - 1, 4] = df.iloc[i, 5]
        final_pd.iloc[len(final_pd) - 1, 5] = df.iloc[i, 6]
        final_pd.iloc[len(final_pd) - 1, 6] = df.iloc[i, 7]
    # Store final result
    final_pd.to_csv(path_result + noncolored_address, sep=',', index=False, header=True)
