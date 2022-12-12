from aiohttp import web

users = {
    1: {'user_id': 1, 'nickname': 'Jack', 'age': 25},
    2: {'user_id': 2, 'nickname': 'John', 'age': 22}
}


@web.middleware
async def check_authn(request, handler):

    print("Before Authn")
    response = await handler(request)
    print("After Authn")
    return response


@web.middleware
async def check_authz(request, handler):

    print("Before Authz")
    response = await handler(request)
    print("After Authz")
    return response


async def get_users(request):

    print("Get users handler")
    if 'nickname' in request.query:
        for user_id, user in users.items():
            if request.query['nickname'] == user['nickname']:
                return web.json_response(user)

    return web.json_response(users)


async def get_user(request):

    print("Get user handler")
    print(request)
    user_id = int(request.match_info['user_id'])
    user = users[user_id]

    return web.json_response(user)


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


app = web.Application(middlewares=[check_authn, check_authz])


app.add_routes([web.get('/users', get_users),
                web.post('/users', create_user),
                web.get('/users/{user_id}', get_user),
                web.put('/users/{user_id}', update_user),
                web.delete('/users/{user_id}', delete_user)])

if __name__ == '__main__':
    web.run_app(app)
