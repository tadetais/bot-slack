import os
import pandas as pd
from pandas import DataFrame

card_df: DataFrame

def init(card_id: int, user):
    global card_df
    df = filter_errors(update_data())
    card_df = df.loc[df["CARD"] == card_id]
    if card_df.empty:
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "<@{}> Não consegui localizar esse card, contate o suporte avançado!".format(user)
                }
            }
        ]
    message = format_info(user)
    del card_df
    return message

def format_info(user):
    return [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Segue o status do card #{}".format(get_data("CARD")),
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "<@{}>".format(user)
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Título:*\n{}".format(get_data("TITULO"))
                }
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Status:*\n{}".format(get_status()),
                }
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*CLIENTE:*\n{}".format(get_data("CLIENTE")),
                }
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*QUEM SOLICITOU:*\n{}".format(get_data("QUEM SOLICITOU")),
                }
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*CRIADO EM:*\n{}".format(format_dates("CRIADO EM")),
                }
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*INÍCIO DESENVOLVIMENTO:*\n{}".format(format_dates("INICIO DESENVOLVIMENTO")),
                }
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*INÍCIO VALIDAÇÃO:*\n{}".format(format_dates("INICIO VALIDACAO")),
                }
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*INÍCIO DEPLOY:*\n{}".format(format_dates("INICIO DEPLOY")),
                }
            ]
        },
    ]

def filter_errors(df: DataFrame):
    error_regex = "ERRO|ERRO_NF"
    return df.loc[df["LABELS"].str.contains(error_regex)]

def get_data(column_name: str):
    data = card_df.iat[0, card_df.columns.get_loc(column_name)]
    return "-" if data == "" else data

def get_status():
    return get_data("FILA").split(" | ")[0]

def format_dates(column_name: str):
    date = get_data(column_name)
    return pd.to_datetime(get_data(column_name)).strftime("%d/%m/%Y %H:%M:%S") if date != "-" else date

def update_data():
    df: DataFrame = pd.read_json(os.getenv("JSON_DATA_URL"))
    return df