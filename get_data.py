# -*- coding: utf-8 -*-
import psycopg2
from myclasses import Token, Document, plutchik


def get_data(raw_statement_id):

    db_name = "ams_article"
    db_user = "postgres"
    db_password = ""
    db_host = "localhost"
    db_port = 5432

    conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
    cur = conn.cursor()

    query = '''

    select t.value, t.modifier, se.idx sentence_idx, e.idx sentence_position
        from nlp.statement s
        join nlp.tag t on t.statement_id = s.statement_id
        left join nlp.sentity e on e.sentity_id = t.sentity_id
        left join nlp.sentence se on se.sentence_id = e.sentence_id
        where s.raw_statement_id = {0} and s.version_id = 1 and t.value like 'xw%'
        order by se.idx, e.idx


    '''

    doc = Document()

    cur.execute(query.format(raw_statement_id))
    result = cur.fetchall()

    current_token = (0, 0)

    for res in result:

        emotion, modifier, sentence_idx, sentence_position = res

        if current_token == (sentence_idx, sentence_position):
            tok.sentiment_score = get_sentiment_score(emotion, modifier, tok)

        else:
            current_token = (sentence_idx, sentence_position)
            tok = Token(sentence_position, sentence_idx)
            tok.sentiment_score = get_sentiment_score(emotion, modifier, tok)
            doc.add_token(tok)

    get_text_body_query = '''

    select prep_content
        from nlp.statement
        where raw_statement_id = {0}

    '''

    cur.execute(get_text_body_query.format(raw_statement_id))
    text_body = cur.fetchall()[0][0]

    cur.close()
    conn.close()

    return doc, text_body


def get_sentiment_score(emotion, modifier, tok):

    score = tok.sentiment_score

    emotions = {key: value for (value, key) in enumerate(plutchik)}
    score[emotions[emotion]] = modifier

    return score
