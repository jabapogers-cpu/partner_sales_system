from sqlalchemy.orm import Session


def test_get_db_yields_session_and_closes_it():
    from database import get_db

    gen = get_db()
    session = next(gen)

    assert isinstance(session, Session)

    gen.close()