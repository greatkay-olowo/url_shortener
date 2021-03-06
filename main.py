from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from nanoid import generate
import sqlite3
from validators import url

base_url = 'http://127.0.0.1:8000/'

app = FastAPI()


# welcome
@app.get('/')
async def welcome():
    return {
        'guide, make get requests to:': {
            'shorten_url': '/new/{url}. Url should include www',
            'redirect_shortened_url': '/{code}',
            'show_record': '/record/{code}'
        }
    }


# create a new record
@app.get('/new/{user_url}')
async def new_record(user_url: str):
    formated_url = 'http://' + user_url
    if url(formated_url):
        connection = sqlite3.connect('url.db')
        cursor = connection.cursor()
        last_data = cursor.execute(
            'SELECT * FROM urls WHERE user_url = ?', (user_url,)).fetchall()

        if not last_data:
            code = generate(size=5)
            connection = sqlite3.connect('url.db')
            cursor = connection.cursor()
            cursor.execute('INSERT INTO urls VALUES (?,?,?)', (code, user_url, 0))
            data = cursor.execute(
                'SELECT * FROM urls WHERE user_url = ?', (user_url,)).fetchall()
            connection.commit()
            return {'status': 'success', 'data': {'shortened_url': base_url + data[0][0]}}
        else:
            return {'status': 'already_taken', 'data': {'shortened_url': base_url + last_data[0][0], 'count': last_data[0][2]}}
    else:
        return {'status': 'error', 'data': {'message': 'Error while trying to shorten a non url.'}}


# redirect url
@app.get('/{code}')
async def get_user_url(code: str):
    connection = sqlite3.connect('url.db')
    cursor = connection.cursor()
    data = cursor.execute(
        'SELECT * FROM urls WHERE code = ?', (code,)).fetchall()
    if data:
        cursor.execute(
            "UPDATE urls SET hit = hit+1 WHERE code = ? ", (code,))
        connection.commit()
        return RedirectResponse(url='http://' + data[0][1])
    else:
        return {'status': 'error', 'data': {'message': 'not data available.'}}


# get a record
@app.get('/record/{code}')
async def get_record(code: str):
    connection = sqlite3.connect('url.db')
    cursor = connection.cursor()
    link = cursor.execute(
        'SELECT * FROM urls WHERE code = ?', (code,)).fetchall()
    connection.commit()
    if link:
        return {
            'status': 'success',
            'data': {
                    'shortened_url': base_url + link[0][0],
                    'user_url': link[0][1],
                    'counter': link[0][2],
                }}
    else:
        return {'status': 'error', 'data': {'message': 'record not found'}}
