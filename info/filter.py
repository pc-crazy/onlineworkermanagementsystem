# import django_filters
#
# from worker.models import WorkerSkill
#
#
# class SkillFilter(django_filters.FilterSet):
#     first_name = django_filters.CharFilter(lookup_expr='icontains')
#     class Meta:
#         model =  WorkerSkill
#         fields = ['skill',]