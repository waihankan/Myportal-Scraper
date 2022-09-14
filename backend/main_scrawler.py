#!/usr/bin/python3
"""
   Grab info from html and archive it both for one term or all past terms
"""


from fetch_data import FetchDataRequests

fetcher = FetchDataRequests()
# fetcher.archive_all_past_terms()
fetcher.update_current_term("202322")  # archive 2022 Fall term
