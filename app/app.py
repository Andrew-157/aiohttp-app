from aiohttp import web
import aiohttp_jinja2
import jinja2
import base64
import random
import string

users = {
    1: {'user_id': 1, 'username': 'Jack', 'age': 25, 'password': 'password_jack'},
    2: {'user_id': 2, 'username': 'John', 'age': 22, 'password': 'password_john'}
}

user_sessions = {}


def generate_token():

    letters = string.ascii_lowercase
    token = ''.join(random.choice(letters) for i in range(16))

    return token


@web.middleware
async def check_authz(request, handler):

    print("Before Authz")
    response = await handler(request)
    print("After Authz")
    return response


async def autenticate(request):

    creds_raw = request.headers['Authorization']
    creds_encoded = creds_raw.split(' ')[1]
    creds_decoded = base64.b64decode(creds_encoded).decode()
    username, password = creds_decoded.split(':')

    print(f"Authenticating user {username}...")

    for user in users.values():
        if username == user['username'] and password == user['password']:

            print("Authenticated...")

            token = generate_token()
            user_sessions[username] = token

            return web.json_response({'token': token})

    return web.json_response({'error': 'invalid credentials'}, status=401)


async def get_users(request):

    print("Get users handler")
    if 'username' in request.query:
        for user_id, user in users.items():
            if request.query['username'] == user['username']:
                return web.json_response(user)

    return web.json_response(users)


@aiohttp_jinja2.template('user.html')
async def get_user(request):

    print("Get user handler")
    print(request)
    user_id = int(request.match_info['user_id'])
    user = users[user_id]

    return {'user': user}


async def create_user(request):

    print("Create user handler")
    user = await request.json()
    user_id = user['user_id']

    if user_id in users:
        return web.json_response({'error': 'user already exists'}, status=409)

    users[user_id] = user

    return web.json_response(user)


async def update_user(request):

    print("Update user handler")
    user_id = int(request.match_info['user_id'])
    user = await request.json()
    users[user_id] = user

    return web.json_response(user)


async def delete_user(request):

    print("Delete user handler")
    user_id = int(request.match_info['user_id'])
    users.pop(user_id)

    return web.Response()


app = web.Application(middlewares=[check_authz])


aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(
    'D:\\projects\\aiohttp-app\\app\\templates'))


app.add_routes([web.post('/authenticate', autenticate),
                web.get('/users', get_users),
                web.post('/users', create_user),
                web.get('/users/{user_id}', get_user),
                web.put('/users/{user_id}', update_user),
                web.delete('/users/{user_id}', delete_user)])


if __name__ == '__main__':
    web.run_app(app)
