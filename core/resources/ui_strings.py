from django.utils.translation import gettext_lazy as _
from jaribio import settings

DASHBOARD_DASHBOARD_TITLE = _('Dashboard')
DASHBOARD_PAYMENT_HOME_TITLE = _('Payment Home')
DASHBOARD_PRODUCT_HOME_TITLE = _('Product Home')
DASHBOARD_VENDOR_HOME_TITLE = _('Vendor Home')
DASHBOARD_SHIPMENT_HOME_TITLE = _('Shipment Home')
DASHBOARD_PAYMENT_REQUEST_HOME_TITLE = _('Payment Request Home')
DASHBOARD_PRICE_CALCULATOR_TITLE = _('Price Calculator')


DASHBOARD_ATTRIBUTES_TITLE = _('Attributes')
DASHBOARD_ATTRIBUTE_TITLE = _('Attribute')
DASHBOARD_ATTRIBUTE_UPDATE_TITLE = _('Attribute Update')
DASHBOARD_ATTRIBUTE_CREATE_TITLE = _('New Attribute')

DASHBOARD_BALANCE_HISTORY_TITLE         = _('Balance History')
DASHBOARD_BALANCE_HYSTORIES_TITLE       = _('Balance Histories')

DASHBOARD_BRANDS_TITLE                  = _('Brands')
DASHBOARD_BRAND_TITLE                   = _('Brand')
DASHBOARD_BRAND_CREATE_TITLE            = _('New Brand')
DASHBOARD_BRAND_UPDATE_TITLE            = _('Brand Update')
DASHBOARD_BRAND_PRODUCTS_TITLE          = _('Brand Products')

DASHBOARD_COUPONS_TITLE                 = _('Coupons')
DASHBOARD_COUPON_TITLE                  = _('Coupon')
DASHBOARD_COUPON_CREATE_TITLE           = _('New Coupon')
DASHBOARD_COUPON_UPDATE_TITLE           = _('Coupon Update')

DASHBOARD_INFOS_TITLE                 = _('Infos')
DASHBOARD_INFO_TITLE                  = _('Info')
DASHBOARD_INFO_CREATE_TITLE           = _('New Info')
DASHBOARD_INFO_UPDATE_TITLE           = _('Info Update')

DASHBOARD_GROUPS_TITLE                 = _('Groups')
DASHBOARD_GROUP_TITLE                  = _('Group')
DASHBOARD_GROUP_CREATE_TITLE           = _('New Group')
DASHBOARD_GROUP_UPDATE_TITLE           = _('Group Update')


DASHBOARD_HIGHLIGHTS_TITLE                  = _('Highlights')
DASHBOARD_HIGHLIGHT_TITLE                 = _('Highlight')
DASHBOARD_HIGHLIGHT_UPDATE_TITLE           = _('Highlight Update')
DASHBOARD_HIGHLIGHT_CREATE_TITLE           = _('New Highlight')

DASHBOARD_CAMPAIGNS_TITLE               = _('Campaigns')
DASHBOARD_CAMPAIGN_UPDATE_TITLE               = _('Campaign Update')
DASHBOARD_CAMPAIGN_CREATE_TITLE               = _('Campaign Create')
DASHBOARD_CAMPAIGN_TITLE               = _('Campaign')

DASHBOARD_ORDERS_TITLE                  = _('Orders')
DASHBOARD_ORDER_TITLE                   = _('Order')
DASHBOARD_ORDER_UPDATE_TITLE            = _('Order Update')
DASHBOARD_ORDER_ITEM_TITLE              = _('Order Item')
DASHBOARD_ORDER_ITEM_UPDATE_TITLE       = _('Order Item Update')
DASHBOARD_ORDER_HISTORY_TITLE           = _('Order History')

DASHBOARD_PAYMENT_TITLE = _('Payment')
DASHBOARD_PAYMENTS_TITLE = _('Payments')

DASHBOARD_PAYMENT_REQUESTS_TITLE = _('Payment Requests')
DASHBOARD_PAYMENT_REQUEST_TITLE = _('Payment Request')

DASHBOARD_PAYMENT_METHODS_TITLE = _('Payment Methods')
DASHBOARD_PAYMENT_METHOD_TITLE = _('Payment Method')
DASHBOARD_PAYMENT_METHOD_UPDATE_TITLE = _('Payment Method Update')
DASHBOARD_PAYMENT_METHOD_CREATE_TITLE = _('New Payment Method')

DASHBOARD_POLICIES_TITLE = _('Policies')
DASHBOARD_POLICY_TITLE = _('Policy')
DASHBOARD_POLICY_UPDATE_TITLE = _('Policy Update')
DASHBOARD_POLICY_CREATE_TITLE = _('New Policy')

DASHBOARD_POLICY_GROUPS_TITLE = _('Policy Groups')
DASHBOARD_POLICY_GROUP_TITLE = _('Policy Group')
DASHBOARD_POLICY_GROUP_UPDATE_TITLE = _('Policy Group Update')
DASHBOARD_POLICY_GROUP_CREATE_TITLE = _('New Policy Group')


DASHBOARD_USERS_TITLE = _('Users')
DASHBOARD_CUSTOMERS_TITLE = _('Customers')
DASHBOARD_SELLERS_TITLE = _('Sellers')
DASHBOARD_USER_TITLE = _('User')
DASHBOARD_USER_UPDATE_TITLE = _('User Update')
DASHBOARD_USER_CREATE_TITLE = _('New User')


DASHBOARD_TOKENS_TITLE = _('Tokens')
DASHBOARD_PARTNER_TOKENS_TITLE = _('Partner Tokens')
DASHBOARD_TOKEN_CREATE_TITLE = _('New Token')

DASHBOARD_REPORTS_TITLE = _('Reports')

DEFAULT_HIGHLIGHT_FEATURES = _('Features')
DEFAULT_HIGHLIGHT_NEW_ARRIVALS = _('New Arrivals')
DEFAULT_HIGHLIGHT_TOP_10 = _('Top 10')
DEFAULT_HIGHLIGHT_BEST_DEALS = _('Best deals of the Week')
DEFAULT_HIGHLIGHT_SALES = _('Sales')
LABEL_NEW = _('New')
LABEL_NEW_UPPERCASE = _('NEW')

INFOS_FREE_SHIPPING_TITLE = _('Free shipping')
INFOS_FREE_SHIPPING_CONTENT = _('LYSHOP is offering free shipping for members. This offers is limited.')

INFOS_CUSTOM_SALE_TITLE = _('Sale')
INFOS_CUSTOM_SALE_CONTENT = _('LYSHOP is currently offering sale on selected articles.')
RECOMMANDATION_LABEL = _('Recommendation')

PRODUCT_ADDED = _('Product Added')

REQUEST_ERROR = _('Error on the request')
INVALID_FORM = _('Invalid Submitted data')



# CATEGORIES



CATEGORY_SEE_ALL = _('See all')

UI_PARFUM_BANNER_DESCRIPTION = _("Always smell good with our exclusive selection of fragrances!")
UI_MODE_BANNER_DESCRIPTION = _("Define your own style with our items available for men, women and children !")
UI_LYSHOP_BANNER_DESCRIPTION = _("Your online shop in Gabon")

UI_PRODUCT_AVAILABILITY = _('Availability')
UI_PRODUCT_AVAILABILITY_LOW = _('availability')
UI_CART_ON_DEMAND_TITLE = _("Items available to order")
UI_ON_DEMANDE_HINT = _("This article is only available to order. The delivery time varies between 1 to 2 months. An advance of half the belly price is required.")
UI_CART_CONTAINS_ON_DEMAND = _("Your basket contains items that are only available to order. These items will not be delivered at the same time as the items available immediately.")
UI_CART_ON_DEMAND_PAYMENT_HINT = _("An advance of half of the total price of the items on order is required.")
UI_CART_ON_DEMAND_SPLITUP_HINT = _("Your order will be divided into two groups, one order containing the items available immediately and the other part containing the items available immediately.")
UI_PRODUCT_OPEN_CREATED_URL = _("Open the create Product")
UI_CONTACT_SUBJECT = _('Need more information')
UI_CONTACT_BODY = _('Hello, I have a question about your products.')
UI_WHATSAPP_BODY = f'Bonjour, je suis interésé(e) par vos articles sur votre site {settings.SITE_HOST}. Pouvez me donner plus d\'informations ? Merci !' 
UI_INVALID_USER_REQUEST = _('Invalid user request')
UI_RESOURCE_NOT_FOUND_TITLE = _('Resource not found !')
UI_RESOURCE_NOT_FOUND = _('The resource you requested does not exist or is no longer available. Visit our catalog to discover other products.')
UI_400_TITLE = _('Bad Request')
UI_400 = _('You submitted a bad request.')
UI_404_TITLE = UI_RESOURCE_NOT_FOUND_TITLE
UI_404 = UI_RESOURCE_NOT_FOUND
UI_403_TITLE = _('Access Forbidden')
UI_403 = _('You can not access this page.')

UI_500_TITLE = _('Server Error')
UI_500 = _('Oups ! There is an intern error. If the errors persists please informe our team through our contact.')
UI_GO_TO_QUIZ = _('Go to QUIZ-Home')
UI_HOME_PAGE = _('Home')
UI_CAMPAIGN_CREATE_BTN_LABEL = _('Create Campaign')
UI_CAMPAIGN_IMAGE_TITLE = _('Campaign Image')
UI_BACK_BTN_LABEL = _('Back')
UI_CREATE_BTN_LABEL = _('Create')
UI_UPDATE_BTN_LABEL = _('Update')
UI_CANCEL_BTN_LABEL = _('Cancel')
UI_SEND_BTN_LABEL   = _('Send')
UI_SEO_CATALOG_HOME = _('Buy Shoes|Parfums|Smartphones|Women|Men|Children')
UI_SEO_HOME = _('Your online Shop for Shoes|clothes|parfums in Gabon|LYSHOP')
UI_ADDRESS_BILLING_AND_SHIPPING = _("USED FOR BILLING AND SHIPPING")
UI_ADDRESS_BILLING = _("USED FOR BILLING")
UI_ADDRESS_SHIPPING = _("USED FOR SHIPPING")

UI_CATEGORY_WOMEN_DESCRIPTION = _("Change your style without constraints and try out new styles for women. Shoes, Clothing, Underwear, Eau de parfum, Eau de toilette, Bags and other accessories available at LYSHOP")
UI_CATEGORY_MEN_DESCRIPTION = _("Discover our collection for men. Revisit your style with our items available for men. Choose your items and customize your look. With shoes like Moccasins, Boots, Pants, Perfumes, Sneaker, Sandals available at LYSHOP your online store in Gabon. Become yourself again!")
UI_CATEGORY_CHILDREN_DESCRIPTION = _("Finding children's items is not always easy! That was before ! Discover our selection of quality for children. Footwear, Clothing, Accessories, Underwear for girls and boys.")
UI_CAMPAIGN_FLASH_TITLE = _('LYSHOP FLASH SALE')
UI_CAMPAIGN_FLASH_DESCRIPTION  = _('Our FLASH SALE is a way to have quality items at reduced prices. Items available as long as stock is available')



UI_STRINGS_CONTEXT = {

    'UI_CONTACT_SUBJECT': UI_CONTACT_SUBJECT,
    'UI_CONTACT_BODY': UI_CONTACT_BODY,
    'UI_RESOURCE_NOT_FOUND': UI_RESOURCE_NOT_FOUND,
    'UI_GO_TO_QUIZ': UI_GO_TO_QUIZ,
    'UI_HOME_PAGE': UI_HOME_PAGE,
    'UI_RESOURCE_NOT_FOUND_TITLE': UI_RESOURCE_NOT_FOUND_TITLE,
    'UI_400_TITLE': UI_400_TITLE,
    'UI_400': UI_400,
    'UI_403_TITLE' : UI_403_TITLE,
    'UI_403': UI_403,
    'UI_404_TITLE': UI_404_TITLE,
    'UI_404': UI_404,
    'UI_500_TITLE': UI_500_TITLE,
    'UI_500': UI_500,
    'UI_BACK_BTN_LABEL': UI_BACK_BTN_LABEL,
    'UI_CREATE_BTN_LABEL' : UI_CREATE_BTN_LABEL,
    'UI_UPDATE_BTN_LABEL': UI_UPDATE_BTN_LABEL,
    'UI_CANCEL_BTN_LABEL': UI_CANCEL_BTN_LABEL,
    'UI_SEND_BTN_LABEL'  : UI_SEND_BTN_LABEL,
    'UI_ADDRESS_BILLING_AND_SHIPPING': UI_ADDRESS_BILLING_AND_SHIPPING,
    'UI_ADDRESS_BILLING' : UI_ADDRESS_BILLING,
    'UI_ADDRESS_SHIPPING' : UI_ADDRESS_SHIPPING,
    'UI_WHATSAPP_BODY': UI_WHATSAPP_BODY,
}