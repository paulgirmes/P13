from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import get_template
from django.template import Context
from frontpage.models import Child_care_facility
from auth_access_admin.models import FamilyMember
from day_to_day.models import Child, DailyFact
from django.conf import settings

class Command(BaseCommand):

    help = "Sends Dailyfact Mails to FamilyMenber whit has_daylyfact_access=True"
    def add_arguments(self, parser):
        parser.add_argument("txt_template", nargs="+", type=str)
        parser.add_argument("hmtl_template",  nargs="+", type=str)

    def handle(self, *args, **options):
        self.send_dailyfacts(**options)
    
    def send_dailyfacts(self, txt_template, html_template):
        cc_facility = Child_care_facility.objects.get(name=settings.STRUCTURE)
        familly_members = self.get_family_menbers()
        plaintext = get_template(txt_template)
        html = get_template(txt_template)
        if familly_members is not None:
            messages = self.get_messages(familly_members, cc_facility, plaintext, html)
        if messages is not None:
            connection = get_connection()   # Use default email connection
            connection.send_messages(messages)

    def get_family_menbers(self):
        # retourne les membres famille avec has_daylyfact_access=True et None si pas
        family_members = FamilyMember.objects.filter(has_daylyfact_access=True)
        if family_members.count() != 0:
            return family_members 
        return None

    def get_dailyFacts_today(self, familly_member):
        # retourne les dayly facts pour un familly member par enfant dans in dict {enfant1:transmissions,....}
        daily_facts_today = {}
        childs = Child.objects.filter(relative=familly_member)
        for child in childs:
            daily_Facts_today_child = DailyFact.objects.filter(
                    child = child
                    ).order_by("-time_stamp")
            if daily_Facts_today_child.count() != 0: 
                daily_facts_today[child]=daily_Facts_today_child
        if len(daily_facts_today) != 0:
            return daily_facts_today
        return None
        

    def get_messages(self, familly_members, structure, txt_template, html_template):
        messages = None
        for member in familly_members:
            dailyfacts = self.get_dailyFacts_today(member)
            if dailyfacts is not None:
                context = Context({"member" : member, "dailyfacts":dailyfacts, "child_care_facility":structure})
                subject, from_email, to = "Voici les Transmissions de vos enfants", structure.email , member.email
                text_content = txt_template.render(context)
                html_content = html_template.render(context)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                messages.append(msg)
            return messages
            

