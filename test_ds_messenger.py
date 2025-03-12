'''
test_ds_messenger.py

Tests the functionality of ds_messenger.py. Line tests each function
in ds_messenger module. Does not test for server-related errors
(i.e. ConnectionRefusedError)

Stephanie Lee
stephl25@uci.edu

'''
import ds_messenger as dsm


def test_direct_messenger_init():
    '''
    Tests the instantiation of the DirectMessenger class.
    '''
    dm_obj = dsm.DirectMessenger()
    assert dm_obj.token is None
    assert dm_obj.dsp_conn is None
    assert dm_obj.dsuserver is None
    assert dm_obj.username is None
    assert dm_obj.password is None

    dm_obj.dsuserver = "127.0.0.1"
    dm_obj.username = "testingdm"
    dm_obj.password = "using unittest"

    assert isinstance(dm_obj, dsm.DirectMessenger)
    assert dm_obj.dsuserver == "127.0.0.1"
    assert dm_obj.username == "testingdm"
    assert dm_obj.password == "using unittest"


def test_start_session():
    '''
    Tests the start_session() function in the ds_messenger.py
    '''
    dm_obj = dsm.DirectMessenger("127.0.0.1", "testingdm", "using unittest")
    assert isinstance(dm_obj, dsm.DirectMessenger)
    assert dm_obj.token is None
    assert dm_obj.dsp_conn is None

    welcome_message = dm_obj.start_session()
    assert welcome_message in ('Welcome back, testingdm!',
                               'Welcome to ICS32 Distributed Social, testingdm!')
    assert dm_obj.token is not None
    assert dm_obj.dsp_conn is not None
    dm_obj.close_socket()

    dm_obj2 = dsm.DirectMessenger("badserver", "testingdm", "using pytest")
    assert isinstance(dm_obj2, dsm.DirectMessenger)
    assert dm_obj2.token is None
    assert dm_obj2.dsp_conn is None

    welcome_message = dm_obj2.start_session()
    assert welcome_message is False


def test_join_exceptions():
    '''
    Tests the _join() method exceptions are triggering correctly.
    '''
    # Missing username
    no_user_dm_obj = dsm.DirectMessenger()
    assert no_user_dm_obj.username is None
    assert no_user_dm_obj.join() is None

    # Missing password
    no_pwd_dm_obj = dsm.DirectMessenger()
    no_pwd_dm_obj.username = "NoPassword"
    assert no_pwd_dm_obj.password is None
    assert no_pwd_dm_obj.join() is None

    # Server error messages (invalid password)
    dm_test_obj_1 = dsm.DirectMessenger("127.0.0.1", "testingdm", "incorrectpassword")
    assert dm_test_obj_1.init_socket() is True
    assert dm_test_obj_1.join() is None

    # dsp.DSProtocolError (missing ds_conn)
    dm_test_obj_3 = dsm.DirectMessenger("127.0.0.1", "someuser", "BOOM")
    assert dm_test_obj_3.join() is None


def test_init_socket_exceptions():
    '''
    Tests the _init_socket exceptions are being triggered correctly.
    '''
    # dsuserver is None
    dm_test_obj_4 = dsm.DirectMessenger()
    assert dm_test_obj_4.dsuserver is None
    assert dm_test_obj_4.init_socket() is False

    # dsuserver is an int
    dm_test_obj_4.dsuserver = 1232345
    assert dm_test_obj_4.init_socket() is False

    # dsuserver is "badaddress"
    dm_test_obj_4.dsuserver = "badaddress"
    assert dm_test_obj_4.init_socket() is False


def test_send():
    '''
    Tests send() function of ds_messenger.py
    '''
    dm_test_obj_1 = dsm.DirectMessenger("127.0.0.1", "testingdm", "using unittest")

    # establishing a user to send to
    dm_test_obj_2 = dsm.DirectMessenger("127.0.0.1", "temp_user", "temp_password")
    dm_test_obj_2.start_session()
    dm_test_obj_2.close_socket()

    # sending message before joining (triggers dsp.DSProtocolError)
    is_ok = dm_test_obj_1.send("Hello temp_user!", "temp_user")
    assert is_ok is False

    # join then send message
    dm_test_obj_1.start_session()
    is_ok = dm_test_obj_1.send("Hello temp_user!", "temp_user")
    assert is_ok is True


def test_retrieve_new():
    '''
    Tests retrieve_new() function of ds_messenger.py
    '''
    dm_test_obj_2 = dsm.DirectMessenger("127.0.0.1", "temp_user", "temp_password")

    # getting inbox before joining (triggers dsp.DSProtocolError)
    inbox = dm_test_obj_2.retrieve_new()
    assert inbox is None

    # join and get inbox
    dm_test_obj_2.start_session()
    inbox = dm_test_obj_2.retrieve_new()
    assert isinstance(inbox, list)
    if len(inbox) != 0:
        assert inbox[-1]['message'] == "Hello temp_user!"
        assert inbox[-1]['from'] == "testingdm"


def test_retrieve_all():
    '''
    Tests retrive_all() function of ds_messenger.py
    '''
    dm_test_obj_1 = dsm.DirectMessenger("127.0.0.1", "testingdm", "using unittest")
    dm_test_obj_2 = dsm.DirectMessenger("127.0.0.1", "temp_user", "temp_password")

    # getting inbox before joining (triggers dsp.DSProtocolError)
    inbox = dm_test_obj_1.retrieve_all()
    assert inbox is None

    # join and get inbox
    dm_test_obj_1.start_session()
    inbox = dm_test_obj_1.retrieve_all()
    assert isinstance(inbox, list) and (len(inbox) == 0 or len(inbox) > 0)

    # send message to dm_test_obj_1 then retrieve their inbox
    dm_test_obj_2.start_session()
    is_sent = dm_test_obj_2.send("Hello to you too, testingdm", "testingdm")
    assert is_sent is True

    dm_test_obj_1.start_session()
    inbox = dm_test_obj_1.retrieve_all()
    assert isinstance(inbox, list) and len(inbox) > 0
    assert inbox[-1]['message'] == "Hello to you too, testingdm"
    assert inbox[-1]['from'] == "temp_user"


def test_get_inbox_exception():
    '''
    Tests Exceptions in get_inbox() are being thrown and handled correctly.
    '''
    dm_test_obj_1 = dsm.DirectMessenger("127.0.0.1", "testingdm", "using unittest")
    dm_test_obj_1.start_session()
    # reassigning token to get error message from server
    dm_test_obj_1.token = "badtoken"
    inbox = dm_test_obj_1.retrieve_all()
    assert inbox is None


def test_get_response_exception():
    '''
    Tests Exceptions in get_response() are being thrown and handled correctly.
    '''
    dm_test_obj_1 = dsm.DirectMessenger("127.0.0.1", "testingdm", "using unittest")
    dm_test_obj_1.start_session()
    dm_test_obj_1.send("A message to a non-existent user", "A non-existent user")


def test_direct_message_class():
    '''
    Tests the functionality of the DirectMessage class is
    working properly and returning the correct types and values.
    '''
    dm_obj = dsm.DirectMessage()
    dm_obj.set_recipient("recipient")
    dm_obj.set_message("new message")
    dm_obj.create_timestamp()

    assert isinstance(dm_obj.recipient, str)
    assert isinstance(dm_obj.message, str)
    assert isinstance(dm_obj.timestamp, float)

    assert dm_obj.recipient == "recipient"
    assert dm_obj.message == "new message"


if __name__ == "__main__":
    test_direct_messenger_init()
    test_start_session()
    test_join_exceptions()
    test_init_socket_exceptions()
    test_send()
    test_get_response_exception()
    test_retrieve_new()
    test_retrieve_all()
    test_get_inbox_exception()
    test_direct_message_class()
