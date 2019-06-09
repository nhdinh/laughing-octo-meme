from test.utils.assertions import assert_json_response, assert_header_value


class TestApplication:
    def test_app_should_return_code_200(self, test_client):
        response = test_client.get('/')
        assert response.status_code == 200

    def test_app_should_return_data_in_json(self, test_client):
        response = test_client.get('/')
        assert_header_value('Content-Type', 'application/json', response.headers)

    def test_app_should_return_hello_world(self, test_client):
        response = test_client.get('/')
        assert_json_response({'hello': 'world'}, response)
