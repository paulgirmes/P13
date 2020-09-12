"""
Utility to send mail reports to family-members
with authorisation

"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import get_connection, EmailMessage
from django.template.loader import get_template
from frontpage.models import Child_care_facility
from auth_access_admin.models import FamilyMember
from day_to_day.models import Child, DailyFact
from django.conf import settings


class Command(BaseCommand):

    help = (
        "Sends Dailyfact Mails to FamilyMenber which "
        + "has_daylyfact_access=True, "
        + "please provide a .txt template url"
    )

    def add_arguments(self, parser):
        parser.add_argument("txt_template", nargs="+", type=str)

    def handle(self, *args, **options):
        self.send_dailyfacts(options["txt_template"][0])

    def send_dailyfacts(self, txt_template):
        """
        takes a .txt template url as argument
        sends one mail to each authorized family
        member with day details about their children
        """
        cc_facility = Child_care_facility.objects.get(name=settings.STRUCTURE)
        familly_members = self.get_family_members()
        plaintext = get_template(txt_template)
        if familly_members is not None:
            messages = self.get_messages(
                familly_members, cc_facility, plaintext
            )
        if messages is not None:
            # Use default email connection
            connection = get_connection()
            connection.send_messages(messages)

    def get_family_members(self):
        # returns family members with has_daylyfact_access=True/None
        # if not
        family_members = FamilyMember.objects.filter(has_daylyfact_access=True)
        if family_members.count() != 0:
            return family_members
        return None

    def get_dailyFacts_today(self, familly_member):
        # returns dayly facts for one familly member ordered by child
        # in a dict {child1:daylifactslist,....}
        daily_facts_today = []
        childs = Child.objects.filter(relative=familly_member)
        for child in childs:
            daily_Facts_today_child = (
                DailyFact.objects.filter(child=child)
                .filter(time_stamp__date=timezone.now().date())
                .order_by("-time_stamp")
            )
            if daily_Facts_today_child.count() != 0:
                daily_facts_today.append(daily_Facts_today_child)
        if len(daily_facts_today) != 0:
            return [childs, daily_facts_today]
        return None

    def get_messages(self, familly_members, structure, txt_template):
        # returns a list of emails (1 for each family member if any dailyfacts)
        messages = []
        for member in familly_members:
            dailyfacts = self.get_dailyFacts_today(member)
            if dailyfacts is not None:
                context = {
                    "member": member,
                    "childs": dailyfacts[0],
                    "dailyfacts": dailyfacts[1],
                    "child_care_facility": structure,
                }
                subject, from_email, to = (
                    "Voici les Transmissions de vos enfants",
                    structure.email,
                    member.email,
                )
                text_content = txt_template.render(context)
                msg = EmailMessage(subject, text_content, from_email, [to])
                messages.append(msg)
        if len(messages) != 0:
            return messages
        return None
