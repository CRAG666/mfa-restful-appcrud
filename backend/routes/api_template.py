from flask import jsonify, request, abort
from flask.views import MethodView
import jwt
from flask import current_app as app
import datetime
from helpers.validations import token_required, validate_json
from models import ma, db
from models.Login import LoginSchema


class MethodsApi(MethodView):
    """ Class for control to endpoints """
    def __init__(self, table: db.Model, table_schema: ma.Schema, **kwargs):
        """Contructor

        Args:
            table (db.Model): sqlalchemy model
            table_schema (ma.Schema): marshmallow schema
        Keyword Args:
            schema (ma.Schema): marshmallow scheme to validate the login. Defaults to LoginSchema
            field_search (str): field name to search in db
            password_field_name (str): field name for password
            key_encrypt (str): key to create jwt token. Default to app.config['SECRET_KEY']
            post_action (tuple): Receive a tuple with two elements. The first is the function to be executed after the creation of the token, the second corresponds to the parameters received by the function in str. Default to False
        """
        self.customize_login = kwargs
        self.Table = table
        self.Result = table_schema()
        self.Results = table_schema(many=True)
        self.login = validate_json(
            kwargs.get(
                "schema",
                LoginSchema)())(self.login)
        self.put = validate_json(self.Result)(self.put)
        self.add = validate_json(self.Result)(self.add)

    @token_required()
    def get(self, current_user, id=None):
        """Method http GET

        Args:
            current_user (object): Contains the data of the logged in user
            id (int, optional): ID registration. Defaults to None.

        Returns:
            json: many or one registry
            http error: corresponding code http error
        """
        if id:
            return self.get_by_id(current_user, id)

        elif 'page' in request.args.keys():
            page = int(request.args.get(
                'page',
                type=int,
                default=1))
            per_page = int(request.args.get(
                'size',
                type=int,
                default=10))
            return self.get_pagination(page, per_page, current_user)

        return self.get_all(current_user)

    def get_all(self, current_user: object):
        registrys_list = self.Table.all(
            self.Table,
            current_user)
        return jsonify({"results": self.Results.dump(registrys_list)})

    def get_by_id(self, current_user: object, id: int):
        one_registry = self.Table.get_by_id(self.Table, id, current_user)
        return self.Result.jsonify(one_registry)

    def get_pagination(self, page: int, per_page: int, current_user: object):
        paginar = self.Table.paginate(self.Table, page, per_page, current_user)
        return jsonify(
            {"results": self.Results.dump(paginar.items),
                "total-pages": paginar.pages})

    def post(self):
        """ Method http GET """
        rute = str(request.url_rule)
        if rute.find('login') != -1:
            return self.login()
        return self.add()

    def login(self):
        """Create new session and execute post action(optional)

        Returns:
            token (json): jwt
        """
        auth = request.json
        search_field_name = self.customize_login.get(
            'field_search',
            "email")
        search_field_value = auth[search_field_name]
        search_dict = {search_field_name: search_field_value}

        user = self.Table.query.filter_by(**search_dict).first()

        if not user:
            abort(401)

        password_field_name = self.customize_login.get(
            'password_field_name',
            "password")

        password = auth[password_field_name]

        if user.compare_passwords(password):
            token = jwt.encode({
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            }, self.customize_login.get('key_encrypt', app.config['SECRET_KEY']))
            action = self.customize_login.get('post_action', False)
            if action:
                exec(f'action[0]({action[1]})')
            return jsonify({'token': token.decode('UTF-8')})
        abort(401)

    @token_required()
    def add(self, current_user):
        """ Add new record

        Args:
            current_user (object): Contains the data of the logged in user

        Returns:
            json: registry created
        """
        new_registry = self.Table(request.json, current_user)
        insert_correct_data = new_registry.save()
        if not insert_correct_data:
            return self.databse_err()
        return self.Result.jsonify(new_registry), 201

    @token_required()
    def put(self, current_user, id):
        """ Edit record

        Args:
            current_user (object): Contains the data of the logged in user
            id (int, optional): ID registration

        Returns:
            json: edited record
        """
        registry_update = self.Table.get_by_id(self.Table, id, current_user)
        registry_update.changes(request.json, current_user)
        update_correct_data = registry_update.save()
        if not update_correct_data:
            return self.databse_err("update")
        return self.Result.jsonify(registry_update)

    @token_required()
    def delete(self, current_user, id):
        """ Delete record

        Args:
            current_user (object): Contains the data of the logged in user
            id (int, optional): ID registration

        Returns:
            json: deleted record
        """
        registry_delete = self.Table.get_by_id(self.Table, id, current_user)
        deleted_data = registry_delete.delete(current_user)
        if not deleted_data:
            return self.databse_err("delete")
        return self.Result.jsonify(registry_delete)

    @staticmethod
    def databse_err(action: str = "insert") -> jsonify:
        return jsonify(
            {"Err": f"Error trying to {action} data"}), 409
