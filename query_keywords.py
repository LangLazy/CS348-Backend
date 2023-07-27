import mysql.connector
import os
import logging

from db import database

def query_keywords(queryParams: dict[dict[str]]):
    print("hellp")
    db = database()
    author_params = []
    other_params = []
    for query in queryParams.values():
        if query['field'] == "Author":
            value = query['value'].strip()
            if query['equality'] == "Exact":
                author_params.append(value)
            elif query['equality'] == "Contains":
                author_params.append("%" + value + "%")
        else:
            values = [x.strip(' ') for x in query["value"].split(",")]
            if query['equality'] == "Contains":
                values = ["%" + x + "%" for x in values]
            other_params.extend(values)
    print(author_params)
    print(other_params)
    params = author_params.copy()
    params.extend(other_params)
    print(params)
    query = generate_keyword_query_string(queryParams)
    result = db.execute(query, params)
    output = []
    
    for row in result:
        output.append(row)
    
    return output

def generate_keyword_query_string(queryParams):
    first_join = "SELECT w.paper_id, group_concat(a.author_name) as Authors, " + \
                "group_concat(a.author_id) as Authors_id " + \
                "FROM author a NATURAL JOIN wrote w"
    if len(queryParams) == 0:
        first_join += " GROUP BY w.paper_id"
        second_join = "SELECT * FROM paper NATURAL JOIN keywords Group by paper_id"
        return ("SELECT * FROM ({}) X NATURAL JOIN ({}) Y".format(first_join, second_join))
    author_params = ""
    query_params = ""
    for query in queryParams.values():
        if query['value'] == "": continue
        equality = determine_equality(query["equality"], query["boolean"])
        if query["field"] == "Author": 
            if author_params == "": author_params += "a.author_name " + equality + " %s"
            elif query["boolean"] == "NOT": 
                author_params += " AND a.author_name " + equality + " %s"
            elif query["boolean"] != "None": 
                author_params += " " + query["boolean"] + " a.author_name " + equality + " %s"
        else:
            if query["field"] == "Keywords": 
                attribute = "word"
                table = "t"
            elif query["field"] == "Title": 
                attribute = "title"
                table = "p"
            if query_params == "": pass
            elif query["boolean"] == "AND" or query["boolean"] == "NOT":
                query_params += " AND "
            elif query["boolean"] == "OR":
                query_params += " OR "
            value = [x.strip(' ') for x in query["value"].split(",")]
            formatted_portion = [table + "." + attribute + " " + equality + " %s"] * len(value)
            joined_Operator = query["boolean"] if query["boolean"] != "None" else "AND"
            query_params += (" " + joined_Operator + " ").join(formatted_portion)
    if author_params != "":
        first_join += " WHERE " + author_params
    first_join += " GROUP BY w.paper_id"

    where_string = ""
    if query_params != "":
        where_string = "WHERE {} ".format(query_params)

    # I really tried to make this readable
    query = ("SELECT * FROM " + \
             "({}) as X ".format(first_join) +\
             "NATURAL JOIN " +\
             "(SELECT paper_id, title, year, fos_name, n_citation, page_start, " +\
                "page_end, doc_type, lang, vol, issue, isbn, doi, url, abstract, " +\
                "group_concat(word) as Keywords FROM paper p NATURAL JOIN keywords t " +\
                where_string + " GROUP BY paper_id) as Y")
    print(query)
    return query

def determine_equality(equality, boolean):
    newEquality = "="
    if equality == "Contains": newEquality = "LIKE"
    if boolean == "NOT":
        if equality == "Exact": newEquality = "!" + newEquality
        elif equality == "Contains": newEquality = "NOT " + newEquality
    return newEquality

# field: queryField.KEYWORDS, value: "", boolean: booleanLogic.None

# query_keywords(
#     {
#         "1": {
#             "field": "Keywords",
#             "value": "hello",
#             "equality": "Exact",
#             "boolean": "None"
#         },
#         "2": {
#             "field": "Author",
#             "value": "this",
#             "equality": "Exact",
#             "boolean": "AND"
#         },
#         "3": {
#             "field": "Title",
#             "value": "temp, something, great",
#             "equality": "Contains",
#             "boolean": "AND"
#         },
#         "4": {
#             "field": "Keywords",
#             "value": "cs",
#             "equality": "Exact",
#             "boolean": "NOT"
#         }
#     }
# )