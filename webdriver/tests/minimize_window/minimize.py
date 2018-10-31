from tests.support.asserts import assert_error, assert_success
from tests.support.helpers import is_fullscreen


def minimize(session):
    return session.transport.send(
        "POST", "session/{session_id}/window/minimize".format(**vars(session)))


def is_minimized(session):
    return session.execute_script("return document.hidden")


def test_no_browsing_context(session, closed_window):
    response = minimize(session)
    assert_error(response, "no such window")


def test_fully_exit_fullscreen(session):
    session.window.fullscreen()
    assert is_fullscreen(session)

    response = minimize(session)
    assert_success(response)
    assert not is_fullscreen(session)
    assert is_minimized(session)


def test_minimize(session):
    assert not is_minimized(session)

    response = minimize(session)
    assert_success(response)
    assert is_minimized(session)


def test_payload(session):
    assert not is_minimized(session)

    response = minimize(session)
    value = assert_success(response)
    assert isinstance(value, dict)

    value = response.body["value"]
    assert "width" in value
    assert "height" in value
    assert "x" in value
    assert "y" in value
    assert isinstance(value["width"], int)
    assert isinstance(value["height"], int)
    assert isinstance(value["x"], int)
    assert isinstance(value["y"], int)

    assert is_minimized(session)


def test_minimize_twice_is_idempotent(session):
    assert not is_minimized(session)

    first_response = minimize(session)
    assert_success(first_response)
    assert is_minimized(session)

    second_response = minimize(session)
    assert_success(second_response)
    assert is_minimized(session)
