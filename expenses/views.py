from django.shortcuts import render, redirect
from .models import Expense, Member
from django.db.models import Sum, Max

def home(request):
    # Fetch all expenses, most recent first
    expenses = Expense.objects.all().order_by('-date_added')
    
    # Calculate total paid per member
    balance = Expense.objects.values('paid_by').annotate(total=Sum('amount'))
    
    return render(request, 'expenses/home.html', {
        "expenses": expenses,
        "balance": balance
    })

def add_expense(request):
    if request.method == "POST":
        desc = request.POST['description']
        amt = float(request.POST['amount'])
        paid_by_other = request.POST.get('paid_by_other', '').strip()
        paid_by_select = request.POST.get('paid_by', '').strip()
        paid_by = paid_by_other or paid_by_select or 'Unknown'
        
        # Create expense (date_added is auto-handled)
        Expense.objects.create(description=desc, amount=amt, paid_by=paid_by)
        return redirect('home')

    # Fetch members for dropdown
    members = Member.objects.all().order_by('name')
    return render(request, 'expenses/add_expense.html', {'members': members})

def members(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        contact = request.POST.get('contact', '').strip()
        if name:
            Member.objects.create(name=name, contact=contact)
            return redirect('members')

    members = Member.objects.all().order_by('name')
    expense_names = Expense.objects.values_list('paid_by', flat=True).distinct()
    member_names = set(members.values_list('name', flat=True))
    others = [n for n in expense_names if n and n not in member_names]

    return render(request, 'expenses/members.html', {'members': members, 'others': others})

def balance(request):
    # Aggregate total and last payment date per member
    totals_qs = Expense.objects.values('paid_by').annotate(
        total=Sum('amount'),
        last_date=Max('date_added')
    )
    totals = {item['paid_by']: item['total'] for item in totals_qs}
    last_dates = {item['paid_by']: item['last_date'] for item in totals_qs}

    # All member names including unpaid ones
    member_names = sorted(set(list(totals.keys()) + list(Member.objects.values_list('name', flat=True))))
    total_expense = sum(totals.values()) if totals else 0
    count = len(member_names) if member_names else 1
    per_person_share = total_expense / count if count > 0 else 0

    rows = []
    for name in member_names:
        paid = totals.get(name, 0)
        balance_amt = paid - per_person_share
        last_date = last_dates.get(name, None)
        rows.append({
            'name': name,
            'paid': paid,
            'share': per_person_share,
            'balance': balance_amt,
            'balance_abs': abs(balance_amt),
            'last_date': last_date
        })

    return render(request, 'expenses/balance.html', {
        'rows': rows,
        'total_expense': total_expense,
        'per_person_share': per_person_share
    })
