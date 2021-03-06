# -*- coding: utf-8 -*-
"""
Integration tests for the ldap authentication sub-system.
"""
from tracim.fixtures.ldap import ldap_test_server_fixtures
from nose.tools import eq_, ok_

from tracim.fixtures.users_and_groups import Test as TestFixture
from tracim.model import DBSession, User
from tracim.tests import LDAPTest, TracimTestController


class TestAuthentication(LDAPTest, TracimTestController):
    application_under_test = 'ldap'
    ldap_server_data = ldap_test_server_fixtures
    fixtures = [TestFixture, ]

    def test_ldap_auth_fail_no_account(self):
        # User is unknown in tracim database
        eq_(0, DBSession.query(User).filter(User.email == 'unknown-user@fsf.org').count())

        self._connect_user('unknown-user@fsf.org', 'no-pass')

        # User is registered in tracim database
        eq_(0, DBSession.query(User).filter(User.email == 'unknown-user@fsf.org').count())

    def test_ldap_auth_fail_wrong_pass(self):
        # User is unknown in tracim database
        eq_(0, DBSession.query(User).filter(User.email == 'richard-not-real-email@fsf.org').count())

        self._connect_user('richard-not-real-email@fsf.org', 'wrong-pass')

        # User is registered in tracim database
        eq_(0, DBSession.query(User).filter(User.email == 'richard-not-real-email@fsf.org').count())

    def test_ldap_auth_sync(self):
        # User is unknown in tracim database
        eq_(0, DBSession.query(User).filter(User.email == 'richard-not-real-email@fsf.org').count())

        self._connect_user('richard-not-real-email@fsf.org', 'rms')

        # User is registered in tracim database
        eq_(1, DBSession.query(User).filter(User.email == 'richard-not-real-email@fsf.org').count())

    def test_ldap_attributes_sync(self):
        # User is already know in database
        eq_(1, DBSession.query(User).filter(User.email == 'lawrence-not-real-email@fsf.local').count())

        # His display name is Lawrence L.
        lawrence = DBSession.query(User).filter(User.email == 'lawrence-not-real-email@fsf.local').one()
        eq_('Lawrence L.', lawrence.display_name)

        # After connexion with LDAP, his display_name is updated (see ldap fixtures)
        self._connect_user('lawrence-not-real-email@fsf.local', 'foobarbaz')
        lawrence = DBSession.query(User).filter(User.email == 'lawrence-not-real-email@fsf.local').one()
        eq_('Lawrence Lessig', lawrence.display_name)
