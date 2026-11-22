import json

from sqlalchemy import func
from sqlmodel import Session, select

from core.entities.unique_entity_id import UniqueEntityId
from domain.auth.enterprise.entities.user import User
from domain.cloudwise.enterprise.entities.cost_record import CostRecord
from domain.cloudwise.enterprise.value_objects.cost_aggregates import CostSeriesRow, CostSummary
from domain.cloudwise.enterprise.value_objects.cost_filters import CostFilters
from domain.runops.enterprise.entities.provision_request import ProvisionRequest
from domain.runops.enterprise.entities.template import Template
from domain.runops.enterprise.value_objects.provision_status import ProvisionStatus
from infra.database.sqlmodel.models import (
    DimAssinaturaModel,
    DimDataModel,
    DimServicoModel,
    FatoCustoModel,
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
        outputs=json.loads(model.outputs) if model.outputs else {},
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
            outputs=json.dumps(request.outputs),
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
        model.outputs = json.dumps(request.outputs)
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
            slug=template.slug,
            description=template.description,
        )
        self._session.merge(model)
        self._session.commit()


class SQLCostsRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    @staticmethod
    def _join(statement, filters: CostFilters):
        statement = (
            statement.select_from(FatoCustoModel)
            .join(DimDataModel, FatoCustoModel.data_id == DimDataModel.data_id)
            .join(DimServicoModel, FatoCustoModel.servico_id == DimServicoModel.servico_id)
            .join(
                DimAssinaturaModel,
                FatoCustoModel.assinatura_id == DimAssinaturaModel.assinatura_id,
            )
        )
        if filters.service:
            statement = statement.where(DimServicoModel.nome == filters.service)
        if filters.subscription_id:
            statement = statement.where(DimAssinaturaModel.codigo == filters.subscription_id)
        if filters.start:
            statement = statement.where(DimDataModel.data >= filters.start)
        if filters.end:
            statement = statement.where(DimDataModel.data <= filters.end)
        return statement

    async def list_records(self, filters: CostFilters) -> list[CostRecord]:
        statement = self._join(
            select(
                FatoCustoModel.id,
                FatoCustoModel.custo,
                FatoCustoModel.tags,
                DimDataModel.data,
                DimServicoModel.nome,
                DimAssinaturaModel.codigo,
            ),
            filters,
        ).order_by(DimDataModel.data, DimServicoModel.nome, DimAssinaturaModel.codigo)
        return [
            CostRecord(
                id=UniqueEntityId(id_),
                subscription_id=subscription,
                cost=cost,
                record_date=record_date,
                resource_type=service,
                tags=json.loads(tags),
            )
            for id_, cost, tags, record_date, service, subscription in self._session.exec(statement)
        ]

    async def series(self, filters: CostFilters, granularity: str) -> list[CostSeriesRow]:
        period = DimDataModel.ano_mes if granularity == "month" else DimDataModel.data
        statement = (
            self._join(
                select(period, DimServicoModel.nome, func.sum(FatoCustoModel.custo)), filters
            )
            .group_by(period, DimServicoModel.nome)
            .order_by(period)
        )
        return [
            CostSeriesRow(
                period=value if isinstance(value, str) else value.isoformat(),
                service=service,
                total=total,
            )
            for value, service, total in self._session.exec(statement)
        ]

    async def summary(self, filters: CostFilters) -> CostSummary:
        total, subscriptions = self._session.exec(
            self._join(
                select(
                    func.coalesce(func.sum(FatoCustoModel.custo), 0.0),
                    func.count(func.distinct(FatoCustoModel.assinatura_id)),
                ),
                filters,
            )
        ).one()
        top = self._session.exec(
            self._join(select(DimServicoModel.nome), filters)
            .group_by(DimServicoModel.nome)
            .order_by(func.sum(FatoCustoModel.custo).desc())
            .limit(1)
        ).first()
        return CostSummary(
            total_cost=total,
            top_service=top or "n/a",
            subscription_count=subscriptions,
        )


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
