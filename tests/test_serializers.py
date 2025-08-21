import pytest

# def test(api_client, db):
#     response = api_client.post('/api/v1/auth/token/')
#     assert response.status_code == 400

def test_post_pagination_keys(api_client, db):
    response = api_client.get('/api/v1/blogs/posts/')
    print(response.data)
    assert response.status_code == 200
    
    assert 'count' in response.data
    assert 'next' in response.data
    assert 'previous' in response.data
    assert 'results' in response.data
    
    assert response.json()['results'] == []

    