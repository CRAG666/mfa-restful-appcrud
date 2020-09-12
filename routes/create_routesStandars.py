from routes.api_template import MethodsApi


def create_routes(**kwargs):
    """Create routes standars
    Args:
        **kwargs: Arbitrary keyword arguments.

    Keyword Args:
        blueprint (object): blueprint or object flask app
        noun (str): noun to create endpoints and method view name.
        table (db.Model): sqlalchemy model.
        table_schema (ma.Schema): marshmallow schema.
        login_endpoint (bool, optional): Create login endpoint. Defaullt to False.
        customize_login (dict, optional): receives configuration parameters to login. Defaults to None.
        endpoints (list, optional): List to endpoints ([['/url', ['GET']]]). Default generate endpoints with noun.
    Examples:
        basic usage:
            create_routes(
                table=SomeModel,
                table_schema=SomeSchema,
                blueprint=some_blueprint,
                noun="v1/somenoun",
                login_endpoint=True)

        customize endpoints:
            create_routes(
                table=SomeModel,
                table_schema=SomeSchema,
                blueprint=some_blueprint,
                noun="v1/somenoun",
                endpoints=[['/api/v1/somenoun', ['GET','POST'])
    """
    view_func = MethodsApi.as_view(
        f"{kwargs.get('noun')}_api",
        kwargs.get('table'),
        kwargs.get('table_schema'),
        kwargs.get('customize_login')
    )

    endpoints = kwargs.get(
        'endpoints',
        get_endpoints(
            kwargs.get('noun'),
            kwargs.get('login_endpoint', False)))

    for i in endpoints:
        kwargs.get('blueprint').add_url_rule(
            i[0],
            methods=i[1],
            view_func=view_func)


def get_endpoints(noun: str, login: bool) -> list:
    endpoint_list = [
        [f'/api/{noun}/', ['POST', 'GET']],
        [f'/api/{noun}/<int:id>', ['GET', 'PUT', 'DELETE']]]
    if login:
        endpoint_list.insert(0, [f'/api/{noun}/login', ['POST']])
    return endpoint_list
