from django.urls import reverse_lazy
from django.views.generic import (TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView)
from django.views.generic.edit import FormView
from django.contrib import messages
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect
from .forms import *
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

class HomeView(TemplateView):
    template_name = 'app_admin/index.html'


class CategoryCreateView(CreateView):
    template_name = 'app_admin/category_create.html'
    model = Category
    form_class = CategoryCreateForm
    success_url = reverse_lazy('app_admin:category')

    def form_valid(self, form):
        # Check if the category_sort_id already exists in the form
        new_category_sort_id = form.cleaned_data['category_sort_id']

        # Check if the ID already exists in the form data (not in the database)
        if Category.objects.filter(category_sort_id=new_category_sort_id).exists():
            # Add an error message to the form
            messages.error(self.request, 'Selline kategooria number on juba olemas, palun sisesta teine number!')
            return self.form_invalid(form)

        # Save the form if the ID is unique
        return super().form_valid(form)

    def form_invalid(self, form):
        # Clear existing messages to prevent duplicates
        messages.success(self.request, "")

        # Check if there are errors in the form for the 'category_name' field
        if 'category_name' in form.errors:
            # Clear existing errors for 'category_name' field
            form.errors.pop('category_name', None)

            # Capture the error message and add it to the messages
            messages.error(self.request, "Selline toidu kategooria on juba olemas.")

        return super().form_invalid(form)


class CategoryListView(ListView):
    template_name = 'app_admin/category.html'
    context_object_name = 'data'  # Use a more general name to hold both categories and menus

    def get_queryset(self):
        categories = Category.objects.all()
        return {'categories': categories}


class CategoryUpdateView(UpdateView):
    template_name = 'app_admin/category_update.html'
    model = Category
    form_class = CategoryUpdateForm
    success_url = reverse_lazy('app_admin:category')

    def form_valid(self, form):
        # Additional checks
        return super().form_valid(form)


class CategoryDeleteView(DeleteView):
    template_name = 'app_admin/category_delete.html'
    model = Category
    success_url = reverse_lazy('app_admin:category')


class MenuListView(ListView):
    template_name = 'app_admin/menu.html'
    context_object_name = 'data'
    paginate_by = 10

    def get_queryset(self):
        return Menu.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class MenuCreateView(CreateView):
    template_name = 'app_admin/menu_form_create.html'
    model = Menu
    form_class = MenuCreateForm
    success_url = reverse_lazy('app_admin:category')

    def form_invalid(self, form):
        # Check if there are errors in the form for the 'date' field
        if 'date' in form.errors:
            # Clear existing errors for 'date' field
            form.errors.pop('date', None)

            # Capture the error message and add it to the messages
            messages.error(self.request, "Selle kuupäevaga on päis juba olemas!")

        return super().form_invalid(form)


class MenuUpdateView(UpdateView):
    template_name = 'app_admin/menu_update.html'
    model = Menu
    form_class = MenuCreateForm
    success_url = reverse_lazy('app_admin:category')

    def form_valid(self, form):
        # Additional checks
        return super().form_valid(form)


class MenuDeleteView(DeleteView):
    template_name = 'app_admin/menu_delete.html'
    model = Menu
    success_url = reverse_lazy('app_admin:category')


class FoodMenuListView(ListView):
    model = FoodMenu
    template_name = 'app_admin/food_menu_list.html'
    context_object_name = 'object_list'
    paginate_by = 10  # Number of items to display per page

    def get_queryset(self):
        # Retrieve the queryset and order it by the 'date' field
        return FoodMenu.objects.all().order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.object_list, self.paginate_by)

        page = self.request.GET.get('page')
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            object_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            object_list = paginator.page(paginator.num_pages)

        context['object_list'] = object_list
        return context


class FoodMenuUpdateView(SingleObjectMixin, FormView):
    model = FoodMenu
    form_class = FoodMenuUpdateForm
    template_name = 'app_admin/food_menu_update.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=FoodMenu.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=FoodMenu.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return FoodMenuFormset(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('app_admin:food_menu_detail', kwargs={'pk': self.object.pk})


class FoodMenuDetailView(DetailView):
    model = FoodMenu
    template_name = 'app_admin/food_menu_detail.html'


class FoodMenuDeleteView(DeleteView):
    model = FoodMenu
    template_name = 'app_admin/food_menu_delete.html'
    success_url = reverse_lazy('app_admin:food_menu_list')


class FoodMenuCreateView(CreateView):
    model = FoodMenu
    form_class = FoodMenuCreateForm
    template_name = 'app_admin/food_menu_create.html'

    def form_invalid(self, form):
        # Capture the ValidationError and add it to the form's errors
        messages.error(self.request, form.errors['__all__'][0])
        return super().form_invalid(form)


class ArchivePage(ListView):
    model = Menu
    template_name = 'app_admin/archive.html'

    def get_context_data(self, **kwargs):
        context = super(ArchivePage, self).get_context_data(**kwargs)
        context['unique_dates'] = Menu.objects.all()
        return context


class SearchResultsListView(ListView):
    model = FoodItem
    template_name = 'app_admin/archive_search.html'
    allow_empty = False
    paginate_by = 10  # Adjust the number of items per page as needed

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = None
        if len(query) > 2:
            object_list = FoodItem.objects.select_related('menu').filter(food__icontains=query)

        return object_list

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(SearchResultsListView, self).dispatch(request, *args, **kwargs)
        except Http404:
            return redirect('app_admin:archive')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class OldMenuListView(ListView):
    model = Menu
    template_name = 'app_admin/archive_menu.html'

    def get_context_data(self, **kwargs):
        all_data = None
        query = self.request.GET.get('date')
        # Listi vaade lisa argument
        # https://stackoverflow.com/questions/71023649/listview-with-an-extra-argument
        if not query:
            query = self.kwargs['date']

        # teeme kuupäeva sobivaks
        # date_object = datetime.strptime(query, '%d.%m.%Y').date()
        # date_object = datetime.strptime(query, '%d.%m.%Y').date()
        # today_string = date_object.strftime('%Y-%m-%d')
        parts = query.split('.')
        today_string = parts[2] + '-' + parts[1] + '-' + parts[0]
        # estonian_date = datetime.strptime(today_string, '%Y-%m-%d').strftime('%d.%m.%Y')
        estonian_date = query

        try:
            # https://stackoverflow.com/questions/1542878/what-to-do-when-django-query-returns-none-it-gives-me-error
            # Kui tekib error
            today_menu_id = Menu.objects.get(date=today_string)  # vastuseks üks kirje või error
            today_menuheadlines = Menu.objects.filter(Q(date=today_string)).values('date', 'theme', 'recommends',
                                                                                            'prepared')
            today_all_categories = FoodMenu.objects.filter(date_id=today_menu_id)

            # https://stackoverflow.com/questions/3397170/
            all_data = (FoodItem.objects.filter(Q(menu_id__in=today_all_categories))
                        .values('menu_id', 'food', 'full_price', 'half_price', 'show_in_menu',
                                'menu__category__category_name', 'id', 'menu__category__category_sort_id')
                        .annotate(dcount=Count('menu_id')).order_by('menu__category__category_sort_id', 'id'))
            # print(today_all_categories)
        except Menu.DoesNotExist:
            today_menuheadlines = None

        context = {
            'object_list': all_data,
            'menuheadlines': today_menuheadlines,
            'estonian_date': estonian_date,
            'today_string': today_string

        }

        return context



