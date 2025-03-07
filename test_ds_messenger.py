import pytest
import ds_messenger as dsm

def test_DirectMessenger_init():
    dm_obj = dsm.DirectMessenger()
    assert dm_obj.token == None
    assert dm_obj.dsp_conn == None
    assert dm_obj.dsuserver == None
    assert dm_obj.username == None
    assert dm_obj.password == None

    dm_obj.dsuserver = "127.0.0.1"
    dm_obj.username = "testingdm"
    dm_obj.password = "using unittest"

    assert isinstance(dm_obj, dsm.DirectMessenger)
    assert dm_obj.dsuserver == "127.0.0.1"
    assert dm_obj.username == "testingdm"
    assert dm_obj.password == "using unittest"

def test_start_session():
    dm_obj = dsm.DirectMessenger("127.0.0.1", "testingdm", "using unittest")
    assert isinstance(dm_obj, dsm.DirectMessenger)
    assert dm_obj.token == None
    assert dm_obj.dsp_conn == None

    welcome_message = dm_obj.start_session()
    assert welcome_message in ('Welcome back, testingdm!', 'Welcome to ICS32 Distributed Social, testingdm!')
    assert dm_obj.token != None
    assert dm_obj.dsp_conn != None
    dm_obj._close_socket()

def test_join_exceptions():
    # Missing username
    no_user_dm_obj = dsm.DirectMessenger()
    assert no_user_dm_obj.username == None
    assert no_user_dm_obj._join() == False

    # Missing password
    no_pwd_dm_obj = dsm.DirectMessenger()
    no_pwd_dm_obj.username = "NoPassword"
    assert no_pwd_dm_obj.password == None
    assert no_pwd_dm_obj._join() == False

    # Server error messages (invalid password)
    dm_test_obj_1 = dsm.DirectMessenger("127.0.0.1", "testingdm", "incorrectpassword")
    assert dm_test_obj_1._init_socket() == True
    assert dm_test_obj_1._join() == False

    # dsp.DSProtocolError (missing ds_conn)
    dm_test_obj_3 = dsm.DirectMessenger("127.0.0.1", "someuser", "BOOM")
    assert dm_test_obj_3._join() == False

def test_init_socket_exceptions(): #questions about ConnectionRefusedError and dsp.DSProtocolError
    # dsuserver is None
    dm_test_obj_4 = dsm.DirectMessenger()
    assert dm_test_obj_4.dsuserver == None
    assert dm_test_obj_4._init_socket() == False

    # dsuserver is an int
    dm_test_obj_4.dsuserver = 1232345
    assert dm_test_obj_4._init_socket() == False

    # dsuserver is "badaddress"
    dm_test_obj_4.dsuserver = "badaddress"
    assert dm_test_obj_4._init_socket() == False

def test_send():
    dm_test_obj_1 = dsm.DirectMessenger("127.0.0.1", "testingdm", "using unittest")

    # establishing a user to send to
    dm_test_obj_2 = dsm.DirectMessenger("127.0.0.1", "temp_user", "temp_password")
    dm_test_obj_2.start_session()
    dm_test_obj_2._close_socket()

    # sending message before joining (triggers dsp.DSProtocolError)
    is_ok = dm_test_obj_1.send("Hello temp_user!", "temp_user")
    assert is_ok == False

    # join then send message
    dm_test_obj_1.start_session()
    is_ok = dm_test_obj_1.send("Hello temp_user!", "temp_user")
    assert is_ok == True

def test_retrieve_new():
    dm_test_obj_2 = dsm.DirectMessenger("127.0.0.1", "temp_user", "temp_password")

    # getting inbox before joining (triggers dsp.DSProtocolError)
    inbox = dm_test_obj_2.retrieve_new()
    assert inbox == None

    # join and get inbox
    dm_test_obj_2.start_session()
    inbox = dm_test_obj_2.retrieve_new()
    assert type(inbox) == list
    if len(inbox) != 0:
        assert inbox[-1]['message'] == "Hello temp_user!"
        assert inbox[-1]['from'] == "testingdm"

def test_retrive_all():
    dm_test_obj_1 = dsm.DirectMessenger("127.0.0.1", "testingdm", "using unittest")
    dm_test_obj_2 = dsm.DirectMessenger("127.0.0.1", "temp_user", "temp_password")

    # getting inbox before joining (triggers dsp.DSProtocolError)
    inbox = dm_test_obj_1.retrieve_all()
    assert inbox == None

    # join and get inbox
    dm_test_obj_1.start_session()
    inbox = dm_test_obj_1.retrieve_all()
    assert type(inbox) == list and (len(inbox) == 0 or len(inbox) > 0)

    # send message to dm_test_obj_1 then retrieve their inbox
    dm_test_obj_2.start_session()
    is_sent = dm_test_obj_2.send("Hello to you too, testingdm", "testingdm")
    assert is_sent == True

    dm_test_obj_1.start_session()
    inbox = dm_test_obj_1.retrieve_all()
    assert type(inbox) == list and len(inbox) > 0
    assert inbox[-1]['message'] == "Hello to you too, testingdm"
    assert inbox[-1]['from'] == "temp_user"

def test_get_inbox_exception():
    dm_test_obj_1 = dsm.DirectMessenger("127.0.0.1", "testingdm", "using unittest")
    dm_test_obj_1.start_session()
    # reassigning token to get error message from server
    dm_test_obj_1.token = "badtoken"
    inbox = dm_test_obj_1.retrieve_all()
    assert inbox == None

def test_get_response_exception():
    dm_test_obj_1 = dsm.DirectMessenger("127.0.0.1", "testingdm", "using unittest")
    dm_test_obj_1.start_session()
    dm_test_obj_1.send("A message to a non-existent user", "A non-existent user")

if __name__ == "__main__":
    test_DirectMessenger_init()
    test_start_session()
    test_join_exceptions()
    test_init_socket_exceptions()
    test_send()
    test_get_response_exception()
    test_retrieve_new()
    test_retrive_all()
    test_get_inbox_exception()
