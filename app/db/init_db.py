from sqlalchemy.orm import Session

from app.core.logger import logger

from app.constants.role import Role
from app.crud.crud_role import crud_role
from app.crud.crud_user import crud_user
from app.crud.crud_user_role import crud_user_role
from app.db.base import Base
from app.db.session import engine
from app.schemas.role import RoleCreate
from app.schemas.user import UserCreate
from app.schemas.user_role import UserRoleCreate


def init_db(db: Session) -> None:
    logger.debug("Initializing Database...")

    Base.metadata.create_all(bind=engine)

    # Create Roles [USER, ADMIN] if they don't exists
    user_role = crud_role.get_by_name(db, name=Role.USER["name"])
    if not user_role:
        user_role_in = RoleCreate(
            name=Role.USER["name"], description=Role.USER["description"]
        )
        crud_role.create(db, obj_in=user_role_in)

    admin_role = crud_role.get_by_name(db, name=Role.ADMIN["name"])
    if not admin_role:
        admin_role_in = RoleCreate(
            name=Role.ADMIN["name"], description=Role.ADMIN["description"]
        )
        crud_role.create(db, obj_in=admin_role_in)

    # Create default admin
    admin_user = crud_user.get_by_username(db, username="admin")
    if not admin_user:
        admin_user_in = UserCreate(
            username="admin",
            password="admin",
            full_name="Default System Admin",
        )
        admin_user = crud_user.create(db, obj_in=admin_user_in)
        admin_acc_role = crud_user_role.get_by_user_id(db, user_id=admin_user.id)
        if not admin_acc_role:
            role = crud_role.get_by_name(db, name=Role.ADMIN["name"])
            user_role_in = UserRoleCreate(user_id=admin_user.id, role_id=role.id)
            crud_user_role.create(db, obj_in=user_role_in)
