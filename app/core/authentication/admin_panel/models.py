from sqladmin import ModelView

from app.core.database.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.first_name, User.is_superuser]
