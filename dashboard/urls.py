from django.conf.urls import url, include
from django.urls import path, reverse_lazy
# from demosite import settings
from dashboard import views

app_name = 'dashboard'

category_patterns = [
    path('', views.categories, name='categories'),
    path('detail/<uuid:category_uuid>/', views.category_detail, name='category-detail'),
    path('delete/<uuid:category_uuid>/', views.category_delete, name='category-delete'),
    path('delete/', views.categories_delete, name='categories-delete'),
    path('update/<uuid:category_uuid>/', views.category_update, name='category-update'),
    path('create/', views.category_create, name='category-create'),
]

group_patterns = [
    path('',views.groups, name='groups'),
    path('group-create/',views.group_create, name='group-create'),
    path('group-detail/<int:pk>/',views.group_detail, name='group-detail'),
    path('group-delete/<int:pk>/',views.group_delete, name='group-delete'),
    path('group-update/<int:pk>/',views.group_update, name='group-update'),
    path('delete/',views.groups_delete, name='groups-delete'),
]

# highlight_patterns = [
#     path('', views.highlights, name='highlights'),
#     path('detail/<uuid:highlight_uuid>/', views.highlight_detail, name='highlight-detail'),
#     path('update/<uuid:highlight_uuid>/', views.highlight_update, name='highlight-update'),
#     path('delete/<uuid:highlight_uuid>/', views.highlight_delete, name='highlight-delete'),
#     path('delete/', views.highlights_delete, name='highlights-delete'),
#     path('create/', views.highlight_create, name='highlight-create'),
#     path('add-products/<uuid:highlight_uuid>/', views.highlight_add_products, name='highlight-add-products'),
# ]

# new_patterns = [
#     path('',views.news, name='news'),
#     path('news-create/',views.news_create, name='news-create'),
#     path('news-detail/<uuid:news_uuid>/',views.news_detail, name='news-detail'),
#     path('news-delete/<uuid:news_uuid>/',views.news_delete, name='news-delete'),
#     path('news-update/<uuid:news_uuid>/',views.news_update, name='news-update'),
#     path('news-bulk-delete/',views.news_bulk_delete, name='news-bulk-delete'),
# ]


# policy_patterns = [
#     path('', views.policies, name='policies'),
#     path('detail/<uuid:policy_uuid>/', views.policy_details, name='policy-detail'),
#     path('remove/<uuid:policy_uuid>/', views.policy_remove, name='policy-remove'),
#     path('remove-all/', views.policy_remove_all, name='policy-remove-all'),
#     path('update/<uuid:policy_uuid>/', views.policy_update, name='policy-update'),
#     path('create/', views.policy_create, name='policy-create'),
#     path('delete/', views.policies_delete, name='policies-delete'),

#     path('policy-groups/', views.policy_groups, name='policy-groups'),
#     path('policy-groups/delete', views.policy_groups_delete, name='policy-groups-delete'),
#     path('policy-groups/detail/<uuid:group_uuid>/', views.policy_group_details, name='policy-group-detail'),
#     path('policy-groups/update-members/<uuid:group_uuid>/', views.policy_group_update_members, name='policy-group-update-members'),
#     path('policy-groups/remove/<uuid:group_uuid>/', views.policy_group_remove, name='policy-group-remove'),
#     #path('policy-groups/remove-all/', views.policy_remove_all, name='policy-group-remove-all'),
#     path('policy-groups/update/<uuid:group_uuid>/', views.policy_group_update, name='policy-group-update'),
#     path('policy-groups/create/', views.policy_group_create, name='policy-group-create'),
# ]

quiz_pattterns = [
    path('', views.product_home, name='product-home'),
    path('products/products/', views.products, name='products'),
    path('products/detail/<uuid:product_uuid>/', views.product_detail, name='product-detail'),
    path('products/update/<uuid:product_uuid>/', views.product_update, name='product-update'),
    path('products/delete/<uuid:product_uuid>/', views.product_delete, name='product-delete'),
    path('products/delete/', views.products_delete, name='products-delete'),
    path('products/products-changes/', views.products_changes, name='products-changes'),
    path('products/activate/<uuid:product_uuid>/(?P<toggle>)/', views.product_toggle_active, name='product-activate'),
    path('products/product-images/<uuid:product_uuid>/', views.product_images, name='product-images'),
    path('products/product-image/detail/<uuid:image_uuid>/', views.product_image_detail, name='product-image-detail'),
    path('products/product-image/update/<uuid:image_uuid>/', views.product_image_update, name='product-image-update'),
    path('products/product-image/delete/<uuid:image_uuid>/', views.product_image_delete, name='product-image-delete'),
    path('products/product-image/create/<uuid:product_uuid>', views.product_image_create, name='product-image-create'),

]


users_patterns = [
    path('create-account/',views.create_account, name='create-account'),
    path('generate-token/', views.generate_token, name='generate-token'),
    path('tokens/', views.tokens, name='tokens'),
    path('', views.users, name='users'),
    path('customers/', views.customers, name='customers'),
    path('create-user/', views.create_account, name='create-user'),
    path('detail/<int:pk>/', views.user_details, name='user-detail'),
    path('send-welcome-mail/<int:pk>/', views.send_welcome_mail, name='send-welcome-mail'),
    path('delete/<int:pk>/', views.user_delete, name='user-delete'),
    path('users-delete/', views.users_delete, name='users-delete'),

]

"""
campaigns_patterns = [
    path('', views.campaigns, name='campaigns'),
    path('detail/<uuid:campaign_uuid>/', views.campaign_detail, name='campaign-detail'),
    path('update/<uuid:campaign_uuid>/', views.campaign_update, name='campaign-update'),
    path('delete/<uuid:campaign_uuid>/', views.campaign_delete, name='campaign-delete'),
    path('delete/', views.campaigns_delete, name='campaigns-delete'),
    path('create/', views.campaign_create, name='campaign-create'),
    path('add-products/<uuid:campaign_uuid>/', views.campaign_add_products, name='campaign-add-products'),
]

report_patterns = [
    path('reports/', views.reports, name='reports'),
    path('reports/update-suspicious-requests/', views.update_suspicious_requests, name='update-suspicious-requests'),
]
"""

urlpatterns = [
    path('', views.dashboard, name='home'),
    #path('abtests/',views.abtests, name='abtests'),
    path('quizzes/', include(quiz_pattterns, app_name), namespace="quizzes"),
    #path('campaigns/', include(campaigns_patterns, app_name), namespace='campaigns'),

    path('categories/', include(category_patterns, app_name), namespace='categories'),
    path('groups/', include(group_patterns, app_name), namespace='users'),
    path('users/', include(users_patterns, app_name), namespace="users"),

    #path('highlights/', include(highlight_patterns, app_name), namespace='highlights'),

    #path('news/',include(new_patterns, app_name), namespace='news'),

    #path('fetch-payments/', views.fetch_payments, name="fetch-payments"),
    #path('policies/', include(policy_patterns, app_name), namespace='policies'),



    path('partner-tokens/', views.partner_tokens, name='partner-tokens'),
    path('partner-token-details/<uuid:token_uuid>/', views.partner_token_details, name='partner-token-details'),
    path('partner-token-create', views.create_partner_token, name='partner-token-create'),
    path('partner-token-update/<uuid:token_uuid>/', views.update_partner_token, name='partner-token-update'),
]