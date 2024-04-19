from flask import jsonify, request, g
from datetime import datetime, timezone
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.transactions import bp
from app.models import Transaction, Account, User
from app.utils import allacounts
from flask_babel import get_locale

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
    g.locale = str(get_locale())


@bp.route('/transact', methods=['POST'])
@login_required
def create_transaction():
    data = request.json
    amount = data.get('amount')
    direction = data.get('direction')
    description = data.get('description')
    account_number = data.get('account_number')
    second_account_number = data.get('second_account_number')


    if not all([amount, direction, description, account_number, second_account_number]):
        return jsonify({ 'error": "Missing required fields' }), 400
    
    try:
        amount  = int(amount)
        direction = int(direction)
        account_number = int(account_number)
        second_account_number = int(second_account_number)
    except ValueError:
        return jsonify({ 'error': 'Invalid amount account number or direction'}), 400
    
    if direction not in [-1, 1]:
        return jsonify({ 'error': 'Direction must be -1 or 1'}), 400
    
    account = Account.query.filter_by(number=account_number).first()
    second_account = Account.query.filter_by(number=second_account_number).first()

    # first account doesn't exist
    if not account:
        #create acccount and add to db

        #get account_name and normal
        #normal
        account_normal = [-1, 1]
        cur_normal = account_normal[0]
        if direction == 1: 
            cur_normal = account_normal[1]
        #account_name 
        account_name = allacounts.get(account_number)
        #
        account = Account(name=account_name, normal=cur_normal, number=account_number)
        #add to db
        db.session.add(account)
    
    # second account doesn't exist
    if not second_account:
        #create second account and add to db

        #get second_account_name and normal
        #normal
        acccount_normal = [-1, 1]
        cur_normal = acccount_normal[1]
        opposite_direction = 1
        if direction == 1:
            opposite_direction == -1
            cur_normal == acc_normal[0]

        #second_account_name
        second_account_name = allacounts.get(second_account_number)
        #create second account
        second_account= Account(name=second_account_name, normal=cur_normal, number=second_account_number )
        #add to db
        db.session.add(second_account)
        db.session.commit()



    transaction_id = Transaction.query.count() + 1
    opposite_direction =  -1 * direction

    #create new transaction - first entry
    new_transaction = Transaction(
        transaction_id=transaction_id,
        amount=amount,
        direction=direction,
        description=description,
        client=current_user,
        account_id=account.number,
        second_account_id=second_account.number
    )   

    db.session.add(new_transaction)

    #create new transaction - second entry
    opposite_transaction = Transaction(
        transaction_id = transaction_id,
        amount=amount,
        direction=opposite_direction,
        description=description,
        client=current_user,
        account_id=second_account.number,
        second_account_id=account.number
    )
    db.session.add(opposite_transaction)
    db.session.commit()

    return jsonify({ 'message': 'Transaction created successfully'}), 201

    
@bp.route('/transactions', methods=['GET'])
@login_required
def get_transactions():
    transactions = Transaction.query.limit(10).all()

    serialized_transactions = []
    for transaction in transactions:  
        serialized_transaction = { 
            'id': transaction.id,
            'transaction_id': transaction.transaction_id,
            'amount': transaction.amount,
            'direction': transaction.direction,
            'description': transaction.description,
            'account_number': transaction.account_id,
            'second_account_number': transaction.second_account_id,
            'client': transaction.client.username
        }   
        serialized_transactions.append(serialized_transaction)
    return jsonify(serialized_transactions), 200

@bp.route('/transactions/user/<int:user_id>', methods=['GET'])
@login_required
def get_user_transactions(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({ 'error': 'User not found' }), 404

    transactions = db.session.query(Transaction).filter(Transaction.client.has(id=user_id)).all()

    serialized_transactions = []
    for transaction in transactions:
        serialized_transaction = {
            'id': transaction.id,
            'transaction_id': transaction.transaction_id,
            'amount': transaction.amount,
            'direction': transaction.direction,
            'description': transaction.description,
            'account_number': transaction.account_id,
            'second_account_number': transaction.second_account_id,
            'client': transaction.client.username  
        }
        serialized_transactions.append(serialized_transaction)

    return jsonify(serialized_transactions), 200