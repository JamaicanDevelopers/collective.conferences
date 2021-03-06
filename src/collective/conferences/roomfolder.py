# -*- coding: utf-8 -*-
from collective.conferences import _
from plone.supermodel import model
from Products.Five import BrowserView
from plone.app.textfield import RichText
from plone.supermodel.directives import primary
from zope import schema
from zope.security import checkPermission


class IRoomfolder(model.Schema):
    """A folder for the rooms of a conference.
    """


    title = schema.TextLine(
            title=_(u"Name of the room folder"),
        )

    description = schema.Text(
            title=_(u"roomfolder description"),
        )
    
    
    primary('details')
    details = RichText(
            title=_(u"Information about the Conference Rooms"),
            required=False
        )

    
class RoomfolderView(BrowserView):

    def canRequestReview(self):
        return checkPermission('cmf.RequestReview', self.context)   