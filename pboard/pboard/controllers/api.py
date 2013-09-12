# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
from tg import expose, flash, require, url, lurl, request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg import predicates


from pboard.lib.base import BaseController
from pboard.lib   import dbapi as pld
from pboard.model import data as pmd
from pboard import model as pm

__all__ = ['PODApiController']

class PODApiController(BaseController):
    """Sample controller-wide authorization"""
    
    # The predicate that must be met for all the actions in this controller:
    # allow_only = has_permission('manage',
    #                             msg=l_('Only for people with the "manage" permission'))
    
    @expose('pboard.templates.index')
    def index(self):
        """Let the user know that's visiting a protected controller."""
        flash(_("Secure Controller here"))
        return dict(page='index')
    
    @expose()
    def create_event(self, parent_id=None, data_label=u'',data_datetime=None,data_reminder_datetime=None,add_reminder=False, **kw):

      loNewNode = pld.createNode()
      loNewNode.parent_id     = int(parent_id)
      loNewNode.node_type     = pmd.PBNodeType.Event
      loNewNode.data_label    = data_label
      loNewNode.data_content  = ''
      loNewNode.data_datetime = data_datetime
      if add_reminder:
        loNewNode.data_reminder_datetime = data_reminder_datetime

      pm.DBSession.flush()
      redirect(lurl('/dashboard?node=%i'%(loNewNode.parent_id)))

    @expose()
    def set_parent_node(self, node_id, new_parent_id, **kw):
      loNewNode = pld.getNode(node_id)
      if new_parent_id!='':
        loNewNode.parent_id = int(new_parent_id)
      pm.DBSession.flush()
      redirect(lurl('/dashboard?node=%s'%(node_id)))

