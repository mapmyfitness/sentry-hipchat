from __future__ import absolute_import

from django import forms

from sentry.plugins import plugins
from sentry.rules import rules
from sentry.rules.actions.base import EventAction


class NotifyHipchatRoomForm(forms.Form):
    room = forms.IntegerField()


class NotifyHipchatRoomAction(EventAction):
    form_cls = NotifyHipchatRoomForm
    label = 'Send a notification to a Hipchat room id: {room}'

    def after(self, event, state):
        room = self.get_option('room')

        if not room:
            return

        plugin = plugins.get('hipchat')
        if not plugin.is_enabled(self.project):
            return

        group = event.group

        if not plugin.should_notify(group=group, event=event):
            return

        plugin.notify_users(group=group, event=event, room=room)


rules.add(NotifyHipchatRoomAction)
