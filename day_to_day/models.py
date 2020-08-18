from django.db import models
from frontpage.models import Child_care_facility
from auth_access_admin.models import Employee, FamilyMember
from django.conf import settings

class EmployeeScheduledDay(models.Model):
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE,
        verbose_name="Employé",
        )
    open_day = models.ForeignKey(
        "OpenDay", 
        on_delete=models.CASCADE,
        verbose_name="Jour d'ouverture"
        )
    scheduled_arrival_time = models.TimeField("Heure d'Arrivée Planifiée")
    scheduled_departure_time = models.TimeField("Heure de Départ Planifiée")
    true_arrival_time_stamp = models.TimeField(
        "Heure d'Arrivée réelle",
        auto_now_add=True,
        blank=True,

        )
    true_departure_time_stamp = models.TimeField(
        "Heure de Départ réelle",
        auto_now_add=True,
        blank=True,
    )
    absence_motive = models.CharField(
        "Motif de l'absence", max_length=100, blank=True,
        )

    class Meta:
        verbose_name = "Jour de Planification Employé"
        verbose_name_plural = "Jours de Planification Employé"

    def __str__(self):
        return self.open_day+" "+self.employee


class ChildScheduledDay(EmployeeScheduledDay):
    employee = None
    child = models.ForeignKey(
        "child", 
        on_delete=models.CASCADE,
        verbose_name="Enfant",
        )
    class Meta:
        verbose_name = "Jour de Planification Enfants"
        verbose_name_plural = "Jours de Planification Enfants"

    def __str__(self):
        return self.open_day+" "+self.child

class Child(models.Model):
    last_name = models.CharField("Nom", max_length=100)
    first_name = models.CharField("Prénom", max_length=100)
    birth_date = models.DateField("Date de Naissance")
    vaccine_next_due_date = models.DateField("Date de Prochaine Vaccination")
    cc_facility = models.ForeignKey(Child_care_facility,
        on_delete=models.CASCADE,
        verbose_name="Structure de Garde"
    )
    relative = models.ManyToManyField(
        FamilyMember,
        through="family_link"
    )
    class Meta:
        verbose_name = "Enfant"
        verbose_name_plural = "Enfants"

    def __str__(self):
        return self.first_name+" "+self.last_name


class Family_link(models.Model):
    child = models.ForeignKey(
        Child,
        on_delete = models.CASCADE,
        verbose_name="Enfant",
        )
    relative = models.ForeignKey(
        FamilyMember,
        on_delete = models.CASCADE,
        verbose_name="Membre Familial",
    )
    link_type = models.CharField(
        "Lien Familial",
        max_length=50,
    )
    retrieval_auth = models.BooleanField(
        "Autorisation de Prise en Charge",
        default=False,
        )
    emergency_contact_person=models.BooleanField(
        "Contact en cas d'urgence",
        default=False,
    )
    class Meta:
        verbose_name = "Lien de parenté"
        verbose_name_plural = "Liens de parenté"

    def __str__(self):
        return self.child+" "+self.relative


class OpenDay(models.Model):
    date = models.DateField("Date")
    opening_H = models.TimeField("Heure d'Ouverture")
    closing_H = models.TimeField("Heure de Fermeture")
    planified_employee = models.ManyToManyField(
        Employee, through="EmployeePlanifiedDay",
        verbose_name= "Employé planifié",
        blank=True,
    )
    planified_child = models.ManyToManyField(
        Child, through="ChildPlanifiedDay",
        verbose_name= "Enfant planifié",
        blank=True,
    )

    class Meta:
        verbose_name = "Jour et heure d'ouverture"
        verbose_name_plural = "Jours et heures d'ouverture"
    
    def __str__(self):
        return " {1}, ouverture à {2}, fermeture à {3}".format(
            self.date, self.opening_H, self.closing_H
            )


class DailyFact(models.Model):

    child = models.ForeignKey(
        Child,
        on_delete= models.CASCADE,
        verbose_name= "Enfant",
        )

    employee = models.ForeignKey(
        Employee,
        on_delete= models.CASCADE,
        verbose_name= "Employé"
    )

    time_stamp = models.DateTimeField(
        "Horodatage",
        auto_now_add=True,
        )

    comment = models.CharField(
        "Commentaire général",
        blank= True,
        max_length= 200,
        )

    class Meta:
        verbose_name = "Donnée de Transmission"
        verbose_name_plural = "Données de Transmission"

    def __str__(self):
        return self.time_stamp+", "+self.employee+"/"+self.child


class Sleep(models.Model):

    length_minutes = models.PositiveSmallIntegerField("Durée")
    daily_fact = models.ForeignKey(
        DailyFact,
        on_delete= models.CASCADE,
        verbose_name= "Transmission"
    )

    class Meta:
        verbose_name = "Sieste"
        verbose_name_plural = "Siestes"

    def __str__(self):
        return self.length_minutes+" minutes"


class Meal(models.Model):

    starter_qtty_gr = models.PositiveSmallIntegerField("Entrée", blank=True)
    main_course_qtty_gr = models.PositiveSmallIntegerField(
            "Plat de résistance",
            blank= True
            )
    desert_qtty_gr = models.PositiveSmallIntegerField("Déssert", blank=True)
    daily_fact = models.ForeignKey(
        DailyFact,
        on_delete= models.CASCADE,
        verbose_name= "Transmission"
        )

    class Meta:
        verbose_name = "Repas"
        verbose_name_plural = "Repas"

    def __str__(self):
        name= ""
        if self.starter_qtty_gr:
            name += "Entrée : "+self.starter_qtty_gr+" gr. "
        if self.main_course_qtty_gr:
            name += "Plat de résistance"+self.main_course_qtty_gr+" gr. "
        if self.desert_qtty_gr:
            name += "Désert"+self.desert_qtty_gr+" gr. "
        return name

class FeedingBottle(models.Model):

    prepared_qtty_ml = models.PositiveSmallIntegerField(
            "Quantité Préparée ml"
        )
    drank_qtty_ml = models.PositiveSmallIntegerField("Quantité Bue ml")
    daily_fact = models.ForeignKey(
        DailyFact,
        on_delete= models.CASCADE,
        verbose_name= "Transmission"
    )

    class Meta:
        verbose_name = "Biberon"
        verbose_name_plural = "Biberons"

    def __str__(self):
        return self.drank_qtty_ml


class Activity(models.Model):

    activity_type = models.CharField("Type d'Activité",
            max_length = 2,
            choices = settings.ACTIVITIES_CHOICES,
        )
    period = models.CharField("Période",
        max_length = 2,
        choices= [
            ("AM","Matin"),
            ("PM", "Après-Midi"),
        ]
    )
    daily_fact = models.ForeignKey(
        DailyFact,
        on_delete= models.CASCADE,
        verbose_name= "Transmission"
    )

    class Meta:
        verbose_name = "Activité"
        verbose_name_plural = "Activités"

    def __str__(self):
        return self.activity_type+", "+self.period


class MedicalEvent(models.Model):

    description = models.CharField("Description",
            max_length = 200,
        )
    body_temp_deg_C = models.DecimalField("Température",
        max_digits = 3,
        decimal_places= 2,
        blank= True,
    )
    given_paracetamol_qtty_mg = models.PositiveSmallIntegerField ("Paracétamol donné / mg",
        blank= True,
    )
    daily_fact = models.ForeignKey(
        DailyFact,
        on_delete= models.CASCADE,
        verbose_name= "Transmission"
    )

    class Meta:
        verbose_name = "Evènement Médical"
        verbose_name_plural = "Evènements Médicaux"

    def __str__(self):
        return self.description


