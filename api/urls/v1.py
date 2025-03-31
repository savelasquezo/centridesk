from django.urls import path

from src.accounts.views.account import AccountView
from src.accounts.views.accounts import AccountsSetUpView
from src.actions.views.actions import Actions
from src.auth.views.static_user_token import StaticUserToken
from src.channels.views.channel import Channel
from src.channels.views.channels import Channels
from src.configurations.views.transcriptions import TranscriptionsView
from src.comments.views.attachments import Attachments
from src.comments.views.comment import Comment
from src.comments.views.comments import Comments
from src.customers.views.customer import Customer
from src.customers.views.customers import Customers
from src.customers.views.customers_filter import CustomersFilter
from src.search.views.generic_search import GenericSearch
from src.status.views.status import HealthStatus
from src.templates.views.templates import TemplatesView
from src.tickets.views.ticket import Ticket
from src.tickets.views.ticket_priorities import TicketPriorities
from src.tickets.views.tickets import Tickets
from src.tickets.views.tickets_filter import TicketsFilter
from src.tickets.views.tickets_status import TicketsStatus
from src.users.views.users_device import UsersDevice

urlpatterns = [
    # Status
    path('status', HealthStatus.as_view()),

    # Channels
    path('channels', Channels.as_view()),
    path('channels/<str:channel_id>', Channel.as_view()),

    path('tickets/status', TicketsStatus.as_view()),
    path('tickets/priorities', TicketPriorities.as_view()),

    # # By Account # #
    # Account
    path('accounts/setup', AccountsSetUpView.as_view()),
    path('accounts/<str:account_id>', AccountView.as_view()),

    # Generic Search
    path('accounts/<str:account_id>/<str:type>/search', GenericSearch.as_view()),

    # Customers
    path('accounts/<str:account_id>/customers', Customers.as_view()),
    path('accounts/<str:account_id>/customers/filter', CustomersFilter.as_view()),
    path('accounts/<str:account_id>/customers/<str:customer_id>', Customer.as_view()),

    # Tickets
    path('accounts/<str:account_id>/tickets', Tickets.as_view()),
    path('accounts/<str:account_id>/tickets/filter', TicketsFilter.as_view()),
    path('accounts/<str:account_id>/tickets/<str:ticket_id>', Ticket.as_view()),
    path('accounts/<str:account_id>/tickets/<str:ticket_id>/comments', Comments.as_view()),
    path('accounts/<str:account_id>/tickets/<str:ticket_id>/comments/attachments', Attachments.as_view()),
    path('accounts/<str:account_id>/tickets/<str:ticket_id>/comments/<str:comment_id>', Comment.as_view()),

    # Templates
    path('accounts/<str:account_id>/campaigns/templates', TemplatesView.as_view()),

    # No expired authentication
    path('auth', StaticUserToken.as_view()),

    # Users
    path('users/device', UsersDevice.as_view()),

    # Actions
    path('accounts/<str:account_id>/actions', Actions.as_view()),

    # Transcriptions
    path('accounts/<str:account_id>/transcriptions', TranscriptionsView.as_view()),
]
