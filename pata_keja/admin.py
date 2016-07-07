from django.contrib import admin
from .models import houseDesc, Comment,houseManager,Plot,booking
# Adds our models to be managable by the admin interface


class houseDescAdmin(admin.ModelAdmin):
    list_display=('house_type','rent_per_month','plot','created','status','house_booked','house_owner','slug')
    search_fields=('rent_per_month', 'status','house_booked','house_owner')
    prepopulated_fields={'slug': ('slug',)}
    date_hierarchy='created'
admin.site.register(houseDesc, houseDescAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display=('name','created', 'active')
    list_filter=('active', 'created', 'updated')
    search_fields=('name', 'body')
    
admin.site.register(Comment,CommentAdmin)


class managerAdmin(admin.ModelAdmin):
    list_display=('first_name','last_name','contanct','email','registered','status')
    search_fields=('first_name','contanct','status')
    date_heirachy='registered'
admin.site.register(houseManager,managerAdmin)


class plotAdmin(admin.ModelAdmin):
    list_display=('name','availableHouses','caretaker')
    search_fields=('name',)
    
admin.site.register( Plot,plotAdmin)


class bookAdmin(admin.ModelAdmin):
    list_display=('user_name','booked_at','house_booked')
    search_fields=('user_name','booked_at')
    date_heirachy='booked_at'
admin.site.register(booking,bookAdmin)
