import pytest

@pytest.mark.parametrize(
        "endpoint", [
            '/api/v1/blogs/posts/',
            '/api/v1/blogs/comments/',
            '/api/v1/blogs/tags/', 
            '/api/v1/blogs/categories/'
            ])
def test_blogs_endpoints(api_client, db, endpoint):
    response = api_client.get(endpoint)
    assert response.status_code == 200

@pytest.mark.parametrize(
        "endpoint", [
            '/api/v1/users/profiles/'
            ])
def test_profiles_endpoints(api_client, db, endpoint):
    response = api_client.get(endpoint)
    assert response.status_code == 200
