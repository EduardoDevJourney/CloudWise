import json
from datetime import date

from sqlmodel import Session, select

from core.entities.unique_entity_id import UniqueEntityId
from domain.cloudwise.enterprise.entities.cost_dim import CostDim
from domain.cloudwise.enterprise.entities.cost_record import CostRecord
from domain.auth.enterprise.entities.user import User
from domain.runops.enterprise.entities.provision_request import ProvisionRequest
from domain.runops.enterprise.entities.template import Template
from domain.runops.enterprise.value_objects.provision_status import ProvisionStatus
from infra.database.sqlmodel.models import (
    CostDimModel,
    CostRecordModel,
    ProvisionRequestModel,
    TemplateModel,
    UserModel,
)


def _to_provision_request(model: ProvisionRequestModel) -> ProvisionRequest:
    return ProvisionRequest(
        id=UniqueEntityId(model.id),
        user_id=model.user_id,
        template_id=model.template_id,
        status=ProvisionStatus(model.status),
        request_data=json.loads(model.request_data),
        error_message=model.error_message,
        created_at=model.created_at,
        started_at=model.started_at,
        finished_at=model.finished_at,
    )


def _to_template(model: TemplateModel) -> Template:
    return Template(
        id=UniqueEntityId(model.id),
        name=model.name,
        params_schema=json.loads(model.params_schema),
        azure_sku=model.azure_sku,
        slug=model.slug,
        description=model.description or "",
    )


class SQLProvisionRequestsRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    async def create(self, request: ProvisionRequest) -> None:
        model = ProvisionRequestModel(
            id=str(request.id),
            user_id=request.user_id,
            template_id=request.template_id,
            status=request.status.value,
            request_data=json.dumps(request.request_data),
            error_message=request.error_message,
            created_at=request.created_at,
            started_at=request.started_at,
            finished_at=request.finished_at,
        )
        self._session.add(model)
        self._session.commit()

    async def save(self, request: ProvisionRequest) -> None:
        model = self._session.get(ProvisionRequestModel, str(request.id))
        if model is None:
            await self.create(request)
            return
        model.status = request.status.value
        model.error_message = request.error_message
        model.started_at = request.started_at
        model.finished_at = request.finished_at
        model.request_data = json.dumps(request.request_data)
        self._session.add(model)
        self._session.commit()

    async def find_by_id(self, provision_id: str) -> ProvisionRequest | None:
        model = self._session.get(ProvisionRequestModel, provision_id)
        return _to_provision_request(model) if model else None

    async def list_all(self) -> list[ProvisionRequest]:
        models = self._session.exec(select(ProvisionRequestModel)).all()
        return [_to_provision_request(m) for m in models]


class SQLTemplatesRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    async def find_by_id(self, template_id: str) -> Template | None:
        model = self._session.get(TemplateModel, template_id)
        if model is None:
            model = self._session.exec(
                select(TemplateModel).where(TemplateModel.slug == template_id)
            ).first()
        return _to_template(model) if model else None

    async def list_all(self) -> list[Template]:
        models = self._session.exec(select(TemplateModel)).all()
        return [_to_template(m) for m in models]

    async def save(self, template: Template) -> None:
        model = TemplateModel(
            id=str(template.id),
            name=template.name,
            params_schema=json.dumps(template.params_schema),
            azure_sku=template.azure_sku,
            slug=template.slug or str(template.id),
            description=template.description,
        )
        self._session.merge(model)
        self._session.commit()


class SQLCostRecordsRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    async def list_all(self) -> list[CostRecord]:
        models = self._session.exec(select(CostRecordModel)).all()
        return [
            CostRecord(
                id=UniqueEntityId(m.id),
                subscription_id=m.subscription_id,
                cost=m.cost,
                record_date=m.record_date,
                resource_type=m.resource_type,
                tags=json.loads(m.tags),
            )
            for m in models
        ]

    async def save_many(self, records: list[CostRecord]) -> None:
        for record in records:
            self._session.merge(
                CostRecordModel(
                    id=str(record.id),
                    subscription_id=record.subscription_id,
                    cost=record.cost,
                    record_date=record.record_date,
                    resource_type=record.resource_type,
                    tags=json.dumps(record.tags),
                )
            )
        self._session.commit()


class SQLCostDimsRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    async def list_all(self) -> list[CostDim]:
        models = self._session.exec(select(CostDimModel)).all()
        return [
            CostDim(
                id=UniqueEntityId(m.id),
                record_date=m.record_date,
                category=m.category,
                service_name=m.service_name,
            )
            for m in models
        ]

    async def save_many(self, dims: list[CostDim]) -> None:
        for dim in dims:
            self._session.merge(
                CostDimModel(
                    id=str(dim.id),
                    record_date=dim.record_date,
                    category=dim.category,
                    service_name=dim.service_name,
                )
            )
        self._session.commit()


class SQLUsersRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    @staticmethod
    def _to_user(m: UserModel) -> User:
        return User(id=m.id, email=m.email, role=m.role, active=m.active, created_at=m.created_at)

    async def find_by_id(self, user_id: str) -> User | None:
        model = self._session.get(UserModel, user_id)
        return self._to_user(model) if model else None

    async def list_all(self) -> list[User]:
        return [self._to_user(m) for m in self._session.exec(select(UserModel)).all()]

    async def save(self, user: User) -> None:
        self._session.merge(
            UserModel(
                id=user.id,
                email=user.email,
                role=user.role,
                active=user.active,
                created_at=user.created_at,
            )
        )
        self._session.commit()
