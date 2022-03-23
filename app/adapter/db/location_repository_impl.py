import typing

from app.common import exception
from app.domain.repository import location_repository
from app.domain import model as domain_model
from app.adapter.db import sql_db
from app.adapter.db import model as sql_model
from app.adapter.db import location_mapper


class LocationRepositoryImpl(location_repository.LocationRepository):

    def __init__(self) -> None:
        self.db = sql_db.get_db()

    def list(
        self, device_id=None
    ) -> typing.List[domain_model.Location]:
        if device_id:

            found_locations = self.db.query(
                sql_model.Location
            ).filter(
                sql_model.Location.device_id == device_id
            ).all()

        else:
            found_locations = self.db.query(sql_model.Location).all()

        locations = [
            location_mapper.to_domain_model(location)
            for location in found_locations
        ]
        return locations

    def create(
        self, locations: typing.List[domain_model.Location]
    ) -> typing.List[int]:

        sql_locations = [
            location_mapper.to_sql_model(location) for location in locations
        ]

        for l in sql_locations:
            self.db.add(l)

        self.db.commit()

        for l in sql_locations:
            self.db.refresh(l)
            yield l.id
