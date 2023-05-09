import enum

from sqlalchemy import Column, BigInteger, Enum, VARCHAR, ForeignKey, Integer, Boolean, select
from sqlalchemy.orm import relationship, validates, sessionmaker

from app.db import CustomBaseModel, get_object
from app.db.user import User


# import re
# from bot.settings import EMAIL_REG_EXP, NAME_REG_EX


class GradeTypes(enum.Enum):
    """
    Grade type
    """
    TRAINEE = "trainee"
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"

    @classmethod
    def choices(cls):
        return [exp_type.value for exp_type in cls]


def get_humanize_profile_grade(grade: str) -> str:
    match grade:
        case GradeTypes.TRAINEE.value:
            return "Стажер"
        case GradeTypes.JUNIOR.value:
            return "Junior"
        case GradeTypes.MIDDLE.value:
            return "middle"
        case GradeTypes.SENIOR.value:
            return "senior"


# class WorkTypes(enum.Enum):
#     """
#     Work types
#     """
#
#     REMOTE = "remote"
#     PART_TIME = "part-time"
#     FULL_TIME = "full-time"
#
#     @classmethod
#     def choices(cls):
#         return [exp_type.value for exp_type in cls]


class WorkTypes(enum.Enum):
    """
    Work types
    """

    PART_TIME = "Частичная занятость"
    TRAINEE = "Стажировка"
    PROJECT = "Проектная работа"
    FULL_TIME = "Полная занятость"

    @classmethod
    def choices(cls):
        return [exp_type.value for exp_type in cls]


class Profile(
    CustomBaseModel,
):
    """
    Profile model
    """
    __tablename__ = "profiles"

    firstname = Column(VARCHAR(32))
    lastname = Column(VARCHAR(32))

    # email = Column(
    #     String(255),
    #     unique=True,
    #     server_default=text("''"),
    # )

    professional_role = Column(VARCHAR(32))

    grade = Column(Enum(*(
        type.value for type in GradeTypes
    ), name="grade"))

    work_type = Column(Enum(*(
        work_type.value for work_type in WorkTypes
    ), name="work_types"))

    region = Column(VARCHAR(32))

    salary_from = Column(Integer)
    salary_to = Column(Integer)

    ready_for_relocation = Column(Boolean, default=False)

    # telegram user id
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    user = relationship('User', uselist=False, back_populates='profile')

    # @validates("email")
    # def validate_email(self, key, address):
    #     """
    #     Email db validator
    #     :param key:
    #     :param address:
    #     :return:
    #     """
    #
    #     if re.match(EMAIL_REG_EXP, address):
    #         return address
    #     raise ValueError

    # @validates("firstname", "lastname")
    # def validate_name(self, key, name):
    #     """
    #     Firstname and lastname db validator
    #     :param name:
    #     :param key:
    #     :return:
    #     """
    #
    #     if re.match(NAME_REG_EXP, name):
    #         return name
    #     raise ValueError
    #
    @validates("salary_from", "salary_to")
    def validate_numbers(self, key, number_):
        """
        Firstname and lastname db validator
        :param number_:
        :param key:
        :return:
        """
        return int(number_)


async def get_profile_by_user_id(user_id, session):
    async with session() as session:
        db_response = (await session.execute(select(Profile).where(Profile.user_id == user_id))).one_or_none()
        if db_response:
            return db_response[0]
        return None


async def create_profile(
        user_id: int,
        session: sessionmaker
) -> Profile:
    user = await get_object(User, id_=user_id, session=session)
    async with session() as session_:
        async with session_.begin():
            profile = Profile(user_id=user_id)
            session_.add(profile)
            await session_.flush()
            user.profile = profile
            await session_.merge(user)
            await session_.merge(profile)
        return profile
