import json

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import uvicorn
from starlette import status
from starlette.staticfiles import StaticFiles

from app.db import create_async_engine, get_session_maker, Profile, update_object
from app.db.profile import create_profile, get_humanize_profile_grade, GradeTypes, WorkTypes
from app.settings import POSTGRES_URL
from db import get_profile_by_user_id

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

async_engine = create_async_engine(POSTGRES_URL)

with open('static/cities.json', 'r', encoding='utf-8') as f:
    cities = json.load(f)


@app.get("/profile/{id}")
async def profileform(request: Request, id: int):
    async_session_maker = await get_session_maker(async_engine)
    user_profile = await get_profile_by_user_id(user_id=id, session=async_session_maker)

    return templates.TemplateResponse("profileform.html",
                                      {"request": request, "user_profile": user_profile, "cities": cities,
                                       "grades": {grade: get_humanize_profile_grade(grade) for grade in
                                                  GradeTypes.choices()},
                                       "work_types": WorkTypes.choices(),
                                       })


@app.post("/profile/{id}", status_code=status.HTTP_201_CREATED)
async def profileform(id: int,
                      professional_role: str = Form(),
                      grade: str = Form(),
                      work_type: str = Form(),
                      region: str = Form(),
                      salary_from: int = Form(),
                      salary_to: int = Form(default=None),
                      ready_for_relocation: bool = Form(False)
                      ):
    data = {
        "professional_role": professional_role,
        "grade": grade,
        "work_type": work_type,
        "region": region,
        "salary_from": salary_from,
        "salary_to": salary_to,
        "ready_for_relocation": ready_for_relocation
    }

    async_session_maker = await get_session_maker(async_engine)

    profile = await get_profile_by_user_id(user_id=id, session=async_session_maker)

    if not profile:
        profile = await create_profile(user_id=id, session=async_session_maker)

    await update_object(Profile, profile.id, data, async_session_maker)

    return {'status': 'success',
            'data': data}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
