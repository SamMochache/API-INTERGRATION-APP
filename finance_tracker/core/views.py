from django.shortcuts import render
from django.http import JsonResponse
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid import ApiClient, Configuration
import os
from dotenv import load_dotenv
import plotly.express as px
from django.contrib.auth.decorators import login_required
from .models import Transaction, Budget

# Load environment variables from .env file
load_dotenv()

# Set up the Plaid client
configuration = Configuration(
    host=os.getenv('PLAID_ENV')
)

api_client = ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

def get_link_token(request):
    try:
        # Create a link token request
        request_obj = LinkTokenCreateRequest(
            user={'client_user_id': 'unique-user-id'},
            client_name='Finance Tracker',
            products=['transactions'],
            country_codes=['US'],
            language='en',
        )
        response = client.link_token_create(request_obj)
        return JsonResponse(response.to_dict())
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def add_transaction(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        if amount and category:
            user = request.user
            transaction = Transaction(user=user, amount=amount, category=category)
            transaction.save()
            return JsonResponse({'status': 'Transaction Added'})
        return JsonResponse({'error': 'Amount and category are required'}, status=400)

@login_required
def set_budget(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        if amount and category:
            user = request.user
            budget = Budget(user=user, amount=amount, category=category)
            budget.save()
            return JsonResponse({'status': 'Budget Set'})
        return JsonResponse({'error': 'Amount and category are required'}, status=400)

def display_expenses(request):
    data = Transaction.objects.all()
    if data:
        fig = px.pie(data, names='category', values='amount')
        chart_html = fig.to_html(full_html=False)
        return render(request, 'core/dashboard.html', {'chart_html': chart_html})
    return render(request, 'core/dashboard.html', {'message': 'No transactions available'})

def index(request):
    return render(request, 'core/index.html')

def dashboard(request):
    context = {
        'user': request.user,
        'total_balance': 5000,  # Replace with actual calculation
        'transactions': [
            {'date': '2024-12-01', 'amount': 100, 'description': 'Grocery'},
            {'date': '2024-12-05', 'amount': 50, 'description': 'Transport'}
        ]
    }
    return render(request, 'core/dashboard.html', context)
