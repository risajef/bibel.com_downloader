from bs4 import BeautifulSoup
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import markdown as md


templates = Jinja2Templates(directory="templates")


def TemplateResponse(template_name: str, context: dict) -> HTMLResponse:
        assert template_name.endswith(".md")
        body = templates.TemplateResponse(template_name, context).body.decode("utf-8")
        html = md.markdown(body)
        html = f"<html><head></head><body>{html}</body></html>"
        soup = BeautifulSoup(html, features="html.parser")

        styles = soup.new_tag("link", rel="stylesheet", href="/static/css/markdown.css")
        head_tag = soup.find('head')
        head_tag.append(styles)
        return HTMLResponse(content=soup.prettify())