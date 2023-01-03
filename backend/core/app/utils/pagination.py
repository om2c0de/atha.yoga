from typing import Optional, Type

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import QuerySet
from rest_framework.serializers import Serializer

from core.app.utils.request import APIRequest


def paginate(
    resource: Type[Serializer],
    data: QuerySet,
    request: APIRequest,
    context: Optional[dict] = None,
) -> dict:
    """
    Func for paginate data in api handlers
    """
    page = request.GET.get("page", 1)
    if context is None:
        context = {}
    try:
        per_page = (
            int(request.GET.get("per_page", settings.DEFAULT_PER_PAGE))
            or settings.DEFAULT_PER_PAGE
        )
    except ValueError:
        per_page = settings.DEFAULT_PER_PAGE
    if not page:
        return {"data": resource(data, many=True, context=context).data}

    if not data.query.order_by:
        if isinstance(getattr(data.model._meta, "ordering", None), list):
            data = data.order_by(*data.model._meta.ordering)
    paginator = Paginator(data, per_page)
    try:
        output = paginator.page(page)
    except PageNotAnInteger:
        output = paginator.page(1)
    except EmptyPage:
        output = paginator.page(paginator.num_pages)
    try:
        page = int(page)
    except ValueError:
        page = 1

    return {
        "data": resource(output, many=True, context=context).data,
        "links": {
            "current_page": page,
            "next_page": output.next_page_number() if output.has_next() else None,
            "prev_page": output.previous_page_number() if output.has_previous() else 1,
            "last_page": paginator.num_pages,
            "count": data.count(),
        },
    }
