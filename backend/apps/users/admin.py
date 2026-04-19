from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import CustomUserModel
from django.db.models import Count
from django.db.models.functions import TruncDay
import json

@admin.register(CustomUserModel)
class CustomUserAdmin(ModelAdmin):
    list_display = ('email', 'full_name', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('email', 'full_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('-date_joined',)

    def changelist_view(self, request, extra_context=None):
        """Override to add chart data to the user list page"""
        extra_context = extra_context or {}
        
        # Calculate user statistics
        total_users = CustomUserModel.objects.count()
        active_users = CustomUserModel.objects.filter(is_active=True).count()
        
        extra_context.update({
            "total_users": total_users,
            "active_users": active_users,
        })
        
        # Chart data
        try:
            data = (
                CustomUserModel.objects
                .annotate(date=TruncDay("date_joined"))
                .values("date")
                .annotate(count=Count("id"))
                .order_by("date")
            )
            
            labels = [d["date"].strftime("%Y-%m-%d") for d in data] if data else []
            values = [d["count"] for d in data] if data else []
        except Exception:
            labels = []
            values = []
        
        chart_data = {
            "labels": labels,
            "datasets": [{
                "label": "New Users",
                "data": values,
                "borderColor": "#7c3aed", 
                "backgroundColor": "rgba(124, 58, 237, 0.1)",
                "tension": 0.4,
                "fill": True
            }],
        }
        
        extra_context["user_growth_chart"] = json.dumps(chart_data)
        return super().changelist_view(request, extra_context=extra_context)


# Unfold Dashboard Stats Callback
def user_stats_callback(request, context):
    from apps.reflections_chat.models import ConversationModel
    
    context.update({
        "total_users": CustomUserModel.objects.count(),
        "active_users": CustomUserModel.objects.filter(is_active=True).count(),
        "total_conversations": ConversationModel.objects.count(),
    })

    # User growth chart logic
    try:
        data = (
            CustomUserModel.objects
            .annotate(date=TruncDay("date_joined"))
            .values("date")
            .annotate(count=Count("id"))
            .order_by("date")
        )

        labels = [d["date"].strftime("%Y-%m-%d") for d in data] if data else []
        values = [d["count"] for d in data] if data else []
        
        chart_data = {
            "labels": labels,
            "datasets": [{
                "label": "New Users",
                "data": values,
                "borderColor": "#7c3aed", 
                "backgroundColor": "rgba(124, 58, 237, 0.1)",
                "tension": 0.4,
                "fill": True
            }],
        }
        context["dashboard_chart"] = json.dumps(chart_data)
    except Exception as e:
        context["dashboard_chart"] = json.dumps({"labels": [], "datasets": []})

    return context
