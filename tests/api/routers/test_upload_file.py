from fastapi.testclient import TestClient

from app.config import sttgs


upload_file_uri = (
    sttgs.get('API_PREFIX') + sttgs.get('UPLOAD_API_PREFIX') + '/file-to-guane'
)


def test_post_file_to_guane(app_client: TestClient):
    response = app_client.post(upload_file_uri)
    assert response.status_code == 200
    content = response.json()
    assert content['success'] is True
    assert content['remote_server_status_code'] == 201
    assert 'filename' in content['remote_server_response']
