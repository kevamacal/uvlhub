import pytest
from sqlalchemy import delete, func, select
from app.modules.auth.models import User
from app.modules.conftest import login, logout
from app import db
from app.modules.notepad.models import Notepad
from app.modules.profile.models import UserProfile


@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    for module testing (por example, new users)
    """
    with test_client.application.app_context():
        user_test = User(email="user@example.com", password="test1234")
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.commit()

    yield test_client
    

def test_list_empty_notepad_get(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get("/notepad")
    assert response.status_code == 200, "The notepad page could not be accessed."
    assert b"You have no notepads." in response.data, "The expected content is not present on the page"

    logout(test_client)
    
    
def test_create_notepad(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."
    
    response = test_client.post(
        '/notepad/create',
        data={
            'title': 'Test de prueba',
            'body': 'Contenido de prueba'},
        follow_redirects=True
    )
    assert response.status_code == 200, "La creación del notepad no devolvió 200."


    user = User.query.filter_by(email="user@example.com").first()
    assert user is not None, "Usuario de prueba no encontrado en la BD."

    new_notepad = Notepad.query.filter_by(title="Test de prueba", user_id=user.id).first()
    assert new_notepad is not None, "No se creó el Notepad en la base de datos."
    assert new_notepad.body == "Contenido de prueba"


def test_edit_notepad(test_client):
 
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    user = User.query.filter_by(email="user@example.com").first()
    notepad = Notepad(title="Test de prueba", body="Descripción de prueba", user_id=user.id)
    db.session.add(notepad)
    db.session.commit()
    
    get_resp = test_client.get(f'/notepad/edit/{notepad.id}')
    assert get_resp.status_code == 200
    
    response = test_client.post(
        f"/notepad/edit/{notepad.id}",
        data={
            "title": "Test de prueba editado",
            "body": "Descripción de prueba editada",
        },
        follow_redirects=True,
    )
    
    assert response.status_code == 200, f"La edición falló. Código: {response.status_code}"
    
    
def test_show_notepad_byId(test_client):
    
    login_response = login(test_client, "user@example.com", "test1234")     
    assert login_response.status_code == 200, "Login was unsuccessful."

    user = User.query.filter_by(email="user@example.com").first()
    notepad = Notepad(title="Prueba", body="Datos de prueba", user_id=user.id)
    db.session.add(notepad)
    db.session.commit()
    
    response = test_client.get(f"/notepad/{notepad.id}")
    
    assert response.status_code == 200, "The notepad display page could not be accessed."
    

def test_delete_notepad(test_client):
    
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."


    user = User.query.filter_by(email="user@example.com").first()
    notepad = Notepad(title="Borrar", body="Borrar", user_id=user.id)
    db.session.add(notepad)
    db.session.commit()

    response = test_client.post(f"/notepad/delete/{notepad.id}", follow_redirects=True)

    assert response.status_code == 200, "The notepad deletion page could not be accessed."
    assert Notepad.query.get(notepad.id) is None
      
      