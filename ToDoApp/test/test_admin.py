# ============================================================
#                           IMPORTS
# ============================================================
from starlette import status

from .utils import *
from ..routers.admin import get_current_user, get_db
from ..models import ToDos


# ============================================================
#                    DEPENDENCY OVERRIDES
# ============================================================
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


# ============================================================
#                    TESTS – ADMIN READ
# ============================================================
def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 1

    todo = data[0]
    assert todo["title"] == "Learn to code!"
    assert todo["description"] == "Need to learn everyday!"
    assert todo["priority"] == 5
    assert todo["complete"] is False
    assert todo["owner_id"] == 1


# ============================================================
#                    TESTS – ADMIN DELETE
# ============================================================
def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(ToDos).filter(ToDos.id == 1).first()
    assert model is None


def test_admin_delete_todo_not_found(test_todo):
    response = client.delete("/admin/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "ToDo not found"}
