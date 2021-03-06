# -*- coding: utf-8 -*-
from collective.conferences import _
from plone.supermodel import model
from zope import schema
from plone.app.textfield import RichText
from plone.supermodel.directives import primary
from plone.autoform.directives import write_permission
from Products.Five import BrowserView
from zope.security import checkPermission
from collective.conferences.track import ITrack
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IContextSourceBinder
from zope.interface import directlyProvides
from plone.autoform import directives
from z3c.form.browser.radio import RadioFieldWidget
from plone import api



def vocabBreakLength(context):
    catalog = api.portal.get_tool(name='portal_catalog')
    results = catalog.uniqueValuesFor('breaklength')
    terms = []
    for value in results:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'), title=value))

    return SimpleVocabulary(terms)

directlyProvides(vocabBreakLength, IContextSourceBinder)



class IConferencebreak(model.Schema):

    
    title = schema.TextLine(
            title=_(u"Title"),
            description=_(u"Conference break title"),
        )

    description = schema.Text(
            title=_(u"Conference break summary"),
            required=False
        )

    primary('details')
    details = RichText(
            title=_(u"Conference break details"),
            required=False
        )
        
        
#    form.widget(track=AutocompleteFieldWidget)
#    track = RelationChoice(
#            title=_(u"Track"),
#            source=ObjPathSourceBinder(object_provides=ITrack.__identifier__),
#            required=False,
#        )


    write_permission(startitem='collective.conferences.ModifyTalktime')
    startitem = schema.Datetime(
            title=_(u"Startdate"),
            description =_(u"Start date"),
            required=False,
        )
    

    write_permission(enditem='collective.conferences.ModifyTalktime')
    enditem = schema.Datetime(
            title=_(u"Enddate"),
            description =_(u"End date"),
            required=False,
        )

    directives.widget(breaklength=RadioFieldWidget)
    breaklength= schema.List(
            title=_(u"Length"),
            value_type=schema.Choice(source=vocabBreakLength),
            required=True,
        )

#@grok.subscribe(IConferencebreak, IObjectAddedEvent)
#def conferencebreakaddedevent(conferencebreak, event):
#    setdates(conferencebreak)

#@grok.subscribe(IConferencebreak, IObjectModifiedEvent)
#def conferencebreakmodifiedevent(conferencebreak, event):
#    setdates(conferencebreak)
    


class ConferencebreakView(BrowserView):

    def canRequestReview(self):
        return checkPermission('cmf.RequestReview', self.context)
    