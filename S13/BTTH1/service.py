from sqlalchemy.orm import Session
from models import MenuItem

def create_menu_item(db: Session, menu):
    try:
        check = db.query(MenuItem).filter(MenuItem.dish_code == menu.dish_code).first()

        if check:
            return None

        new_menu = MenuItem(
            dish_code=menu.dish_code,
            dish_name=menu.dish_name,
            calorie_count=menu.calorie_count,
            price=menu.price,
            status=menu.status
        )

        db.add(new_menu)
        db.commit()
        db.refresh(new_menu)
        return new_menu

    except Exception:
        db.rollback()
        raise

def get_all_menu_items(db: Session):
    return db.query(MenuItem).all()

def get_menu_item_by_id(db: Session, item_id: int):
    return db.query(MenuItem).filter(MenuItem.id == item_id).first()

def update_menu_item(db: Session, item_id: int, menu):
    try:
        item = db.query(MenuItem).filter(MenuItem.id == item_id).first()

        if not item:
            return None

        if menu.dish_code is not None:
            check = db.query(MenuItem).filter(MenuItem.dish_code == menu.dish_code,MenuItem.id != item_id).first()

            if check:
                return "duplicate"

        data = menu.model_dump(exclude_unset=True)

        if "dish_code" in data:
            item.dish_code = data["dish_code"]

        if "dish_name" in data:
            item.dish_name = data["dish_name"]

        if "calorie_count" in data:
            item.calorie_count = data["calorie_count"]

        if "price" in data:
            item.price = data["price"]

        if "status" in data:
            item.status = data["status"]

        db.commit()
        db.refresh(item)
        return item

    except Exception:
        db.rollback()
        raise

def delete_menu_item(db: Session, item_id: int):
    try:
        item = db.query(MenuItem).filter(MenuItem.id == item_id).first()

        if not item:
            return None

        db.delete(item)
        db.commit()
        return True

    except Exception:
        db.rollback()
        raise