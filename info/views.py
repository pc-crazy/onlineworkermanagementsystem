# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.shortcuts import render
from django.contrib.auth import login
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django import forms
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes

from django.utils.encoding import force_str


from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView, FormView, CreateView, ListView, DeleteView, UpdateView
from django.contrib.auth import get_user_model
from django_filters.views import FilterView

# from info.filter import SkillFilter
from info.token import account_activation_token
from worker.models import WorkerProfile, WorkerSkill, ContractorProfile, HireWorker
from info.permisionmixin import WorkerCheckMixin, ContractorCheckMixin

User = get_user_model()

from .forms import UserRegistrationForm, LoginForm, ProfileForm, WorkerSkillForm, ContractorProfileForm, HireSkillForm


def home(request):
    return render(request, 'index.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponseRedirect('/')
    else:
        return HttpResponse('Activation link is invalid!')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            phone_number = userObj['phone_number']
            first_name =  userObj['first_name']
            last_name =  userObj['last_name']
            password =  userObj['password']
            email =  userObj['email']
            type =  userObj['type']
            if not User.objects.filter(phone_number=phone_number).exists():
                user = User.objects.create_user(phone_number,first_name,last_name,email,type, password)
                # login(request, user)
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                # email.send()
                user.is_active = True
                user.save()
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
        else:
            return render(request, 'registration.html', {'form': form})
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form' : form})

def loginuser(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            phone_number = userObj['phone_number']
            password =  userObj['password']
            try:
                user = User.objects.get(phone_number = phone_number)
            except:
                form.add_error(None, 'User not found.')
                return render(request, 'login.html', {'form' : form})
            if not  user.check_password(password):
                form.add_error(None, 'wrong password')
                return render(request, 'login.html', {'form' : form})
            if not  user.is_active:
                form.add_error(None, 'You are not activated. Contact to admin.')
                return render(request, 'login.html', {'form' : form})
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form' : form})

def aboutus(request):
    return render(request, 'aboutus.html')

def contactus(request):
    return render(request, 'contactus.html')

class SkillCreate(WorkerCheckMixin, FormView):

    template_name = 'Skill.html'
    form_class = WorkerSkillForm
    success_url = '/skill/'

    def post(self, request, *args, **kwargs):
        return super(SkillCreate, self).post(request,*args,**kwargs)

    def form_valid(self, form):
        rate_per_day = form.cleaned_data['rate_per_day']
        skill = form.cleaned_data.get('skill').capitalize()
        obj, created = WorkerSkill.objects.get_or_create(user=self.request.user,skill=skill,
                                                         rate_per_day=rate_per_day)
        obj.experience = form.cleaned_data['experience']
        obj.save()
        return super(SkillCreate, self).form_valid(form)

class SkillUpdate(WorkerCheckMixin, UpdateView):
    template_name = 'Skill.html'
    form_class = WorkerSkillForm
    success_url = '/skill/'
    queryset = WorkerSkill.objects.all()

    def get(self, request, *args, **kwargs):
        return super(SkillUpdate, self).get(request, *args, **kwargs)

class SkillListView(WorkerCheckMixin, ListView):

    template_name = 'skilllist.html'
    queryset = WorkerSkill.objects.all().order_by('-created_at')
    paginate_by = 10


    def get_queryset(self):
        return super(SkillListView, self).get_queryset().filter(user=self.request.user)

class DeleteSkillView(WorkerCheckMixin, DeleteView):
    model = WorkerSkill
    template_name = 'confirm_delete.html'
    success_url =  '/skill/'

    def delete(self, request, *args, **kwargs):
       self.object = self.get_object()
       if self.object.user == request.user:
          self.object.delete()
          return HttpResponseRedirect(self.get_success_url())
       else:
          raise Http404 #or return HttpResponse('404_url')

class GetProfile(TemplateView):

    template_name = 'worker_profile_show.html'

    def get_context_data(self, **kwargs):
        context = super(GetProfile, self).get_context_data(**kwargs)
        if self.request.user.is_contractor():
            if ContractorProfile.objects.filter(user=self.request.user).exists():
                context['profile'] = ContractorProfile.objects.get(user=self.request.user)
            return context
        if WorkerProfile.objects.filter(user=self.request.user).exists():
            context['profile'] = WorkerProfile.objects.get(user=self.request.user)
        return context


class CreateProfile(WorkerCheckMixin, FormView):
    form_class = ProfileForm
    template_name = 'worker_profile.html'
    success_url = '/'

    def get_form(self, form_class =  ProfileForm):
        """
        Check if the user already saved contact details. If so, then show
        the form populated with those details, to let user change them.
        """
        if self.request.user.is_worker:
            try:
                contact = WorkerProfile.objects.get(user=self.request.user)
                return form_class(instance=contact, **self.get_form_kwargs())
            except WorkerProfile.DoesNotExist:
                return form_class(**self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
        return super(CreateProfile, self).post(request, *args, **kwargs)

    def form_invalid(self, form):
        return super(CreateProfile, self).form_invalid(form)

    def form_valid(self, form):
        obj , created = WorkerProfile.objects.get_or_create(user=self.request.user)
        obj.city = form.cleaned_data.get('city')
        obj.district = form.cleaned_data.get('district')
        obj.state = form.cleaned_data.get('state')
        obj.address = form.cleaned_data.get('address')
        obj.picture = form.cleaned_data.get('picture')
        obj.about = form.cleaned_data.get('about')
        obj.save()
        return super(CreateProfile, self).form_valid(form)


class CreateContractorProfile(ContractorCheckMixin, FormView):
    form_class = ContractorProfileForm
    template_name = 'worker_profile.html'
    success_url = '/'

    def get_form(self, form_class =  ContractorProfileForm):
        """
        Check if the user already saved contact details. If so, then show
        the form populated with those details, to let user change them.
        """
        if self.request.user.is_worker:
            try:
                contact = ContractorProfile.objects.get(user=self.request.user)
                return form_class(instance=contact, **self.get_form_kwargs())
            except ContractorProfile.DoesNotExist:
                return form_class(**self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
        return super(CreateContractorProfile, self).post(request, *args, **kwargs)

    def form_invalid(self, form):
        return super(CreateContractorProfile, self).form_invalid(form)

    def form_valid(self, form):
        obj , created = ContractorProfile.objects.get_or_create(user=self.request.user)
        obj.city = form.cleaned_data.get('city')
        obj.district = form.cleaned_data.get('district')
        obj.state = form.cleaned_data.get('state')
        obj.address = form.cleaned_data.get('address')
        obj.picture = form.cleaned_data.get('picture')
        obj.about = form.cleaned_data.get('about')
        obj.licence = form.cleaned_data.get('licence')
        obj.save()
        return super(CreateContractorProfile, self).form_valid(form)


class WorkerSkillListView(ListView, FilterView):

    paginate_by = 10
    model = WorkerSkill
    queryset = WorkerSkill.objects.filter(status='N').order_by('-created_at')
    template_name = 'worker_skill_list_filter.html'
    # filterset_class = SkillFilter

    def get_queryset(self):
        queryset =super(WorkerSkillListView, self).get_queryset()
        remove_id = []
        for qs in queryset:
            if not qs.user.is_profile_compele():
                remove_id.append(qs.id)
        queryset = queryset.exclude(id__in= remove_id)
        skill = self.request.GET.get('skill')
        if skill:
            queryset = queryset.filter(skill__icontains = skill)
        city = self.request.GET.get('city')
        if city:
            queryset = queryset.filter(user__rel_worker_profile__city__icontains = city)
        name = self.request.GET.get('name')
        if name :
            queryset = queryset.filter(user__first_name__icontains = name)
        experience = self.request.GET.get('experience')
        if experience:
            queryset = queryset.filter(experience__gte = int(experience))

        return queryset

class HireWorkerView(FormView):

    template_name = 'hire_worker_profile.html'
    form_class = HireSkillForm
    success_url = '/hired-request/'

    def get_context_data(self, **kwargs):
        context = super(HireWorkerView, self).get_context_data(**kwargs)
        if self.request.method == 'GET':
            skill_id = self.request.resolver_match.kwargs['pk']
            WorkerSkill.objects.filter(id = skill_id)
            obj = WorkerSkill.objects.filter(id=skill_id).first()
            if WorkerProfile.objects.filter(user=obj.user).exists():
                context['profile'] = WorkerProfile.objects.get(user=obj.user)
            context['form'] = HireSkillForm
            context['id'] = self.request.resolver_match.kwargs.get('pk', None)
        return context


    def get(self, request, *args, **kwargs):
        return super(HireWorkerView, self).get(request, *args)


    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not self.request.user.is_profile_compele():
            form.add_error(None, 'Error!! Complete  your profile first.Until complete profile you cannot hire any worker')
            context = self.get_context_data(**kwargs)
            skill_id = self.request.resolver_match.kwargs['pk']
            WorkerSkill.objects.filter(id=skill_id)
            obj = WorkerSkill.objects.filter(id=skill_id).first()
            if WorkerProfile.objects.filter(user=obj.user).exists():
                context['profile'] = WorkerProfile.objects.get(user=obj.user)
            context['form'] = HireSkillForm
            context['id'] = self.request.resolver_match.kwargs.get('pk', None)
            context['form'] = form
            return self.render_to_response(context)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        workskill_id = self.request.resolver_match.kwargs.get('pk')
        from_date = form.cleaned_data['from_date']
        to_date = form.cleaned_data['to_date']
        # HireWorker.objects.filter(hired_by=request.user, skill_id=workskill_id, fr)
        ho = HireWorker.objects.get_or_create(hired_by=user, skill_id=workskill_id, from_date=from_date,
                                  to_date=to_date)
        return super(HireWorkerView, self).form_valid(form)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        skill_id = self.request.resolver_match.kwargs['pk']
        WorkerSkill.objects.filter(id=skill_id)
        obj = WorkerSkill.objects.filter(id=skill_id).first()
        if WorkerProfile.objects.filter(user=obj.user).exists():
            context['profile'] = WorkerProfile.objects.get(user=obj.user)
        context['form'] = HireSkillForm
        context['id'] = self.request.resolver_match.kwargs.get('pk', None)
        context['form'] = form
        return self.render_to_response(context)

class HireRequestList(ListView):

    template_name = 'hire-request.html'
    queryset = HireWorker.objects.all()
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_worker():
            return super(HireRequestList, self).get_queryset().filter(skill__user = self.request.user)
        return super(HireRequestList, self).get_queryset().filter(hired_by = self.request.user)

def confirm_hire_worker(request,pk):
    obj = get_object_or_404(HireWorker, pk=pk)
    obj.status = 'confirm'
    obj.save()
    return HttpResponseRedirect('/hired-request/')