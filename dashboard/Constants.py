
APP_PREFIX = 'dashboard.'

SELLER_GROUP = "Seller"

MAX_RECENT = 5
TOP_VIEWS_MAX = 10

DASHBOARD_GLOBALS_PREFIX = "dashboard"



DASHBOARD_PAYMENTS_CONTEXT = {
    'PAYMENTS_URL'              : f"{DASHBOARD_GLOBALS_PREFIX}:payments",
    'PAYMENT_URL'               : f"{DASHBOARD_GLOBALS_PREFIX}:payment-detail",
}


DASHBOARD_VIEW_PERM = 'can_view_dashboard'
TOKEN_GENERATE_PERM = 'can_generate_token'

USER_VIEW_PERM = 'can_view_user'
USER_ADD_PERM = 'can_add_user'
USER_CHANGE_PERM = 'can_change_user'
USER_DELETE_PERM = 'can_delete_user'

ACCOUNT_VIEW_PERM = 'can_view_account'
ACCOUNT_ADD_PERM = 'can_add_account'
ACCOUNT_CHANGE_PERM = 'can_change_account'
ACCOUNT_DELETE_PERM = 'can_delete_account'

CASE_ISSUE_VIEW_PERM = 'can_view_claim'
CASE_ISSUE_ADD_PERM = 'can_add_claim'
CASE_ISSUE_CHANGE_PERM = 'can_change_claim'
CASE_ISSUE_DELETE_PERM = 'can_delete_claim'
CASE_ISSUE_CLOSE_PERM = 'can_close_claim'
GROUP_VIEW_PERM = 'can_view_group'
GROUP_ADD_PERM = 'can_add_group'
GROUP_CHANGE_PERM = 'can_change_group'
GROUP_DELETE_PERM = 'can_delete_group'

IDCARD_VIEW_PERM = 'can_view_idcard'
IDCARD_ADD_PERM = 'can_add_idcard'
IDCARD_CHANGE_PERM = 'can_change_idcard'
IDCARD_DELETE_PERM = 'can_delete_idcard'

PAYMENT_VIEW_PERM = 'can_view_payment'
PAYMENT_ADD_PERM = 'can_add_payment'
PAYMENT_CHANGE_PERM = 'can_change_payment'
PAYMENT_DELETE_PERM = 'can_delete_payment'

PRODUCT_VIEW_PERM = 'can_view_product'
PRODUCT_ADD_PERM = 'can_add_product'
PRODUCT_CHANGE_PERM = 'can_change_product'
PRODUCT_DELETE_PERM = 'can_delete_product'

POLICY_VIEW_PERM = 'can_view_policy'
POLICY_ADD_PERM = 'can_add_policy'
POLICY_CHANGE_PERM = 'can_change_policy'
POLICY_DELETE_PERM = 'can_delete_policy'

POLICY_GROUP_VIEW_PERM = 'can_view_policy_group'
POLICY_GROUP_ADD_PERM = 'can_add_policy_group'
POLICY_GROUP_CHANGE_PERM = 'can_change_policy_group'
POLICY_GROUP_DELETE_PERM = 'can_delete_policy_group'

POLICY_MEMBERSHIP_VIEW_PERM = 'can_view_policy_membership'
POLICY_MEMBERSHIP_ADD_PERM = 'can_add_policy_membership'
POLICY_MEMBERSHIP_CHANGE_PERM = 'can_change_policy_membership'
POLICY_MEMBERSHIP_DELETE_PERM = 'can_delete_policy_membership'

CATEGORY_VIEW_PERM = 'can_view_category'
CATEGORY_ADD_PERM = 'can_add_category'
CATEGORY_CHANGE_PERM = 'can_change_category'
CATEGORY_DELETE_PERM = 'can_delete_category'


