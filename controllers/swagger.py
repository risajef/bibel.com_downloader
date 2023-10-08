from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html

router = APIRouter(prefix='/docs', tags=["swagger"])

@router.get("")
def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Bible Analytics",
        swagger_ui_parameters={
            "tagsSorter": "alpha",
            "operationsSorter": "alpha",
            "docExpansion": "none",
        },
    )