from django.db import models
from frontpage.models import Child_care_facility
from auth_access_admin.models import Employee, FamilyMember


class EmployeePlanifiedDay(models.Model):
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
        "Heure de Départ réel",
        auto_now_add=True,
        blank=True,
    )
    absence_motive = models.CharField(
        "Motif de l'absence", max_length=100, blank=True,
        )

    class Meta:
        verbose_name = "Jour de Planification Employés"
        verbose_name_plural = "Jours de Planification Employés"

    def __str__(self):
        return self.open_day+" "+self.employee


class ChildPlanifiedDay(EmployeePlanifiedDay):
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
    last_name = models.CharField("Nom", max_length=50)
    first_name = models.CharField("Prénom", max_length=50)
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
        verbose_name = "Lien Familial"
        verbose_name_plural = "Liens Familiaux"

    def __str__(self):
        return self.child+" "+self.relative


class OpenDay(models.Model):
    date = models.DateField("Date")
    opening_H = models.TimeField("Heure d'ouverture")
    closing_H = models.TimeField("Heure de fermeture")
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
        verbose_name= "Enfant",
        on_delete= models.CASCADE,
        )

    time_stamp = models.DateTimeField(
        "Horodatage",
        auto_now_add=True,
        )
    employee_nr = models.SmallIntegerField("Numéro de l'employé")
    

    class Meta:
        verbose_name = "Donnée de Transmission"
        verbose_name_plural = "Données de Transmission"
    
    def __str__(self):
        return self.time_stamp+", "+self.employee


