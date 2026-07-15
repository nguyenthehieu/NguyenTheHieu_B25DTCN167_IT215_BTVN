from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base

package_truck = Table(
    "package_truck",
    Base.metadata,
    Column("package_id", Integer, ForeignKey("packages.id"), primary_key=True),
    Column("truck_id", Integer, ForeignKey("trucks.id"), primary_key=True)
)