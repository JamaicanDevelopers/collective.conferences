# -*- coding: utf-8 -*-
from collective.conferences import _
from zope import schema
from plone.supermodel import model
from Products.Five import BrowserView
from plone.supermodel.directives import primary
from Acquisition import aq_inner, aq_parent
from plone.autoform.directives import write_permission, read_permission
from plone.app.textfield import RichText
from zope.schema.interfaces import IContextSourceBinder
from zope.interface import directlyProvides
from zope.security import checkPermission
import datetime

from zope.interface import invariant, Invalid


from z3c.relationfield.schema import RelationChoice
# from plone.formwidget.contenttree import ObjPathSourceBinder




from collective.conferences.speaker import ISpeaker
from collective.conferences.track import ITrack

from plone.namedfile.field import NamedBlobFile
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

# from collective import dexteritytextindexer

from collective.conferences.callforpaper import ICallforpaper


def vocabCfPTracks(context):
    # For add forms

    # For other forms edited or displayed

    if context is not None and not ICallforpaper.providedBy(context):
        #context = aq_parent(aq_inner(context))
        context = context.__parent__

    track_list = []
    if context is not None and hasattr(context, 'cfp_tracks'):
        track_list = context.cfp_tracks

    terms = []
    for value in track_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'), title=value))

    return SimpleVocabulary(terms)

directlyProvides(vocabCfPTracks, IContextSourceBinder)


# class StartBeforeEnd(Invalid):
#     __doc__ = _(u"The start or end date is invalid")


class IWorkshop(model.Schema):
    """A conference workshop. Workshops are managed inside tracks of the Program.
    """
        
    length = SimpleVocabulary(
       [SimpleTerm(value=u'30', title=_(u'30 minutes')),
        SimpleTerm(value=u'45', title=_(u'45 minutes')),
        SimpleTerm(value=u'60', title=_(u'60 minutes')),
        SimpleTerm(value=u'120', title=_(u'120 minutes')),
        SimpleTerm(value=u'180', title=_(u'180 minutes')),
        SimpleTerm(value=u'240', title=_(u'240 minutes')),]
        )
    

    title = schema.TextLine(
            title=_(u"Title"),
            description=_(u"Workshop title"),
        )

    description = schema.Text(
            title=_(u"Workshop summary"),
        )

    primary('details')
    details = RichText(
            title=_(u"Workshop details"),
            required=False
        )

    # use an autocomplete selection widget instead of the default content tree
#    form.widget(speaker=AutocompleteFieldWidget)
#    speaker = RelationChoice(
#            title=_(u"Leader of the workshop"),
#           # source=ObjPathSourceBinder(object_provides=ISpeaker.__identifier__),
#            required=False,
#        )
#    form.widget(speaker=AutocompleteFieldWidget)
#    speaker2 = RelationChoice(
#            title=_(u"Co-Leader of the workshop"),
#           # source=ObjPathSourceBinder(object_provides=ISpeaker.__identifier__),
#            required=False,
#            )


#    dexteritytextindexer.searchable('call_for_paper_tracks')
#    call_for_paper_tracks = schema.List(
#        title=_(u"Choose the track for your workshop"),
#        value_type=schema.Choice(source=vocabCfPTracks),
#        required=True,
#    )


        
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
    
            
    length= schema.Choice(
            title=_(u"Length"),
            vocabulary=length,
            required=True,
        )
  

    write_permission(order='collective.conferences.ModifyTrack')
    order=schema.Int(
           title=_(u"Orderintrack"),               
           description=_(u"Order in the track: write in an Integer from 1 to 12"),
           min=1,
           max=12,
           required=False,
        )
                    
    
    slides = NamedBlobFile(
            title=_(u"Workshop slides / material"),
            description=_(u"Please upload your workshop presentation or material about the content of the workshop in front or short after you have given the workshop."),
            required=False,
        )    
    
    
    creativecommonslicense= schema.Bool(
            title=_(u'label_creative_commons_license', default=u'License is Creative Commons Attribution-Share Alike 3.0 License.'),
                description=_(u'help_creative_commons_license', default=u'You agree that your talk and slides are provided under the Creative Commons Attribution-Share Alike 3.0 License.'),
                default=True
        )
    
        
    messagetocommittee = schema.Text (
            title=_(u'Messages to the Program Committee'),
            description=_(u'You can give some information to the committee here, e.g. about days you are (not) available to give the workshop'),
            required=False,                     
        )
    
    
    read_permission(reviewNotes='cmf.ReviewPortalContent')
    write_permission(reviewNotes='cmf.ReviewPortalContent')
    reviewNotes = schema.Text(
            title=u"Review notes",
            required=False,
        )



# @grok.subscribe(IWorkshop, IObjectMovedEvent)
# def removeCFP_referenceworkshop(workshop, event):
#    if not ICallforpaper.providedBy(event.newParent):
#        workshop.call_for_paper_tracks = None


#    @invariant
#    def validateStartEnd(data):
#        if data.start is not None and data.end is not None:
#            if data.start > data.end:
#                raise StartBeforeEnd(_(
#                    u"The start date must be before the end date."))
                
    
#@grok.subscribe(IWorkshop, IObjectAddedEvent)
#def workshopaddedevent(workshop, event):
#    setdates(workshop)

#@grok.subscribe(IWorkshop, IObjectModifiedEvent)
#def workshopmodifiedevent(workshop, event):
#    setdates(workshop)
    


class WorkshopView(BrowserView):

    def canRequestReview(self):
        return checkPermission('cmf.RequestReview', self.context)

    def WorkshopRoom(self):

       from collective.conferences.track import ITrack
       parent = aq_parent(aq_inner(self.context))
       if ITrack.providedBy(parent):
           room = parent.room.to_object.title
       else: room = ""
       return room
